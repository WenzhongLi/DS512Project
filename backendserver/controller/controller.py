#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author: li
'''
from backendserver import app
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
import Match_Predict

data = None


@app.route('/index', methods=['GET', 'POST'])
def to_index():
    # data =
    return render_template('index.html')


@app.route('/MatchPredict', methods=['GET', 'POST'])
def to_match_predict():
    return render_template('MatchPredict.html')


@app.route('/test', methods=['GET', 'POST'])
def to_test():
    return render_template('test.html')


@app.route('/backend/get_predict', methods=['POST'])
def get_predict():
    a = request.form.get('a', 'a default value')
    # term1 = request.form.get('term1', 'term1 default value')
    term1 = request.form.getlist('term1[]')
    term2 = request.form.getlist('term2[]')
    # term2 = request.form.get('term2', 'term2 default value')
    formation1 = request.form.getlist('formation1[]')
    formation2 = request.form.getlist('formation2[]')
    t1 = []
    for i in term1:
        t1.append(int(i))
    t2 = []
    for i in term2:
        t2.append(int(i))
    f1 = []
    for i in formation1:
        f1.append(int(i))
    f2 = []
    for i in formation2:
        f2.append(int(i))
    predict = Match_Predict.Predict(t1, t2, f1, f2)
    r = predict.Predict()

    print a, t1, t2, f1, f2
    result = "{\"t1win\" :%s, \"t2win\" :%s,\"draw\" :%s,\"expect1\" :%s,\"expect2\" :%s}"

    # "t1win", t1win, "t2win", t2win, "draw", t1t2even
    return result % (r[0], r[1], r[2], r[3], r[4])
