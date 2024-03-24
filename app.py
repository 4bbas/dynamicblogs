from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

from datetime import datetime
from time import time
import re

from config import Config
from posts.blueprint import posts

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(posts, url_prefix='/blog')

class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)

def slugify(s):
  pattern = r'[^\w+]'
  return re.sub(pattern, '-', s)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(140), nullable=False)
  slug = db.Column(db.String(140), unique=True)
  body = db.Column(db.Text)
  created = db.Column(db.DateTime, default=datetime.now())
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.generate_slug()
    
  def generate_slug(self):
    if self.title:
      self.slug = slugify(self.title)
    else:
      self.slug = str(int(time())) 

  def __raper__(self):
    return f'<Post id:{self.id}, title:{self.title}' + self.body + '>'
  
#db.init_app(app)