'''
Created on 01/08/2015

@author: oblivion
'''
from flask import Flask

app = Flask(__name__)
from app import views
