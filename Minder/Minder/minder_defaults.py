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
          <a class="navbar-brand" href="#">Minder</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            ${navbar_active}
          </ul>
        </div><!--/.nav-collapse -->
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
    <div class="col-sm-4 input-group">
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

minds = """
<legend>${section}</legend>
<p>This is the minds page.</p>
	<ol class="tree">
		<li class="tree">
			<label for="folder2">Folder 2</label> <input type="checkbox" id="folder2" />
			<ol>
				<li class="file"><a href="">File 1</a></li>
				<li class="tree">
					<label for="subfolder2"><a href="minds?root=subfolder2">Subfolder 1</a></label> <input type="checkbox" id="subfolder1" />
					<ol>
						<li class="file"><a href="">Subfile 1</a></li>
						<li class="file"><a href="">Subfile 2</a></li>
						<li class="file"><a href="">Subfile 3</a></li>
					</ol>
				</li>
			</ol>
		</li>
	</ol>
"""

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

mind = """{
    "/home/harlanaubuchon/x": {
        "minded_datetime": "2014-05-01T22:21:08.570Z",
        "x": {
            ".mind": {},
            "x1.txt": {
                "file_size": 0,
                "md5_sum": "d41d8cd98f00b204e9800998ecf8427e",
                "mime_type": [
                    "text",
                    "plain"
                ]
            },
            "x2.txt": {
                "file_size": 0,
                "md5_sum": "d41d8cd98f00b204e9800998ecf8427e",
                "mime_type": [
                    "text",
                    "plain"
                ]
            },
            "y1": {
                "y1.txt": {
                    "file_size": 0,
                    "md5_sum": "d41d8cd98f00b204e9800998ecf8427e",
                    "mime_type": [
                        "text",
                        "plain"
                    ]
                },
                "y2.txt": {
                    "file_size": 0,
                    "md5_sum": "d41d8cd98f00b204e9800998ecf8427e",
                    "mime_type": [
                        "text",
                        "plain"
                    ]
                }
            },
            "y2": {
                "y3.txt": {
                    "file_size": 0,
                    "md5_sum": "d41d8cd98f00b204e9800998ecf8427e",
                    "mime_type": [
                        "text",
                        "plain"
                    ]
                },
                "y4.txt": {
                    "file_size": 0,
                    "md5_sum": "d41d8cd98f00b204e9800998ecf8427e",
                    "mime_type": [
                        "text",
                        "plain"
                    ]
                }
            }
        }
    }
}"""