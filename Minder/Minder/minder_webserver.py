import time
import os
import sys
import BaseHTTPServer
import webbrowser
import time
import mimetypes
import urllib
from urlparse import urlparse
import subprocess
from string import Template
import minder_config as mc
import minder_defaults as md
import minds


HOST_NAME = ''
PORT_NUMBER = 8051
CUR_DIR = os.getcwd()
WEBROOT = os.path.join(CUR_DIR, 'webroot')
M_CONFIG = mc.minderconfig()
mit = Template(md.minds)
mbt = Template(md.bare_mind)
methods_list = {
    'home': 'md.home',
    'index': 'md.home',
    'settings': "expand_sections('settings')",
    'minds': "expand_sections('minds')",
    'folders': "mbt.substitute(iter_folders(minds.interrogate(mc.USER_DIRECTORY)))",
    'remotes': 'mit.substitute(iter_folders(minds.interrogate(mc.USER_DIRECTORY)))'
}


#TODO Maybe put some of these methods in the WebServer so we can access self.path?
def get_template(path_name=None, params=None):
    """Parameters: [title (String), navbar_active[key], breadcrumbs
    main_container(content)]"""
    #print 'get_template on %s' % path_name
    hidden_files = eval(mc.minderconfig()['System']['show_hidden_files_boolean'])
    sd = {}
    p = path_name.split('.')[0].strip('/')

    #ALL
    if p != 'folders':
        sd['title'] = p
        sd['navbar_active'] = md.navbar_active[p]

    if params is not None and p == 'remotes':
        pm = params.split('=')[1]
        minds_dict = minds.interrogate(pm, hidden_files)
        sd['main_container'] = mit.substitute(iter_folders(minds_dict))
        sd['breadcrumbs'] = breadcrumber(minds_dict)

    elif params is None and p == 'remotes':
        minds_dict = minds.interrogate(mc.USER_DIRECTORY, hidden_files)
        sd['main_container'] = mit.substitute(iter_folders(minds_dict))
        sd['breadcrumbs'] = breadcrumber(minds_dict)

    else:
        sd['main_container'] = eval(methods_list[p])
        sd['breadcrumbs'] = breadcrumber({'root': '', 'name': p})

    if p == 'folders':
        html_string = sd['main_container']

    else:
        mt = Template(md.main_template)
        html_string = mt.substitute(sd)

    h_response = {
        'code': 404,
        'type': 0,
        'body': None
    }

    return h_response


def route_request(u):
    qp = None
    sd = None
    http_body = None

    #try:
    if u.query:
        qp = {}
        for q in u.query.split('&'):
            q_pair = q.split('=')
            qp[q_pair[0]] = q_pair[1]

        minds_dict = minds.interrogate(qp)
        breadcrumb_dict = {'root': minds_dict['root'], 'name': minds_dict['name']}
        sd = {
            'title': u.path,
            'navbar_active': md.navbar_active[u.path],
            'main_container': mit.substitute(iter_folders(minds_dict)),
            'breadcrumbs': breadcrumber(breadcrumb_dict),
        }

    else:
        qp = {'root': mc.USER_DIRECTORY}

        if u.path == 'remotes':
            minds_dict = minds.interrogate(mc.USER_DIRECTORY)
            breadcrumb_dict = {'root': minds_dict['root'], 'name': minds_dict['name']}
            sd = {
                'title': u.path,
                'navbar_active': md.navbar_active[u.path],
                'main_container': mit.substitute(iter_folders(minds_dict)),
                'breadcrumbs': breadcrumber(breadcrumb_dict),
            }
            http_body = sd['main_container']

        if u.path == 'folders':
            minds_dict = minds.interrogate(mc.USER_DIRECTORY)
            breadcrumb_dict = {'root': minds_dict['root'], 'name': minds_dict['name']}
            sd = {
                'title': None,
                'navbar_active': None,
                'main_container': mbt.substitute(iter_folders(minds_dict)),
                'breadcrumbs': breadcrumber(breadcrumb_dict),
            }
            http_body = sd['main_container']

        else:
            sd = {
                'title': u.path,
                'navbar_active': md.navbar_active[u.path],
                'main_container': eval(methods_list[u.path]),
                'breadcrumbs': breadcrumber({'root': '', 'name': u.path}),
            }
            mt = Template(md.main_template)
            http_body = mt.substitute(sd)

    h_response = {
        'code': 200,
        'type': 'text/html',
        'body': http_body
    }

    #except:
    #    h_response = {
    #        'code': 404,
    #        'type': 'text/html',
    #        'body': md.html_404
    #    }

    return h_response





