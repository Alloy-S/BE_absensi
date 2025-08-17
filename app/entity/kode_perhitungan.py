from app.database import db

class KodePerhitungan(db.Model):
    __tablename__ = 'kode_perhitungan'

    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    field_laporan = db.Column(db.String(50), nullable=False)