import time
import os
import BaseHTTPServer
import webbrowser
import json
from string import Template
import minder_config as mc
import minder_defaults as md
import mimetypes


HOST_NAME = ''
PORT_NUMBER = 8051
CUR_DIR = os.getcwd()
WEBROOT = os.path.join(CUR_DIR, 'webroot')
mt = Template(md.minds)
methods_list = {'index': 'md.index',
     'settings': 'expand_settings()',
     'minds': 'mt.substitute(iterFolders(md.mind, final_html=[]))',
     'remotes': 'md.remotes'}


def get_template(path_name=None):
    """Parameters: [title (String), navbar_active[key], breadcrumbs
    main_container(content)]"""
    sd = {}
    p = path_name.split('.')[0]
    print p
    sd['title'] = p
    sd['navbar_active'] = md.navbar_active[p]
    sd['breadcrumbs'] = md.breadcrumb_list
    sd['main_container'] = eval(methods_list[p])
    t = Template(md.main_template)
    html_string = t.substitute(sd)
    return html_string


def expand_settings():
    config_dict = json.loads(md.config)
    ft = Template(md.form_group)
    st = Template(md.settings)
    final_html = ""
    for section in config_dict['config']:
        form_builder = {"section": None, "form_groups":""}
        form_builder['section'] = section['section']['name']
        for i in section['section']['items']:
            form_builder['form_groups'] += ft.substitute(i)
        final_html += st.substitute(form_builder)
    return final_html


def iterFolders(d, final_html=None):

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
            iterFolders(folder, final_html)
        final_html.append(eft.substitute(fd))

    else:
        final_html.append(eft.substitute(fd))

    result = ''.join(final_html)
    return {"folders_template": result}


def get_file(file_name):
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
        try:
            if self.path.endswith('.html'):
                h = get_template(self.path.strip(os.path.sep))
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(h)
            else:
                c = get_file(self.path)
                print self.path
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
    webbrowser.open("http://localhost:8051/index.html", new=0)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)