# -*- coding: utf-8 -*-
__author__ = 'harlanaubuchon'

DEFAULT_CONFIG = {
                     "defaults": {
                         "space_remaining_threshold_bytes": 2048,
                         "text_difference_threshold_percentage": 99,
                         "file_size_limit_in_kilobytes": 300000,
                         },
                     "minds": {}
                     }

# parameters: [title (String), navbar_active[key], main_container(content)]
main_template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" type="image/png" href="../images/py.png" />

    <title>${title}</title>

    <!-- Bootstrap core CSS -->
    <link href="../css/bootstrap.min.css" rel="stylesheet">
    <link href="../css/bootstrap.override.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link rel="stylesheet" type="text/css" href="./css/css-ninja-styles.css" media="screen">
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
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/index.html">Minder</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            ${navbar_active}
          </ul>
        </div><!--/.nav-collapse -->
        ${breadcrumbs}
      </div>
      <div class="container theme-showcase" role="main">
        ${main_container}
      </div> <!-- /container -->
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="../js/bootstrap.min.js"></script>
  </body>
</html>
"""
# Provide key
navbar_active = {"minds": """
            <li><a href="index.html">Home</a></li>
            <li class="active"><a href="minds.html">.Minds</a></li>
            <li><a href="remotes.html">Remotes</a></li>
            <li><a href="settings.html">Settings</a></li>
            """,
                 "settings": """
            <li><a href="index.html">Home</a></li>
            <li><a href="minds.html">.Minds</a></li>
            <li><a href="remotes.html">Remotes</a></li>
            <li class="active"><a href="settings.html">Settings</a></li>
            """,
                 "remotes": """
            <li><a href="index.html">Home</a></li>
            <li><a href="minds.html">.Minds</a></li>
            <li class="active"><a href="remotes.html">Remotes</a></li>
            <li><a href="settings.html">Settings</a></li>
            """,
                 "index": """
            <li class="active"><a href="index.html">Home</a></li>
            <li><a href="minds.html">.Minds</a></li>
            <li><a href="remotes.html">Remotes</a></li>
            <li><a href="settings.html">Settings</a></li>
            """}

# Expects dictionary with array of values (section, key, type as [text, number], value)
settings = """
<form class="form-horizontal" method="POST" id="form">
 <fieldset>
 <legend>${section}</legend>
  ${form_groups}
  <div class="form-actions">
     <button class="btn btn-primary" type="submit">Save</button>
  </div>
 </fieldset>
</form>
<br>
"""

form_group = """
<div class="form-group">
    <label for="${type}" class="col-sm-4 control-label">${label}</label>
    <div class="col-sm-6 input-group">
        <input type="${type}" class="form-control" id="${type}" name="${key}" placeholder="${value}">
        <span class="input-group-addon">${uom}</span>
    </div>
</div>
"""

# Parameters: None
index = """
<div class="container">
  <div class="jumbotron">
    <h1>.Minder</h1>
    <p>Welcome to Minder! Click Start to begin</p>
    <p>
      <a class="btn btn-lg btn-primary" href="/minds.html" role="button">Start Minder &raquo;</a>
    </p>
  </div>
</div> <!-- /container -->
"""

# Expects dictionary with array of values (section, key, type as [text, number], value)
remotes = """
<legend>${section}</legend>
<p>This is the remotes page.</p>
"""

minds = """<legend>Minds</legend>
<p>Choose a folder to Mind.</p>
    <ol class="tree">
        ${folders_template}
    </ol>"""

begin_folders_template = """
        <li class="tree">
            <label for="${name}"><a href="minds?root=${root}/${name}">${name}</a></label><input type="checkbox" id="${name}"/>
            <ol>
"""

files_template = """<li class="file"><span class="filename">${name}</span><span class="file">${size} bytes</span><span class="file">${mime_type}</span></li>\n            """

end_folders_template = """
            ${file_html}
            </ol>
        </li>
