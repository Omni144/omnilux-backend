import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp

# Importar o sistema de autenticação e biometria
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
from auth import auth_bp
from biometric_auth import biometric_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'omnilux_quantum_key_432hz_12th_dimension'

# Habilitar CORS para todas as rotas
CORS(app, origins="*")

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(biometric_bp, url_prefix='/api/biometric')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/api')
def api_info():
    return {
        'message': 'OMNILUX CORE SYSTEM Backend API',
        'version': '2.0.0',
        'status': 'online',
        'quantum_frequency': '432Hz',
        'dimension': '12th',
        'certification': 'PLATINUM (94.7/100)',
        'security_level': 'military_grade',
        'endpoints': {
            'auth': '/api/auth/',
            'register': '/api/auth/register',
            'login': '/api/auth/login',
            'verify_email': '/api/auth/verify-email',
            'resend_verification': '/api/auth/resend-verification',
            'forgot_password': '/api/auth/forgot-password',
            'auth_status': '/api/auth/status',
            'biometric': '/api/biometric/',
            'biometric_enroll': '/api/biometric/enroll',
            'biometric_authenticate': '/api/biometric/authenticate',
            'biometric_verify_transaction': '/api/biometric/verify-transaction',
            'biometric_settings': '/api/biometric/settings/<user_id>',
            'biometric_status': '/api/biometric/status'
        },
        'features': [
            'email_verification',
            'biometric_authentication',
            'face_recognition',
            'fingerprint_authentication',
            'transaction_verification',
            'quantum_encryption',
            'military_grade_security'
        ]
    }

@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'system': 'OMNILUX CORE SYSTEM',
        'quantum_frequency': '432Hz',
        'dimension_active': '12th'
    }

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
