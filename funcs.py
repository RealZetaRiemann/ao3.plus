""" Helper functions for ao3graph.com """
import random
import base64
import io
from wordcloud import WordCloud, STOPWORDS
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

def custom_colours(*args, **kwargs):
    """ Creates and returns a custom color palette to be used in wordcloud_from_dict """
    return "hsl(10, 100%, {}%)".format(random.randint(0, 50))

def wordcloud_from_dict(wcdict):
    """ Renders and returns a wordcloud image with the given dictionary """
    cloud=WordCloud(width=800, height=400, relative_scaling=0, background_color='white',
    color_func=custom_colours, stopwords=STOPWORDS).generate_from_frequencies(wcdict).to_image()
    img = io.BytesIO()
    cloud.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64

class ContactForm(FlaskForm):
    """ Flask Contact Form """
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")
