from database import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    user_role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_role.id'), nullable=False)
    data_kontak_id = db.Column(UUID(as_uuid=True), db.ForeignKey('data_kontak.id'), nullable=False)
    data_pribadi_id = db.Column(UUID(as_uuid=True), db.ForeignKey('data_pribadi.id'), nullable=False)
    data_karyawan_id = db.Column(UUID(as_uuid=True), db.ForeignKey('data_karyawan.id'), nullable=False)
    
    user_role = db.relationship('UserRole', back_populates='users')
    data_kontak = db.relationship('DataKontak', back_populates='user', uselist=False)
    data_pribadi = db.relationship('DataPribadi', back_populates='user', uselist=False)
    data_karyawan = db.relationship('DataKaryawan', back_populates='user', uselist=False)
    login_log = db.relationship('UserLoginLog', back_populates='user')
    reimburse = db.relationship('Reimburse', back_populates='user')
    approval_reimburse = db.relationship("ApprovalReimburse", back_populates="user")
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email}, user_role_id={self.user_role_id}, data_kontak_id={self.data_kontak_id}, data_pribadi_id={self.data_pribadi_id}, data_karyawan_id={self.data_karyawan_id},)>"
    
    
