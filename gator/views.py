from flask import render_template
from gator import gator

@gator.route('/')
def index():
    return render_template('index.html')
