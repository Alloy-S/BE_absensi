from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'), nullable=False)
    
    user_role = db.relationship('UserRole', back_populates='users')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email}, user_role_id={self.user_role_id})>"
    
    
