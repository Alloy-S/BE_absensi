from flask import Flask
from flask_restful import Api
from config import Config
from controllers import lokasi_controller
from database import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy.orm import configure_mappers
from controllers.auth_controller import Login, Register
from controllers.lokasi_controller import lokasi_bp
from controllers.jadwal_controller import jadwal_bp
from controllers.jabatan_controller import jabatan_bp
from controllers.user_controller import user_bp
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

app.register_blueprint(user_bp)
app.register_blueprint(jabatan_bp)
app.register_blueprint(lokasi_bp)
app.register_blueprint(jadwal_bp)

if __name__ == '__main__':
    print("running")
    app.run(debug=True)
