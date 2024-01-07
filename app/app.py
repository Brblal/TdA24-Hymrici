# -*- coding: utf-8 -*-
import codecs
import os
import json
from flask import Flask, render_template, request, jsonify
from . import db


app = Flask(__name__)

app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)
app.jinja_env.default_encoding = 'utf-8'

def load_json_data(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        data = json.load(file)
        # Explicitly encode string values to UTF-8
        if isinstance(data, dict):
            data = {k: v.encode('utf-8').decode('utf-8') if isinstance(v, str) else v for k, v in data.items()}
        return data

@app.route('/')
def index():
    # Load JSON data from the 'lecturer.json' file
    data = load_json_data('data/lecturer.json')
    return render_template('lecturer.html', data=data)


if __name__ == '__main__':
    app.run()
