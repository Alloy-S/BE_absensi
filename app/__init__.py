from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.orm import configure_mappers

# Pindahkan inisialisasi extensions ke luar factory
# agar bisa diimpor di file lain (misal: models) tanpa circular import
from .database import db
from .config import Config

migrate = Migrate()
jwt = JWTManager()
# Dll.

# Panggil configure_mappers sekali di awal
configure_mappers()

def create_app(config_class=Config):
    """
    Application Factory Function
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inisialisasi extensions dengan aplikasi di dalam factory
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    Api(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # --- Registrasi Blueprint di dalam factory ---
    # Impor blueprint di dalam fungsi untuk menghindari circular import
    from app.execption.execption_handler import errors_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.jabatan_controller import jabatan_bp
    from app.controllers.lokasi_controller import lokasi_bp
    from app.controllers.jadwal_controller import jadwal_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth') # Sangat disarankan memberi prefix
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(jabatan_bp, url_prefix='/api/jabatan')
    app.register_blueprint(lokasi_bp, url_prefix='/api/lokasi')
    app.register_blueprint(jadwal_bp, url_prefix='/api/jadwal')

    # Jika ada route sederhana, bisa ditaruh di sini
    @app.route('/test-health')
    def test_health():
        return "Server is healthy!"

    return app