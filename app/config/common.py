from flask import render_template, redirect, request, Response, session, url_for, flash, Flask, jsonify, Blueprint
#from flask_mysqldb import MySQL
import mysql.connector
import re
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os
from decouple import config

