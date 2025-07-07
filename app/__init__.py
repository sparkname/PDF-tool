from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import tempfile
from werkzeug.utils import secure_filename
from .converter import DocumentConverter
import uuid
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 确保上传和转换目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)
    
    print(f"上传目录: {app.config['UPLOAD_FOLDER']}")
    print(f"转换目录: {app.config['CONVERTED_FOLDER']}")
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
