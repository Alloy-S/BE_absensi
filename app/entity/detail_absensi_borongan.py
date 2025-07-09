from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class DetailAbsensiBorongan(db.Model):
    __tablename__ = 'detail_absensi_borongan'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ton_normal = db.Column(db.Numeric(9, 2), nullable=False)
    ton_lembur = db.Column(db.Numeric(9, 2), nullable=False, default=0)
    tipe = db.Column(db.String(20), nullable=False)
    total = db.Column(db.Numeric(9, 2), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    absensi_borongan_id = db.Column(UUID(as_uuid=True), db.ForeignKey('absensi_borongan.id', ondelete="CASCADE"), nullable=False)
    harga_id = db.Column(UUID(as_uuid=True), db.ForeignKey('harga_harian_borongan.id'), nullable=False)

    user = db.relationship('Users', back_populates='detail_absensi_borongan')
    harga = db.relationship("HargaHarianBorongan", back_populates="detail_absensi_borongan", lazy="joined")
    absensi_borongan = db.relationship("AbsensiBorongan", back_populates="detail_absensi_borongan", lazy="joined")

    def __repr__(self):
        return (f"<DetailAbsensiBorongan(id={self.id}, ton_normal={self.ton_normal}, ton_lembur={self.ton_lembur}, "
                f"tipe='{self.tipe}', total={self.total}, date='{self.date}', user_id={self.user_id}, absensi_borongan_id={self.absensi_borongan_id}, harga_id={self.harga_id})>")