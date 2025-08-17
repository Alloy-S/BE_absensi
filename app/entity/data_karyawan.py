from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLAEnum

from app.enums.face_recog_mode import FaceRecogMode


class DataKaryawan(db.Model):
    __tablename__ = 'data_karyawan'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nip = db.Column(db.String(8), nullable=False)
    tgl_gabung = db.Column(db.Date, nullable=False)
    tgl_resign = db.Column(db.Date, nullable=True)
    tipe_karyawan = db.Column(db.String(30), nullable=True)
    gaji_pokok = db.Column(db.Numeric(15, 2), nullable=True)
    face_recognition_mode = db.Column(SQLAEnum(FaceRecogMode, name="face_recog_mode"), nullable=True)
    
    lokasi_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lokasi.id'), nullable=False)
    jadwal_kerja_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jadwal_kerja.id'), nullable=True)
    jabatan_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jabatan.id'), nullable=False)
    user_pic_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False, unique=True)
    grup_gaji_id = db.Column(UUID(as_uuid=True), db.ForeignKey('grup_gaji.id'), nullable=True)
    
    pic = db.relationship('Users', foreign_keys=[user_pic_id], back_populates='user_pic')
    user = db.relationship('Users', back_populates='data_karyawan', foreign_keys=[user_id])
    lokasi = db.relationship('Lokasi', back_populates='data_karyawan')
    jadwal_kerja = db.relationship('JadwalKerja', back_populates='data_karyawan')
    jabatan = db.relationship('Jabatan', back_populates='data_karyawan')
    grup_gaji = db.relationship('GrupGaji', back_populates='data_karyawan')

    def __repr__(self):
        return (f"<DataKaryawan(id={self.id}, nip='{self.nip}', tgl_gabung='{self.tgl_gabung}', "
                f"lokasi_kerja='{self.lokasi_kerja}', tipe_karyawan='{self.tipe_karyawan}', "
                f"jabatan='{self.jabatan}', lokasi_id='{self.lokasi_id}', jadwal_kerja_id='{self.jadwal_kerja_id}')>")