"""

empty_files_template = """<li class="file"><span class="empty">(empty)</span></li>"""

config = """{
    "config": [
        {"section":
            {
            "name": "Settings",
            "items": [
                {
                "key": "text_difference_threshold_percentage",
                "value": "99",
                "type": "number",
                "label": "Text Difference Threshold",
                "uom": "percentage"
                },
                {
                "key": "space_remaining_threshold_bytes",
                "value": "2048",
                "type": "number",
                "label": "Space Remaining Threshold",
                "uom": "bytes"
                },
                {
                "key": "file_dif_size_limit_kilobytes",
                "value": "300000",
                "type": "number",
                "label": "File Diff Size Limit",
                "uom": "kilobytes"
                }
            ]
          }
        },
        {"section":
            {
            "name": "minds",
            "items": [
                {"key": "this_is_a_name",
                 "value": "/path/to/something",
                 "type": "text",
                 "label": "This Is A Name",
                 "file_types": "(text, pdf, doc, docx)",
                 "uom": null
                 },
                 {"key": "this_is_another_name",
                 "value": "/path/to/something/else",
                 "type": "text",
                 "label": "This Is Another Name",
                 "file_types": "(mp3, mp4, wav)",
                 "uom": null
                 }
            ]
        }
      }
    ]
}"""

mind_old = {
    "root": "/home/harlanaubuchon/",
    "name": "x",
    "files": [],
    "folders": [
                {
                 "root": "/home/harlanaubuchon/x/",
                 "name": "y1",
                 "folders": [
                             {
                             "root": "/home/harlanaubuchon/x/y1/",
                             "name": "y1_2",
                             "folders": [],
                             "files": []
                             }
                             ],
                 "files": [
                           {
                           "name": "y0.txt",
                           "mime_type": "text/plain",
                           "size": 100,
                           "checksum": "c873loihagkjhsdo8y98wqyeshdlkahs"
                           },
                           {
                           "name": "y1.txt",
                           "mime_type": "text/plain",
                           "size": 99,
                           "checksum": "b873loihagkjhsdo8y98wqyeshdlkahs"
                           },
                           {
                           "name": "y2.txt",
                           "mime_type": "text/plain",
                           "size": 98,
                           "checksum": "a873loihagkjhsdo8y98wqyeshdlkahs"
                           }
                           ]
                 },
                {
                 "root": "/home/harlanaubuchon/x/",
                 "name": "y2",
                 "folders": [
                            {
                             "root": "/home/harlanaubuchon/x/y2/",
                             "name": "y2_1",
                             "folders": [],
                             "files": [
                                       {
                                       "name": "y3.txt",
                                       "mime_type": "text/plain",
                                       "size": 97,
                                       "checksum": "d873loihagkjhsdo8y98wqyeshdlkahs"
                                       },
                                       {
                                       "name": "y4.txt",
                                       "mime_type": "text/plain",
                                       "size": 96,
                                       "checksum": "e873loihagkjhsdo8y98wqyeshdlkahs"
                                       }
                                       ]
                             }
                            ],
                 "files": [
                           {
                           "name": "y5.txt",
                           "mime_type": "text/plain",
                           "size": 95,
                           "checksum": "f873loihagkjhsdo8y98wqyeshdlkahs"
                           },
                           {
                           "name": "y6.txt",
                           "mime_type": "text/plain",
                           "size": 94,
                           "checksum": "g873loihagkjhsdo8y98wqyeshdlkahs"
                           }
                           ]
                 }
                ]
    }

breadcrumbs = """
      <ol class="breadcrumb">
          ${breadcrumb_list}
      </ol>
"""

breadcrumb_refs = """
          <li><a href="/minds?root=/${path}">${name}</a></li>
"""

breadcrumb_active = """
          <li class="active">${name}</li>
"""

breadcrumb_list = """
      <ol class="breadcrumb">

          <li><a href="/minds?root=/home">home</a></li>

          <li><a href="/minds?root=/home/harlanaubuchon">harlanaubuchon</a></li>

          <li class="active">x</li>

      </ol>"""

mind = {
    "files": [],
    "folders": [
        {
            "files": [
                {
                    "checksum": "17748a55c79f5fd63906a3b72fdb33db",
                    "mime_type": [
                        "text",
                        "plain"
                    ],
                    "name": "y0.txt",
                    "size": 24
                },
                {
                    "checksum": "6fe05d420e64dfde21fb80e021012725",
                    "mime_type": [
                        "text",
                        "plain"
                    ],
                    "name": "y1.txt",
                    "size": 48
                },
                {
                    "checksum": "f2c84ca801223da9af918e673231a170",
                    "mime_type": [
                        "text",
                        "plain"
                    ],
                    "name": "y2.txt",
                    "size": 72
                }
            ],
            "folders": [
                {
                    "files": [],
                    "folders": [],
                    "name": "y1_2",
                    "root": "/home/harlanaubuchon/z/x/y1"
                }
            ],
            "name": "y1",
            "root": "/home/harlanaubuchon/z/x"
        },
        {
            "files": [
                {
                    "checksum": "ec0cbaa49d8ea0411ecf406385789c08",
                    "mime_type": [
                        "text",
                        "plain"
                    ],
                    "name": "y6.txt",
                    "size": 162
                },
                {
                    "checksum": "d9857ed821a1ae0006dcb0e06f406759",
                    "mime_type": [
                        "text",
                        "plain"
                    ],
                    "name": "y5.txt",
                    "size": 139
                }
            ],
            "folders": [
                {
                    "files": [
                        {
                            "checksum": "da6131d255860149f51a5730b7f69d0a",
                            "mime_type": [
                                "text",
                                "plain"
                            ],
                            "name": "y3.txt",
                            "size": 93
                        },
                        {
                            "checksum": "ad4f5dd9e86d927d55a3dc037fbf91cf",
                            "mime_type": [
                                "text",
                                "plain"
                            ],
                            "name": "y4.txt",
                            "size": 116
                        }
                    ],
                    "folders": [],
                    "name": "y2_1",
                    "root": "/home/harlanaubuchon/z/x/y2"
                }
            ],
            "name": "y2",
            "root": "/home/harlanaubuchon/z/x"
        }
    ],
    "name": "x",
    "root": "/home/harlanaubuchon/z"
}