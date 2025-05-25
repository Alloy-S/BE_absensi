from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DataKaryawan(db.Model):
    __tablename__ = 'data_karyawan'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nip = db.Column(db.String(8), nullable=False)
    tgl_gabung = db.Column(db.Date, nullable=False)
    tipe_karyawan = db.Column(db.String(30), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    lokasi_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lokasi.id'), nullable=False)
    jadwal_kerja_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jadwal_kerja.id'), nullable=False)
    jabatan_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jabatan.id'), nullable=False)
    
    
    user = db.relationship('Users', back_populates='data_karyawan')
    lokasi = db.relationship('Lokasi', back_populates='data_karyawan')
    jadwal_kerja = db.relationship('JadwalKerja', back_populates='data_karyawan')
    jabatan = db.relationship('Jabatan', back_populates='data_karyawan')
    jatah_kuota_cuti = db.relationship("JatahKuotaCuti", back_populates="data_karyawan")

    def __repr__(self):
        return (f"<DataKaryawan(id={self.id}, nip='{self.nip}', tgl_gabung='{self.tgl_gabung}', "
                f"lokasi_kerja='{self.lokasi_kerja}', tipe_karyawan='{self.tipe_karyawan}', "
                f"jabatan='{self.jabatan}', lokasi_id='{self.lokasi_id}', jadwal_kerja_id='{self.jadwal_kerja_id}')>")