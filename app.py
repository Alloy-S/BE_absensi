from flask import Flask
from flask_restful import Api
from config import Config
from database import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from controllers.user_controller import UserController
from controllers.auth_controller import Login, Register
from sqlalchemy.orm import configure_mappers

configure_mappers()


app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)
migrate = Migrate(app, db) 
jwt = JWTManager(app)
api = Api(app)


# Register API Routes
api.add_resource(Login, '/api/auth/login')
api.add_resource(Register, '/api/auth/register')
api.add_resource(UserController, '/api/users/', '/api/users/<int:id>')
# api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)
