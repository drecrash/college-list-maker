from flask import Flask, render_template, url_for, redirect, request, jsonify, send_file
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import flask_wtf
from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, Optional
from flask_wtf.file import FileAllowed, FileField
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_bcrypt import bcrypt
from flask_migrate import Migrate
import datetime
import random
import paginate
import smtplib, ssl
import json
import os
from urllib.parse import urlparse, parse_qs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pytz
import zipfile
from sqlalchemy import create_engine, text

from app_setup import app, db
from funcs import get_data, get_ec_data, get_importance_data, sort_dict, main
from forms import MainForm

@app.route("/", methods=['GET', 'POST'])
def index():
    form = MainForm()
    importance_data = get_importance_data()
    all_ecs = list(importance_data.keys())
    using_act = False
    using_sat = False
    act_score = 0
    sat_score = 0
    chosen_test = ''

    ec_length = len(all_ecs)

    if form.validate_on_submit():
        if form.optional.data == "F":
            if form.act_score.data:
                using_act = True
                act_score = form.act_score.data
                chosen_test = 'A'
            else:
                using_sat = True
                sat_score = form.sat_score.data
                chosen_test = 'S'

        gpa = form.gpa.data
        income = form.income.data
        essay = form.essay.data
        ecs = form.extracurriculars.data
        ecs = [char for char in ecs]

        if using_act or using_sat:
            test_optional = False
        else:
            test_optional = True

        for i in range(len(ecs)):
            if i == 0:
                continue
            elif ecs[i] == " " and ecs[i-1] == ",":
                ecs[i] = ''

        ecs_fin = ''
        for i in range(len(ecs)):
            ecs_fin += ecs[i]

        ecs = ecs_fin
        
        ecs = ecs.split(',')

        print("caaaa")
        
        #(user_gpa, user_testoptional, chosen_test, user_actscore, user_satscore, user_income, user_essayskills, user_ecs):
        returned_string = main(float(gpa), test_optional, chosen_test, int(act_score), int(sat_score), int(income), int(essay), ecs)

        print(returned_string)

        return returned_string

    else:
        print(form.errors)


    return render_template("listmaker.html", form = form, all_ecs = all_ecs, ec_length = ec_length)

@app.route("/result")
def finalresult(result):
    return result

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80, debug=True)

    
