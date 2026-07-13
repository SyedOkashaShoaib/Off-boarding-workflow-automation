from flask import Blueprint
from flask import render_template, redirect, url_for


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return redirect (url_for('cases.create_case'))