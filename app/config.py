import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'document-converter-secret-key'
    UPLOAD_FOLDER = os.path.abspath(os.environ.get('UPLOAD_FOLDER') or 'uploads')
    CONVERTED_FOLDER = os.path.abspath(os.environ.get('CONVERTED_FOLDER') or 'converted')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 104857600)  # 100MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
