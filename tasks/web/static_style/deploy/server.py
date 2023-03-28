import os
import re

from flask import Flask, render_template, session

# create our little application :)
app = Flask(__name__)

config = type('Object', (object,), {})
with open(os.path.join(os.path.dirname(__file__), 'FLASKR_SETTINGS.ini')) as f:
    for str in f:
        key, value, = (re.sub('(^[ \'"\n]*|[ \'"\n]*$)', '', x) for x in str.split('='))
        try:
            value = eval(value)
        except:
            pass
        setattr(config, key, value)
app.config.from_object(config)


@app.route('/')
def hello():
    msg = "There is nothing yet"
    admin = session.get('admin')
    if admin is not None:
        if admin == 1:
            msg = "vrnctf{secr7t_3cp_inf0}"

    else:
        session['admin'] = 0
    return render_template('index.html', msg=msg)


app.run(host='0.0.0.0', port=1120, debug=False)
