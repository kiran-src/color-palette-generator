from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import numpy as np
import urllib.request as ur
from scipy import misc
from PIL import Image
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
Bootstrap(app)


class ImageColours:
    def __init__(self, url):
        self.url = url
        ext = self.url.split('.')[-1]
        ur.urlretrieve(self.url, "aaa."+ext)
        self.image = Image.open("aaa."+ext)
        self.img_array = np.array(self.image)

    def retrieve_results(self):
        return ['']


image_results = ''


class UploadImageForm(FlaskForm):
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit Image")


@app.route('/', methods=['POST', 'GET'])
def home():
    form = UploadImageForm()
    if form.validate_on_submit():
        global image_results
        image_obj = ImageColours(form.img_url.data)
        image_obj.retrieve_image()
        image_results = image_obj.retrieve_results()
        return redirect(url_for("results"))
    return render_template("index.html", form=form)


@app.route('/results')
def results():

    return render_template("results.html", results=image_results)

image_obj = ImageColours("https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/UO_KnightLibrary_Front.jpg/800px-UO_KnightLibrary_Front.jpg")
image_obj.retrieve_results()


if __name__ == "__main__":
    app.run(port=5000, debug=True)