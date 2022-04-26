from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import numpy as np
import urllib.request as ur
from scipy import misc
from PIL import Image
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, URL
import requests
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = "AAAAAAAAAAAAAAAA"
Bootstrap(app)


class ImageColours:
    def __init__(self, url):
        ext = url.split('.')[-1]
        # ur.urlretrieve(url, "aaa." + ext, headers={'User-agent': 'Mozilla/5.0'})
        r = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open("aaa." + ext, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        image = Image.open("aaa." + ext)
        self.img_array = np.array(image)
        self.colors = self.retrieve_results()

    def retrieve_results(self):
        shape = self.img_array.shape
        colors = {}
        for i in range(shape[0]):
            for j in range(shape[1]):
                key = (self.img_array[i][j][0], self.img_array[i][j][1], self.img_array[i][j][2])
                if key in colors:
                    colors[key] += 1
                else:
                    colors[key] = 1
        return colors

    def topten(self):
        top = [{(0, 0, 0): 0} for i in range(10)]
        for i in self.colors:
            for j in range(10):
                if self.colors[i] > sum(top[j].values()):
                    if j == 9 or self.colors[i] <= sum(top[j + 1].values()):
                        top[j] = {i: self.colors[i]}
                        break
        return [('#%02x%02x%02x' % list(i.keys())[0], sum(i.values())) for i in top]


image_results = ''
url = ''


class UploadImageForm(FlaskForm):
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit Image")


@app.route('/', methods=['POST', 'GET'])
def home():
    form = UploadImageForm()
    if form.validate_on_submit():
        global image_results
        image_obj = ImageColours(form.img_url.data)
        image_results = image_obj.topten()
        global url
        url = form.img_url.data
        return redirect(url_for("results"))
    return render_template("index.html", form=form)


@app.route('/results')
def results():
    return render_template("results.html", results=image_results, url=url)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

