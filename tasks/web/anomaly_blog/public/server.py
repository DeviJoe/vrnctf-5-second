import os
import re
import sqlite3
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

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
if not app.config['DATABASE']:
    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'users.db')


# connection to sqlite database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


# initialization of sqlite database
@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/show_entries')
def show_entries():
    cur = g.db.execute("select username, text from Line where blogname ='" + session['blog'] + "'")
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template("blogs/" + session['blog'] + ".html", entries=entries)


@app.route('/')
def show_blogs():
    session['blog'] = "Blogs"

    cur = g.db.execute('select username, blogname from Blog where username = ? order by id desc',
                       (session.get('name', ""),))
    blogs = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('showblogs.html', blogs=blogs)


@app.route('/add_image', methods=['POST'])
def add_image():
    file = request.files['pic']
    pathfile = os.path.join(os.path.dirname(__file__), "templates/blogs/" + session['blog'] + ".html")
    f = open(pathfile)
    file.save(os.path.join(os.path.dirname(__file__), "static/images/", file.filename))
    str = ""
    for line in f:
        if line.find("<ul class=entries>") != -1:
            str += '<p><img src="static/images/' + file.filename + '"width="auto" height="255"></p>\n'
        str += line

    f.close()
    f = open(pathfile, "w")
    f.write(str)
    f.close()
    return redirect(url_for('show_entries'))


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into Line (username, blogname, text) values (?,?, ?)',
                 [session['name'], session['blog'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/add_blog', methods=['POST'])
def add_blog():
    if not session.get('logged_in'):
        abort(401)
    st = request.form['text']
    st = st.replace("/", "")
    st = st.replace("\\", "")
    st = st.replace(".", "")
    pathfile = os.path.join(os.path.dirname(__file__), "templates/blogs/" + st + ".html")
    f = open(pathfile, 'w')
    f.write('{% extends "./layout.html" %}')
    f.write('''
      {% block body %}
    {% if session.logged_in %}
       {% if session.another==False %}
     <form action="{{ url_for('add_image') }}" method="post" enctype="multipart/form-data">
        <p>Load picture</p>
        <p><input type="file" name="pic" enctype="multipart/form-data"></p>
        <dd><input type=submit value=Load>
     </form>
        {% endif %}
      <form action="{{ url_for('add_entry') }}" method=post class=add-entry>
        <dl>
          <dt>AddEntry:
          <dd><textarea name=text rows=5 cols=40></textarea>
          <dd><input type=submit value=Share>
        </dl>
      </form>
      {% endif %}
      <ul class=entries>
    {% for entry in entries %}
        <li><h2>{{ entry.title }}</h2>{{ entry.text|safe }}
    {% else %}
     <li><em>Unbelievable. No entries here so far</em>
    {% endfor %}
    </ul>
      {% endblock %}''')
    session["blog"] = st
    g.db.execute('insert into Blog (username, blogname) values (?,?)',
                 [session['name'], session['blog']])
    g.db.commit()
    f.close()
    return render_template("blogs/" + st + ".html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cursor = sqlite3.connect(app.config['DATABASE']).cursor()
        _name = request.form['username']
        _password = request.form['password']
        cursor.execute("select username, password from User where username= ? ", (_name,))
        user = cursor.fetchall()

        if user == []:
            error = 'Invalid username'
        elif request.form['password'] != user[0][1]:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['name'] = user[0][0]
            flash('You were logged in')
            return redirect(url_for('show_blogs'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_blogs'))


@app.route('/curblog', methods=['GET', 'POST'])
def curblog():
    st = request.args.get('val', '')
    session["blog"] = st
    cur = g.db.execute("select username, blogname from Blog where blogname ='" + session['blog'] + "'")
    user = cur.fetchone()
    if user[0] != session['name']:
        session['another'] = True
    else:
        session['another'] = False
    return redirect(url_for('show_entries'))


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    # session.pop('logged_in', None)
    if request.method == 'POST':
        # cursor = mysql.connect().cursor()
        cursor = sqlite3.connect(app.config['DATABASE']).cursor()
        _name = request.form['username']
        _password = request.form['password']
        cursor.execute("select * from User where username = ?", (_name,))
        data = cursor.fetchone()
        cursor.close()
        if data is not None or _name == "" or _password == "":
            flash('Username or Password is wrong')
            return render_template('registration.html')
        else:
            flash('Success')
            st = ' INSERT INTO User (username, password) VALUES ( ? ,?)'
            g.db.execute(st, (_name, _password))
            g.db.commit()
            session['logged_in'] = True
            session['name'] = _name
            return redirect(url_for('show_blogs'))
    return render_template('registration.html')


if __name__ == '__main__':
    try:
        with closing(connect_db()) as db:
            with app.open_resource('users.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
    except:
        pass
    app.run(host='0.0.0.0', port=1113, debug=False)
    session.clear()
