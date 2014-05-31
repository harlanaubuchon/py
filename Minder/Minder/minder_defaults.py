# -*- coding: utf-8 -*-
__author__ = 'harlanaubuchon'

DEFAULT_CONFIG = {
    "Settings": {
        "space_remaining_threshold_bytes": 2048,
        "text_difference_threshold_percentage": 99,
        "file_size_limit_kilobytes": 300000,
        "mind_time_minutes": 1
    },
    "System": {
        "show_hidden_files_boolean": False,
        "ignored_directories_list": 'AppData, Application Data, Cookies, Local Settings',
        "directory_listing_depth_number": 1
    }
}

CONFIG_UOM = {
    "percentage": {"uom": "%", "type": "number"},
    "bytes": {"uom": "B", "type": "number"},
    "kilobytes": {"uom": "KB", "type": "number"},
    "boolean": {"uom": None, "type": "select", "options": ['True', 'False']},
    "number": {"uom": None, "type": "number"},
    "text": {"uom": None, "type": "text"},
    "list": {"uom": None, "type": "text"},
}

WEB_PAGES = ['minds', 'folders', 'remotes', 'settings', 'home', 'index']
WEB_FILES = ['html', 'css', 'js', 'eot', 'svg', 'ttf', 'woff', 'png']

# parameters: [title (String), navbar_active[key], main_container(content)]
main_template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Minder Is Not a DVCS Enhanced Repository">
    <meta name="author" content="Harlan AuBuchon - https://github.com/harlanaubuchon">
    <link rel="shortcut icon" type="image/png" href="../images/py.png" />

    <title>${title}</title>

    <!-- Bootstrap core CSS -->
    <link href="../css/bootstrap.min.css" rel="stylesheet">
    <link href="../css/bootstrap.override.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link rel="stylesheet" type="text/css" href="../css/css-ninja-styles.css" media="screen">
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
    <!--<link href="navbar-fixed-top.css" rel="stylesheet">-->

    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <!-- Fixed navbar -->
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="glyphicon glyphicon-th-large" style="color:#fff"></span>
          </button>
          <button type="button" class="btn btn-harlan btn-lg">
            <span class="glyphicon glyphicon-eye-open"></span> Minder
          </button>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            ${navbar_active}
          </ul>
        </div><!--/.nav-collapse -->
        ${breadcrumbs}
      </div>

        ${main_container}

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="../js/bootstrap.min.js"></script>
	<script src="../js/minder.js"></script>  
  </body>
</html>
"""


# Provide key
navbar_active = {"minds": """
            <li><a href="home">Home</a></li>
            <li class="active"><a href="minds">.Minds</a></li>
            <li><a href="remotes">Remotes</a></li>
            <li><a href="settings">Settings</a></li>
            """,
                 "folders": """
            <li><a href="home">Home</a></li>
            <li class="active"><a href="minds">.Minds</a></li>
            <li><a href="remotes">Remotes</a></li>
            <li><a href="settings">Settings</a></li>
            """,
                 "settings": """
            <li><a href="home">Home</a></li>
            <li><a href="minds">.Minds</a></li>
            <li><a href="remotes">Remotes</a></li>
            <li class="active"><a href="settings">Settings</a></li>
            """,
                 "remotes": """
            <li><a href="home">Home</a></li>
            <li><a href="minds">.Minds</a></li>
            <li class="active"><a href="remotes">Remotes</a></li>
            <li><a href="settings">Settings</a></li>
            """,
                 "home": """
            <li class="active"><a href="home">Home</a></li>
            <li><a href="minds">.Minds</a></li>
            <li><a href="remotes">Remotes</a></li>
            <li><a href="settings">Settings</a></li>
            """}

panel_group = """
<div class="container theme-showcase" role="main">
    <div class="row clearfix">
        <div class="col-md-12 column">
            <div class="panel-group" id="panel-${title}">

                ${panels}

            </div>
        </div>
    </div>
</div><!-- container -->
"""

minds_panel = """
                <div class="panel panel-default">
                    <div class="panel-heading">
                         <a class="panel-title" data-toggle="collapse" data-parent="#panel-${title}" href="#panel-element-${panel_id}">${section}</a>
                    </div>
                    <div id="panel-element-${panel_id}" class="panel-collapse collapse">
                        <div class="panel-body">


                            <form class="form-horizontal" method="POST" id="${section}" name="${section}">
                             <fieldset>

                                ${form_groups}

                                <div class="form-group">
                                    <div class="col-sm-6 input-group">
                                        <button class="btn btn-primary" type="submit" name="section" value="${section}">Update</button>
                                        <button class="btn btn-danger btn-xs" type="submit" name="delete" value="${section}">Forget</button>
                                    </div>
                                </div>
                             </fieldset>
                            </form>


                        </div>
                    </div>
                </div>
