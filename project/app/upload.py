from flask import Blueprint, render_template, request, redirect, url_for

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    return "Upload Page"  # Replace with actual logic
