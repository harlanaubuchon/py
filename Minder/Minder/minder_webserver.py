import time
import os
import BaseHTTPServer
import webbrowser
import json
from string import Template
import minder_config as mc
import minder_defaults as md
import minds
import mimetypes


HOST_NAME = ''
PORT_NUMBER = 8051
CUR_DIR = os.getcwd()
WEBROOT = os.path.join(CUR_DIR, 'webroot')
mit = Template(md.minds)
methods_list = {'home': 'md.home',
                'index': 'md.index',
     'settings': 'expand_settings()',
     'minds': 'mit.substitute(iter_folders(md.mind, hidden_files=False))',
     'remotes': 'md.remotes'}

#TODO Maybe put some of these methods in the WebServer so we can access self.path?

def get_template(path_name=None, params=None):
    """Parameters: [title (String), navbar_active[key], breadcrumbs
    main_container(content)]"""
    hidden_files = False
    sd = {}
    p = path_name.split('.')[0]
    print p, params
    sd['title'] = p
    sd['navbar_active'] = md.navbar_active[p]
    if params is not None and p == 'minds':
        pm = params.split('=')[1]
        minds_dict = minds.interrogate(pm, hidden_files)
        sd['main_container'] = mit.substitute(iter_folders(minds_dict))
        sd['breadcrumbs'] = breadcrumber(minds_dict)

    elif params is None and p == 'minds':
        minds_dict = minds.interrogate(mc.USER_DIRECTORY, hidden_files)
        sd['main_container'] = mit.substitute(iter_folders(minds_dict))
        sd['breadcrumbs'] = breadcrumber(minds_dict)

    else:
        sd['main_container'] = eval(methods_list[p])
        sd['breadcrumbs'] = breadcrumber({'root': '', 'name': p})

    mt = Template(md.main_template)
    html_string = mt.substitute(sd)
    return html_string


def expand_settings():
    config_dict = json.loads(md.config)
    ft = Template(md.form_group)
    st = Template(md.settings)
    final_html = ""
    for section in config_dict['config']:
        form_builder = {
                        "section": None,
                        "form_groups": ""
        }

        form_builder['section'] = section['section']['name']
        for i in section['section']['items']:
            form_builder['form_groups'] += ft.substitute(i)
        final_html += st.substitute(form_builder)
    return final_html


def iter_folders(d, final_html=None):
    if final_html is None:
        final_html = []
    bft = Template(md.begin_folders_template)
    fit = Template(md.files_template)
    eft = Template(md.end_folders_template)
    final_html.append(bft.substitute(d))
    fd = {"file_html": ""}

    if len(d['files']) > 0:
        for fi in d['files']:
            fd['file_html'] += fit.substitute(fi)

    if len(d['files']) == 0:
        fd['file_html'] += md.empty_files_template

    if len(d['folders']) > 0:
        for folder in d['folders']:
            iter_folders(folder, final_html)
        final_html.append(eft.substitute(fd))

    else:
        final_html.append(eft.substitute(fd))

    result = ''.join(final_html)
    return {"folders_template": result}


def breadcrumber(t):
    bct = Template(md.breadcrumbs)
    brt = Template(md.breadcrumb_refs)
    bat = Template(md.breadcrumb_active)
    root_path = os.path.join(t['root'], t['name'])
    breadcrumb = []
    html_list = []

    for parts in root_path.split(os.path.sep):
        breadcrumb.append(parts)

    if breadcrumb[0] == '':
        breadcrumb.pop(0)

    for b in range(len(breadcrumb)):
        pd = {
            'path': os.path.sep.join(breadcrumb),
            'name': breadcrumb.pop(-1)
        }
        html_list.append(pd)
    html_list.reverse()

    breadcrumb_html = ""
    active_html = bat.substitute(html_list.pop(-1))
    for h in html_list:
        breadcrumb_html += brt.substitute(h)

    breadcrumb_html += active_html
    final_html = {"breadcrumb_list": breadcrumb_html}

    return bct.substitute(final_html)


def get_file(file_name):
    #TODO CR: fix to use 'with open()'
    f = open(WEBROOT + file_name)
    file_string = f.read()
    m = mimetypes.guess_type(WEBROOT + file_name)
    f.close()
    return [m[0], file_string]


class MinderWebApp(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


    def do_GET(self):
        #TODO CR: Use a proper logger
        #print self.path
        try:
            if self.path.endswith('.html'):
                h = get_template(self.path.strip('/'))
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(h)

            elif len(self.path.split('?')) > 1:
                g = self.path.split('?')
                print g
                h = get_template(g[0].strip('/'), g[1])
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(h)

            else:
                c = get_file(self.path)
                print "Retreiving file - %s" % self.path
                self.send_response(200)
                self.send_header("Content-type", c[0])
                self.end_headers()
                self.wfile.write(c[1])

        except (IOError):
            self.send_response(404)
            self.send_header("Content-type", 0)
            self.end_headers()


    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", 0)
        self.end_headers()
        content_length = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_length)
        print post_body
        post_params = post_body.split('&')
        param_dict = {}
        for i in post_params:
            param_dict[i.split('=')[0]] = i.split('=')[1]
        print param_dict


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MinderWebApp)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    webbrowser.open("http://localhost:8051/home.html", new=0)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)