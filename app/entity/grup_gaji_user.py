from app.database import db
from sqlalchemy.dialects.postgresql import UUID

class GrupGajiUser(db.Model):
    __tablename__ = 'grup_gaji_user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grup_id = db.Column(UUID(as_uuid=True), db.ForeignKey('grup_gaji.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    grup_gaji = db.relationship('GrupGaji', back_populates='grup_gaji_user')
    user = db.relationship('Users', back_populates='grup_gaji_user')
    
    def __repr__(self):
        return f"<GrupGajiUser(grp_id='{self.grup_id}', user_id='{self.user_id}')>"