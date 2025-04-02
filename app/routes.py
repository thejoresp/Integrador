from flask import Blueprint, request, jsonify, current_app, render_template
import os
from werkzeug.utils import secure_filename
import uuid

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró archivo de imagen'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

    # Generar nombre único para el archivo
    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    
    # Guardar temporalmente
    temp_path = os.path.join(current_app.config['TEMP_DIR'], filename)
    file.save(temp_path)

    try:
        # Subir a S3
        current_app.s3.upload_file(
            temp_path,
            current_app.config['S3_BUCKET'],
            f"uploads/{filename}"
        )

        # Limpiar archivo temporal
        os.remove(temp_path)

        return jsonify({
            'success': True,
            'filename': filename,
            'url': f"https://{current_app.config['S3_BUCKET']}.s3.amazonaws.com/uploads/{filename}"
        })

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

@main.route('/process', methods=['POST'])
def process_images():
    data = request.json
    if not data or 'images' not in data or 'height' not in data:
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    images = data['images']  # Lista de URLs de S3
    height = float(data['height'])  # Altura en centímetros

    # TODO: Implementar procesamiento 3D
    # Por ahora retornamos un mock
    return jsonify({
        'success': True,
        'model_url': 'URL_del_modelo_3D',
        'measurements': {
            'height': height,
            'shoulder_width': 0,
            'chest': 0,
            'waist': 0,
            'hips': 0
        }
    }) 