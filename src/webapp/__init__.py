#pylint: disable=import-error
from flask import Flask

app = Flask(__name__)

from webapp import routes
from webapp import requests