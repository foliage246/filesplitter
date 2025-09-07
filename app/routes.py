from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import pandas as pd
import zipfile
from datetime import datetime
from . import db
from .models import User, Usage

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_usage_limit():
    today = datetime.utcnow().date()
    usage = Usage.query.filter_by(user_id=current_user.id, date=today).first()
    if current_user.is_premium:
        limit = 100
    else:
        limit = 5
    if usage:
        return usage.count < limit
    return True

def check_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if current_user.is_premium:
        return size <= 100 * 1024 * 1024  # 100MB
    else:
        return size <= 10 * 1024 * 1024  # 10MB

def increment_usage():
    today = datetime.utcnow().date()
    usage = Usage.query.filter_by(user_id=current_user.id, date=today).first()
    if usage:
        usage.count += 1
    else:
        new_usage = Usage(user_id=current_user.id, count=1)
        db.session.add(new_usage)
    db.session.commit()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if not check_usage_limit():
            flash('Daily usage limit reached')
            return redirect(url_for('main.upload'))

        file = request.files['file']
        column = request.form.get('column')

        if file and allowed_file(file.filename):
            if not check_file_size(file):
                flash('File size exceeds limit')
                return redirect(url_for('main.upload'))

            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process file
            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                elif filename.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(filepath)
                elif filename.endswith('.txt'):
                    df = pd.read_csv(filepath, sep='\t')

                if column not in df.columns:
                    flash('Column not found in file')
                    return redirect(url_for('main.upload'))

                # Split by column
                groups = df.groupby(column)
                zip_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], f'split_{filename.rsplit(".", 1)[0]}.zip')

                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for name, group in groups:
                        split_filename = f'{name}_{filename}'
                        split_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], split_filename)
                        if filename.endswith('.csv'):
                            group.to_csv(split_path, index=False)
                        elif filename.endswith(('.xlsx', '.xls')):
                            group.to_excel(split_path, index=False)
                        elif filename.endswith('.txt'):
                            group.to_csv(split_path, sep='\t', index=False)
                        zipf.write(split_path, split_filename)
                        os.remove(split_path)

                increment_usage()
                return send_file(zip_path, as_attachment=True)

            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(url_for('main.upload'))

    return render_template('upload.html')

@main.route('/terms')
def terms():
    return render_template('terms.html')

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')