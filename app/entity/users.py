from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_face_registration_required = db.Column(db.Boolean, nullable=True, default=True)
    is_notif_login_send = db.Column(db.Boolean, nullable=True, default=False)
    is_active = db.Column(db.Boolean, nullable=True, default=True)
    user_role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_role.id'), nullable=True)
    data_kontak_id = db.Column(UUID(as_uuid=True), db.ForeignKey('data_kontak.id'), nullable=True)
    data_pribadi_id = db.Column(UUID(as_uuid=True), db.ForeignKey('data_pribadi.id'), nullable=True)
    data_karyawan_id = db.Column(UUID(as_uuid=True), db.ForeignKey('data_karyawan.id'), nullable=True)

    user_role = db.relationship('UserRole', back_populates='users', lazy="joined")
    user_pic = db.relationship('DataKaryawan', foreign_keys='[DataKaryawan.user_pic_id]', back_populates='pic')
    data_kontak = db.relationship('DataKontak', back_populates='user', uselist=False)
    data_pribadi = db.relationship('DataPribadi', back_populates='user', uselist=False)
    data_karyawan = db.relationship('DataKaryawan', foreign_keys=[data_karyawan_id], back_populates='user',
                                    uselist=False)
    login_log = db.relationship('UserLoginLog', back_populates='user')
    reimburse = db.relationship('Reimburse', back_populates='user')

    approval_izin = db.relationship("ApprovalIzin", back_populates="user",
                                       foreign_keys='[ApprovalIzin.user_id]')
    approval_user_izin = db.relationship("ApprovalIzin", back_populates="approval_user",
                                         foreign_keys='[ApprovalIzin.approval_user_id]')

    approval_lembur = db.relationship("ApprovalLembur", back_populates="user",
                                       foreign_keys='[ApprovalLembur.user_id]')
    approval_user_lembur = db.relationship("ApprovalLembur", back_populates="approval_user",
                                           foreign_keys='[ApprovalLembur.approval_user_id]')

    approval_reimburse = db.relationship("ApprovalReimburse", back_populates="user",
                                       foreign_keys='[ApprovalReimburse.user_id]')
    approval_user_reimburse = db.relationship("ApprovalReimburse", back_populates="approval_user",
                                              foreign_keys='[ApprovalReimburse.approval_user_id]')

    approval_koreksi = db.relationship("ApprovalKoreksi", back_populates="user",
                                       foreign_keys='[ApprovalKoreksi.user_id]')
    approval_user_koreksi = db.relationship("ApprovalKoreksi", back_populates="approval_user",
                                            foreign_keys='[ApprovalKoreksi.approval_user_id]')

    izin = db.relationship("Izin", back_populates="user")
    face_embeddings = db.relationship("FaceEmbeddings", back_populates="user")
    absensi = db.relationship("Absensi", back_populates="user")
    lembur = db.relationship('Lembur', back_populates="user")
    grup_gaji_user = db.relationship("GrupGajiUser", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User(fullname={self.fullname}, email={self.username}, user_role_id={self.user_role_id}, data_kontak_id={self.data_kontak_id}, data_pribadi_id={self.data_pribadi_id}, data_karyawan_id={self.data_karyawan_id},)>"
