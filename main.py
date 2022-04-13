from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
import numpy
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
Bootstrap(app)


class UploadImageForm(FlaskForm):
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit Image")


@app.route('/', methods=['POST', 'GET'])
def home():
    form = UploadImageForm()
    if form.validate_on_submit():
        return redirect(url_for("results"))
    return render_template("index.html", form=form)

@app.route('/results')
def results():
    results = ''
    return render_template("results.html", results=results)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
