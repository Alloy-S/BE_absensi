from flask import Flask
from flask_restful import Api
from config import Config
from database import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy.orm import configure_mappers
from controllers.user_controller import UserController, UserListController
from controllers.auth_controller import Login, Register
from controllers.lokasi_controller import LokasiController, LokasiListController
from controllers.jadwal_controller import JadwalController, JadwalListController
from controllers.jabatan_controller import jabatan_bp
from flask_cors import CORS

configure_mappers()


app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)
migrate = Migrate(app, db) 
jwt = JWTManager(app)
api = Api(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


# Register API Routes
api.add_resource(Login, '/api/auth/login')
api.add_resource(Register, '/api/auth/register')

api.add_resource(UserListController, '/api/users')
api.add_resource(UserController, '/api/users/<string:id>')

api.add_resource(LokasiListController, '/api/konfigurasi/lokasi')
api.add_resource(LokasiController, '/api/konfigurasi/lokasi/<string:id>')


api.add_resource(JadwalListController, '/api/konfigurasi/jadwal')
api.add_resource(JadwalController, '/api/konfigurasi/jadwal/<string:id>')

app.register_blueprint(jabatan_bp)

if __name__ == '__main__':
    print("running")
    app.run(debug=True)