"""

settings_panel = """
                <div class="panel panel-default">
                    <div class="panel-heading">
                         <a class="panel-title" data-toggle="collapse" data-parent="#panel-${title}" href="#panel-element-${panel_id}">${section}</a>
                    </div>
                    <div id="panel-element-${panel_id}" class="panel-collapse collapse">
                        <div class="panel-body">


                            <form class="form-horizontal" method="POST" id="${section}" name="${section}">
                             <fieldset>

                                ${form_groups}

                                <div class="form-group">
                                    <div class="col-sm-6 input-group">
                                         <button class="btn btn-primary" type="submit" name="section" value="${section}">Save</button>
                                    </div>
                                </div>
                             </fieldset>
                            </form>


                        </div>
                    </div>
                </div>
"""

form_group = """
                                <div class="form-group">
                                    <label for="${type}" class="col-sm-4 control-label">${label}</label>
                                    <div class="col-sm-6 input-group">

                                        ${form_items}

                                    </div>
                                </div>
"""

form_item = {"select": """<select class="form-control" type="${type}" id="${type}" name="${key}" value="${value}">${select_options}</select>""",
             "text": """<input type="${type}" class="form-control" id="${type}" name="${key}" value="${value}">""",
             "number": """<input type="${type}" class="form-control" id="${type}" name="${key}" value="${value}">""",
             "uom": """<span class="input-group-addon">${uom}</span>"""
             }

form_select_options = """<option value="${option}"${selected}>${option}</option>"""

home = """
<div class="container">
  <div class="jumbotron">
    <h1>.Minder</h1>
    <p>Welcome to Minder! Click Start to begin</p>
    <p>
      <a class="btn btn-lg btn-primary" href="/minds" role="button">Start Minder &raquo;</a>
    </p>
  </div>
</div> <!-- /container -->
"""

minds = """
<div class="container theme-showcase" role="main">

<legend>Remotes</legend>
    <ol class="tree">
        ${folders_template}
    </ol>

</div> <!-- /container -->
    """

folders = """
    <ol class="tree" id="folders">
        ${folders_template}
    </ol>
   """

begin_folders_template = """
        <li class="tree">
            <label for="${name}"><a id="origin" href="folders?root=${url}">${name}</a></label><input type="checkbox" id="${name}"/>
            <ol>
"""

files_template = """<li class="file"><span class="filename">${name}</span><span class="file">${size} bytes</span><span class="file">${mime_type}</span></li>\n            """

end_folders_template = """
            ${file_html}
            </ol>
        </li>
"""

empty_files_template = """<li class="file"><span class="empty">(empty)</span></li>"""


breadcrumbs = """
      <ol class="breadcrumb">
          ${breadcrumb_list}
      </ol>
"""

breadcrumb_refs = """
          <li><a href="/remotes?root=${path}">${name}</a></li>
"""

breadcrumb_active = """
          <li class="active">${name}</li>
"""

breadcrumb_list = """
      <ol class="breadcrumb">

          <li><a href="/remotes?root=/home">home</a></li>

          <li><a href="/remotes?root=/home/harlanaubuchon">harlanaubuchon</a></li>

          <li class="active">x</li>

      </ol>"""

form_alert = """
<div class="alert alert-danger alert-dismissable">
    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
    <h4>
        I'm terribly sorry, I can't do that for you...
    </h4>
    <strong>Error</strong> - Please ensure all fields are filled correctly and try again.
