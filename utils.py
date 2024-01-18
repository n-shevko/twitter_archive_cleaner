HTML_TEMPLATE = """\
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="{pico_folder}/pico.min.css">
     <style> 
  *:not(pre):not(code):not(.font-monospace) {
    font-family: Ubuntu, sans-serif!important;
  }
  </style>
    <title>Twitter archive: {period}</title>
</head>
<body>
    <main class="container">
    {main}
    </main>
</body>
</html>"""