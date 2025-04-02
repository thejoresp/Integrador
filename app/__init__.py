from flask import Flask
from .config import Config
import os
import boto3

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Asegurar que existan los directorios necesarios
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMP_DIR'], exist_ok=True)

    # Inicializar AWS S3
    app.s3 = boto3.client(
        's3',
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=app.config['AWS_REGION']
    )

    # Registrar blueprints
    from .routes import main
    app.register_blueprint(main)

    return app 