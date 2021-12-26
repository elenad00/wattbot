### wattbot.com v1
from flask import Flask, render_template, request
from static.scripts.signin import signin
from static.scripts.signup import signup
from static.scripts.analytic import runanalytic
app = Flask(__name__)

app.route('/', methods = ['GET', 'POST'])
def index():
    if not request.cookies.get('user'):
        return redirect(url_for('signin'))
    if request.method =='GET':
        return render_template('index.html')
    elif request.method == 'POST':
        runanalytic()

app.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request.method =='GET':
        return render_template('signin.html')
    elif request.method == 'POST':
        signin()

app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method =='GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        signup()


if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
