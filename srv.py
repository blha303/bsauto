#!/usr/bin/env python
from flask import Flask, render_template_string, send_file, request, jsonify
from bandersnatch import bandersnatch
from time import time

TEMPLATE = """
<!doctype html>
<html>
    <head>
        <style>
        body {
          background-color: black;
          color: white;
          font-family: sans-serif
        }
        label {
          background-color: black;
        }
        .segment {
          width:472px;
          height:266px;
        }
        div.segment {
          margin:30px
        }
        video.segment {
        }
        </style>
        <title>Bandersnatch</title>
    </head>
    <body>
        <h3>{{ length }} <a href="?seed={{ seed }}">Share</a></h3>
        <p><a href='https://gist.github.com/blha303/397f724c8e420cbb8023e676c972e052'>How to get segments</a></p>
        <textarea>{% for segment in concat %}
file '{{ segment }}.mkv' {% endfor %}</textarea>
        <div style='display: flex; flex-wrap: wrap;'>
        {% for option in options %}
            <div class='segment' id='{{ option.id }}' style='background-image: url({{ option.url }})'>
                <video class='segment' id='{{ option.id }}-vid' controls poster='{{ option.url }}' preload='none'>
                    <source src='https://s3.home.b303.me/bandersnatch/{{ option.id }}.webm'>
                </video>
                <label for='{{ option.id }}'>{% if option.chose != "No caption (1A)" %}<span class='chose'>Chose {{ option.chose }}</span> &gt;{% endif %} <span class='caption'>{{ option.caption }}</span></label>
            </div>
        {% endfor %}
        </div>
    </body>
</html>
"""

app = Flask(__name__)

@app.route("/json")
@app.route("/json/<seed>")
def as_json(seed=None):
    if not seed:
        seed = int(time())
    if type(seed) is str and seed.isdigit():
        seed = int(seed)
    return jsonify(bandersnatch(seed=seed))

@app.route("/")
def index():
    orig_seed = request.args.get("seed", int(time()))
    if type(orig_seed) is str and orig_seed.isdigit():
        orig_seed = int(orig_seed)
    concat, options, length, seed = bandersnatch(seed=orig_seed)
    return render_template_string(TEMPLATE, concat=concat, options=options, length=length, seed=seed)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=24572)
