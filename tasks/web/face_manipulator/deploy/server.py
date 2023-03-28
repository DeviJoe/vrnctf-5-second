import base64
import hashlib
import io
import os
import random

from PIL import Image
from flask import Flask, render_template, request, make_response, session

app = Flask(__name__)

app.secret_key = 'safsglsjoke3iyg8v4thwp[0aejgp9eh'
flag = 'vrnctf{f6ce_f0rens1s_sh3rl0ck}'

real = os.listdir('real')

fake = os.listdir('fake')

real_set = set([hashlib.sha256(("real75474" + name).encode()).hexdigest() for name in real])
fake_set = set([hashlib.sha256(("fake31423" + name).encode()).hexdigest() for name in fake])



def get_image(filepath):
    im = Image.open(filepath)
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    base64_encoded_image = base64.b64encode(img_byte_arr).decode("utf-8")
    return base64_encoded_image


def get_random_image():
    f = random.randint(0, 1)
    i = random.randint(0, 9999)
    if f == 0:
        return os.path.join("fake", fake[i]), hashlib.sha256(("fake31423" + fake[i]).encode()).hexdigest()
    else:
        return os.path.join("real", real[i]), hashlib.sha256(("real75474" + real[i]).encode()).hexdigest()


@app.route('/check/')
def check():
    result = request.args.get('result')
    image = request.args.get('image')
    count = session.get('count')
    fl = ""
    if count is None:
        count = 0
    else:
        count = int(count)
    if result == 'real':
        if image in real_set:
            count += 1
        else:
            count = 0
    else:
        if image in fake_set:
            count += 1
        else:
            count = 0
    if count >= 20:
        fl = flag
    path, name = get_random_image()
    base64_encoded_image = get_image(path)
    resp = make_response(render_template('index.html', myImage=base64_encoded_image, score=count, flag=fl, image=name))
    session['count'] = count
    return resp


@app.route('/')
def hello():
    path, name = get_random_image()
    base64_encoded_image = get_image(path)
    return render_template('index.html', myImage=base64_encoded_image, image=name)


app.run(host='0.0.0.0', port=1112, debug=False)
