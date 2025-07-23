from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class DetailReimburse(db.Model):
    __tablename__ = 'detail_reimburse'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama = db.Column(db.String(255), nullable=False)
    harga = db.Column(db.Numeric(9, 2), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    reimburse_id = db.Column(UUID(as_uuid=True), db.ForeignKey('reimburse.id'))

    reimburse = db.relationship("Reimburse", back_populates="detail_reimburse")


    def __repr__(self):
        return (
            f"<DetailReimburse(id={self.id}, nama='{self.nama}', jumlah={self.jumlah})>"
        )
