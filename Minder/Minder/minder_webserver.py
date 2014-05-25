import time
import os
import BaseHTTPServer
import webbrowser
import time
from string import Template
import minder_config as mc
import minder_defaults as md
import minds
import mimetypes
import urllib


HOST_NAME = ''
PORT_NUMBER = 8051
CUR_DIR = os.getcwd()
WEBROOT = os.path.join(CUR_DIR, 'webroot')
mit = Template(md.minds)
methods_list = {
    'home': 'md.home',
    'index': 'md.home',
    'settings': 'expand_settings()',
    'minds': 'mit.substitute(iter_folders(minds.interrogate(mc.USER_DIRECTORY)))',
    'remotes': 'md.remotes'
}
print 'Setting Web root directory - %s' % WEBROOT


#TODO Maybe put some of these methods in the WebServer so we can access self.path?
def get_template(path_name=None, params=None):
    """Parameters: [title (String), navbar_active[key], breadcrumbs
    main_container(content)]"""
    #print 'get_template on %s' % path_name
    hidden_files = eval(mc.minderconfig()['Settings']['show_hidden_files_boolean'])
    sd = {}
    p = path_name.split('.')[0].strip('/')
    #print 'Template path - %s  parameters - %s' %(p, params)
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
        print "EMPTY METHOD CALL - %s" % p
        sd['main_container'] = eval(methods_list[p])
        sd['breadcrumbs'] = breadcrumber({'root': '', 'name': p})

    mt = Template(md.main_template)
    html_string = mt.substitute(sd)

    return html_string


def expand_settings():
    config_uom = md.CONFIG_UOM
    config_dict = mc.read_minder_settings()
    fo = Template(md.form_select_options)
    fi = Template(md.form_item['text'])
    ft = Template(md.form_group)
    st = Template(md.settings)
    pt = Template(md.panel_group)
    final_html = ""
    section_html= ""
    for section in config_dict['sections']:

        form_builder = {
                        "title": "Settings",
                        "section": section['name'],
                        "form_groups": ""
                        }

        for i in section['items']:
            select_options = ""
            key_type = i['key'].split('_')[-1]
            template_item = md.form_item[i['type']]

            if i['type'] == 'select':
                value_list = list(config_uom[key_type]['options'])
                selected_value = {
                                  "option": value_list.pop(value_list.index(i['value'])),
                                  "selected": " selected"
                                  }
                select_options += fo.substitute(selected_value)
                for option in value_list:
                    select_options += fo.substitute({'option': option, 'selected': ''})

            if i['uom'] is not None:
                template_item += md.form_item['uom']
            else:
                pass

            i["select_options"] = select_options
            fi = Template(template_item)
            i["form_items"] = fi.substitute(i)
            form_builder['form_groups'] += ft.substitute(i)

        section_html += st.substitute(form_builder)

    final_html += pt.substitute({'title': 'Settings', 'panels': section_html})


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

    # TODO Check this on windows for regressions
    #if breadcrumb[0] == '':
    #    breadcrumb.pop(0)

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
    file_path = os.path.join(WEBROOT + file_name)
    #print 'Reading file from file system - %s' % file_path
    with open(file_path, "rb") as read_handle:

        file_string = read_handle.read()
    m = mimetypes.guess_type(file_name)
    #print 'Mimetype guessed - %s for file %s' % (m, file_name)
    return [m[0], file_string]


class MinderWebApp(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


    def do_GET(self):
        #TODO CR: Use a proper logger
        url_path = urllib.unquote(self.path)
        parsed_url = url_path.split('.')[-1]
        #print 'decoded - %s' % url_path
   
        try:
            if url_path.endswith('.html'):
                h = get_template(url_path.strip('/'))
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(h)

            elif len(url_path.split('?')) > 1:
                g = url_path.split('?')
                h = get_template(g[0], g[1])
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(h)

            elif parsed_url in md.WEB_FILES:
                c = get_file(url_path)
                #print "Retrieving file - %s" % url_path
                self.send_response(200)
                self.send_header("Content-type", c[0])
                self.end_headers()
                self.wfile.write(c[1])

        except (IOError):
            self.send_response(404)
            self.send_header("Content-type", 0)
            self.end_headers()


    def do_POST(self):
        url_path = urllib.unquote(self.path)
        content_length = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_length)
        #print post_body
        post_params = post_body.split('&')
        param_dict = {}

        for i in post_params:
            parsed_i = urllib.unquote(i)
            parsed_i = parsed_i.replace('+', ' ')
            param_dict[parsed_i.split('=')[0]] = parsed_i.split('=')[1]
        print url_path, param_dict

        if url_path == '/settings.html':
            section = {param_dict.pop('section'): param_dict}
            mc.minderconfig(section, update=True)
            time.sleep(1)
            h = get_template(url_path.strip('/'))
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(h)

        else:
            self.send_response(404)
            self.send_header("Content-type", 0)
            self.end_headers()


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
