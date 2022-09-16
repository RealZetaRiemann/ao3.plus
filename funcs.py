# This file includes various helper functions for Ao3graph
from wordcloud import WordCloud, STOPWORDS
import base64
import io
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import random

def custom_colours(*args, **kwargs):
    return "hsl(10, 100%%, %d%%)" % random.randint(0, 50)

# Renders and returns a wordcloud image with the given dictionary
def wordcloud_from_dict(dict):
    wc=WordCloud(width=800, height=400, relative_scaling=0, background_color='white', color_func=custom_colours, stopwords=STOPWORDS).generate_from_frequencies(dict).to_image()
    img = io.BytesIO()
    wc.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")