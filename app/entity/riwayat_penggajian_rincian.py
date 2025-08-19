from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class RiwayatPenggajianRincian(db.Model):
    __tablename__ = 'riwayat_penggajian_rincian'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    komponen = db.Column(db.String(50), nullable=False)
    tipe = db.Column(db.String(20), nullable=False)
    nilai_a = db.Column(db.Numeric(15,2), nullable=False)
    nilai_b = db.Column(db.Numeric(15,2), nullable=False)
    operasi = db.Column(db.String(2), nullable=False)
    jumlah = db.Column(db.Numeric(15,2), nullable=False)
    riwayat_penggajian_detail_id = db.Column(UUID(as_uuid=True), db.ForeignKey('riwayat_penggajian_detail.id', ondelete="CASCADE"), nullable=False)

    riwayat_penggajian_detail = db.relationship("RiwayatPenggajianDetail", back_populates="riwayat_penggajian_rincian")