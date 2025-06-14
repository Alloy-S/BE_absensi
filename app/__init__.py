from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.orm import configure_mappers
import locale
from .database import db
from .config import Config

migrate = Migrate()
jwt = JWTManager()

configure_mappers()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    Api(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    try:
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Indonesian_Indonesia.1252')
        except locale.Error:
            print("Peringatan: Locale 'id_ID' tidak dapat diatur. Nama hari/bulan mungkin dalam Bahasa Inggris.")

    from app.execption.execption_handler import errors_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.jabatan_controller import jabatan_bp
    from app.controllers.lokasi_controller import lokasi_bp
    from app.controllers.jadwal_controller import jadwal_bp
    from app.controllers.face_recognition_controller import face_recognition_bp
    from app.controllers.libur_controller import libur_bp
    from app.controllers.attendance_controller import attendance_bp
    from app.controllers.absensi_controller import absensi_bp
    from app.controllers.koreksi_kehadiran_controller import koreksi_kehadiran_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(jabatan_bp, url_prefix='/api/jabatan')
    app.register_blueprint(lokasi_bp, url_prefix='/api/lokasi')
    app.register_blueprint(jadwal_bp, url_prefix='/api/jadwal')
    app.register_blueprint(face_recognition_bp, url_prefix='/api/face-recognition')
    app.register_blueprint(libur_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(absensi_bp)
    app.register_blueprint(koreksi_kehadiran_bp)

    @app.route('/test-health')
    def test_health():
        return "Server is healthy!"

    return app