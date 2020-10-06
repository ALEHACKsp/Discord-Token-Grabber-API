from flask import Blueprint

routes = Blueprint('routes', __name__)

# import here
from .token_grabber import *
