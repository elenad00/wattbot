from flask import flask
from main import *
app = Flask(__name__)
@app.route('/')
def home():
    
    return render_template('home.html')
