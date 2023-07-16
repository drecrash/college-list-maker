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


class MainForm(FlaskForm):
    gpa = StringField(validators=[InputRequired(), Length(min=1, max=2000)], render_kw={"placeholder": "GPA (4.0 Scale)"})
    optional = StringField(validators=[InputRequired(), Length(min=1, max=1)], render_kw={"placeholder": "T/F"})
    act_score = StringField(validators=[Length(min=0, max=2)], render_kw={"placeholder": "ACT Score (Optional)"})
    sat_score = StringField(validators=[Length(min=0, max=4)], render_kw={"placeholder": "SAT Score (Optional)"})
    income = StringField(validators=[InputRequired(), Length(min=3, max=8)], render_kw={"placeholder": "Income (Plain Integer)"})
    essay = StringField(validators=[InputRequired(), Length(min=1, max=1)], render_kw={"placeholder": "Essay Writing Skills (1-5)"})
    extracurriculars = StringField(validators=[InputRequired(), Length(min=4, max=2000)], render_kw={"placeholder": "Write your extracurriculars, separated by commas", "id": "ec-search"})



    submit = SubmitField("Submit")