def expand_sections(url_path, sections_dict=None):

    panel_group = None
    panel_template = None
    config_uom = md.CONFIG_UOM

    if url_path == 'minds':
        sections_dict = mc.read_minder_settings(minds.recollect())
        panel_group = md.minds_panel_group
        panel_template = md.minds_panel

    if url_path == 'settings':
        sections_dict = mc.read_minder_settings(mc.minderconfig())
        panel_group = md.panel_group
        panel_template = md.settings_panel

    fo = Template(md.form_select_options)
    fi = Template(md.form_item['text'])
    ft = Template(md.form_group)
    st = Template(panel_template)
    pt = Template(panel_group)
    final_html = ""
    section_html = ""
    panel_id = -1

    for section in sections_dict['sections']:
        panel_id = panel_id + 1
        form_builder = {
                        "title": url_path,
                        "section": section['name'],
                        "form_groups": "",
                        "panel_id": panel_id
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

    final_html += pt.substitute({'title': url_path, 'panels': section_html})

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
    f_response = None
    file_path = os.path.join(WEBROOT + file_name)
    if os.path.isfile(file_path):
        with open(file_path, "rb") as read_handle:
            http_body = read_handle.read()
            f_response = {
                          'code': 200,
                          'type': mimetypes.guess_type(file_name)[0],
                          'body': http_body
                          }

    else:
        f_response = {
              'code': 404,
              'type': 'text/html',
              'body': md.html_404
              }

    return f_response


class MinderWebApp(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    Main Web server class utilizing BaseHTTPServer.BaseHTTPRequestHandler.
    Server starts with no additional parameters and will close with Ctr+C from the command line.
    Parameters: D = {'code': int(HTTP Status code), 'type': str(Mime Type), 'body': str(HTTP body)
    }
    """

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


    def do_GET(self):
        raw_path = urllib.unquote(self.path)
        p = urlparse(raw_path)


        try:
            if p.path.strip('/') in md.WEB_PAGES:
                u = p._replace(path=p.path.strip('/'))
                h = route_request(u)
                self.send_response(h['code'])
                self.send_header("Content-type", h['type'])
                self.end_headers()
                self.wfile.write(h['body'])

            else:
                f = get_file(p.path)
                self.send_response(f['code'])
                self.send_header("Content-type", f['type'])
                self.end_headers()
                self.wfile.write(f['body'])

        except (IOError):
            self.send_response(404)
            self.send_header("Content-type", 0)
            self.end_headers()


    def do_POST(self):
        raw_path = urllib.unquote(self.path)
        u = urlparse(raw_path)

        try:
            url_path = urllib.unquote(self.path)
            content_length = int(self.headers.getheader('content-length'))
            post_body = self.rfile.read(content_length)
            print "!!! POST BODY - %s" % post_body
            post_params = post_body.split('&')
            param_dict = {}
            p_section = None

            for i in post_params:
                parsed_i = urllib.unquote(i)
                parsed_i = parsed_i.replace('+', ' ')
                param_dict[parsed_i.split('=')[0]] = parsed_i.split('=')[1]

            print url_path, param_dict

            if param_dict.has_key('section'):
                p_section = {param_dict.pop('section'): param_dict}

            if param_dict.has_key('delete'):
                p_section = {'delete': param_dict['delete']}

            if url_path == '/minds.html':
                minds.recollect(p_section)
                #time.sleep(1)
                m = get_template(url_path.strip('/'))
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(m)

            if url_path == '/settings.html':
                mc.minderconfig(p_section, update=True)
                #time.sleep(1)
                h = get_template(url_path.strip('/'))
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(h)

        except:
            raise


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MinderWebApp)
    #print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    #print 'Setting Web root directory - %s' % WEBROOT

    webbrowser.open("http://localhost:8051/home", new=0)
    d_pid = None
    try:
        m_daemon = [sys.executable, os.path.join(CUR_DIR, 'minder_daemon.py')]
        if mc.SYSTEM.startswith('win'):
            d_pid = subprocess.Popen(m_daemon, shell=True)
        else:
            d_pid = subprocess.Popen(m_daemon)

        #print 'Firing up the MINDER DAEMON...'

        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'Are you sure you want to close Minder? y/n'
        answer =''
        while (answer != 'y') & (answer != 'n'):
            answer = raw_input()
            #print answer
        if answer == 'y':
            d_pid.kill()
            exit(0)

    httpd.server_close()
    #print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
