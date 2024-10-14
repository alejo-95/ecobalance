from flask import render_template, redirect, request, Response, session, url_for, flash, Flask, jsonify, Blueprint
from flask_mysqldb import MySQL
import re