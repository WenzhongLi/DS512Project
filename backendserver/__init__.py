#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author: li
'''

#init
from flask import Flask
app = Flask(__name__)

from backendserver.controller import controller