</div>
"""

minds_panel_group = """
       <div class="container theme-showcase" role="main">
            <div class="row clearfix">

                <div class="col-md-12 column">
                    <div class="panel-group" id="panel-minds">

                        <div class="panel panel-default">
                            <div class="panel-heading">
                                 <a class="panel-title" data-toggle="collapse" data-parent="#panel-minds" href="#panel-element-new_mind">New Mind</a>
                            </div>
                            <div id="panel-element-new_mind" class="panel-collapse collapse">
                                <div class="panel-body">


                                    <form class="form-horizontal" method="POST" id="new_mind">
                                        <fieldset>
                                            <div class="row clearfix">
                                                <div class="col-md-6 column">
                                                    <div class="row clearfix">
                                                        <h4>
                                                            Step 1: &nbsp;&nbsp;Choose a folder for Minder to mind below.
                                                        </h4>
                                                        <div class="form-group">
                                                            <label for="origintext" class="col-sm-2 control-label">Origin</label>
                                                            <div class="col-sm-8 input-group">
                                                                <input type="text" class="form-control" id="origintext" name="origin" value="">
                                                            </div>
                                                        </div>

                                                        <a id="origin" href="folders">Click here to browse folders.</a>
                                                        <div id="originfolder"></div>

                                                    </div>
                                                    <div class="row clearfix">
                                                        <h4>
                                                        Step 2: &nbsp;&nbsp;Choose a folder for Minder to move your files to.
                                                        </h4>
                                                        <div class="form-group">
                                                            <label for="text" class="col-sm-2 control-label">Destination</label>
                                                            <div class="col-sm-8 input-group">
                                                                <input type="text" class="form-control" id="text" name="destination" value="">
                                                            </div>
                                                        </div>

                                                        <a id="destination" href="folders">Click here to browse folders.</a>
                                                        <div id="destinationfolder"></div>

                                                    </div>
                                                </div>
                                                <div class="col-md-6 column">
                                                    <h4>
                                                    Step 3: &nbsp;&nbsp;Choose a Name for your new Mind.
                                                    </h4>
                                                    <form class="form-horizontal" role="form">
                                                        <div class="form-group">
                                                            <label for="text" class="col-sm-4 control-label">Name of Mind</label>
                                                            <div class="col-sm-6 input-group">
                                                                <input type="text" class="form-control" id="text" name="name_of_mind" value="">
                                                                <span class="help-block">Name containing no spaces and no special characters</span>
                                                            </div>
                                                        </div>
                                                        <h4>
                                                            Step 4: &nbsp;&nbsp;Enter one or more files extensions to Mind.
                                                        </h4>
                                                        <div class="form-group">
                                                            <label for="text" class="col-sm-4 control-label">File Extensions</label>
                                                            <div class="col-sm-6 input-group">
                                                                <input type="text" class="form-control" id="text" name="file_extensions_list" value="">
                                                                <span class="help-block">Comma seperated list of file extensions (e.g., .jpg, .png)</span>

                                                            </div>
                                                        </div>
                                                        <div class="form-group">
                                                            <div class="col-md-8">
                                                                <button class="btn btn-primary" type="submit" name="section" value="new_mind">Save</button>
                                                                <button class="btn btn-danger" type="reset" name="section" value="reset">Cancel</button>
                                                            </div>
                                                        </div>
                                                    </form>
                                                </div>
                                            </div>
                                        </fieldset>
                                    </form>
                                </div>
                            </div>
                        </div>

                        ${panels}

                    </div>
                </div>
            </div>
        </div><!-- container -->
        """

html_404 = """
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <meta content="IE=edge" http-equiv="X-UA-Compatible" />
    <meta content="width=device-width, initial-scale=1" name="viewport" />
    <meta content="Minder Is Not a DVCS Enhanced Repository" name="description" />
    <meta content="Harlan AuBuchon - https://github.com/harlanaubuchon" name="author" />
    <link href="../images/py.png" rel="shortcut icon" type="image/png" />

    <title>404</title><!-- Bootstrap core CSS -->
    <link href="../css/bootstrap.min.css" rel="stylesheet" />
    <link href="../css/bootstrap.override.css" rel="stylesheet" /><!-- Custom styles for this template -->
    <link href="../css/css-ninja-styles.css" media="screen" rel="stylesheet" type="text/css" />
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css' /><!--<link href="navbar-fixed-top.css" rel="stylesheet">-->
    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>

<body>
    <!-- Fixed navbar -->

    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="glyphicon glyphicon-th-large" style="color:#fff"></span>
          </button>
          <button type="button" class="btn btn-harlan btn-lg">
            <span class="glyphicon glyphicon-eye-open"></span> Minder
          </button>
        </div>

            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="home">Home</a></li>

                    <li class="active"><a href="minds">.Minds</a></li>

                    <li><a href="remotes">Remotes</a></li>

                    <li><a href="settings">Settings</a></li>
                </ul>
            </div><!--/.nav-collapse -->

            <ol class="breadcrumb">
                <li class="active">June 26, 1969 - Royal Albert Hall</li>
            </ol>
        </div>

        <div class="container">
          <div class="jumbotron">
            <h1>404</h1>
            <h4>Something terrible has happened...</h4>
            <p>
              <a class="btn btn-lg btn-primary" href="/home" role="button">Click here to start over</a>
            </p>
          </div>
        </div> <!-- /container -->
        <!-- Bootstrap core JavaScript
    ================================================== -->
        <!-- Placed at the end of the document so the pages load faster -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
        <script src="../js/bootstrap.min.js"></script>
        <script src="../js/minder.js"></script>
    </div>
</body>
</html>
"""
