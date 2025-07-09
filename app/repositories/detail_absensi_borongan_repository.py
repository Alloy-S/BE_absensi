from app.database import db
from app.entity import DetailAbsensiBorongan

class DetailAbsensiBoronganRepository:
    @staticmethod
    def create(ton_normal, ton_lembur, tipe, total, user_id, absensi_borongan_id, harga_id):
        new_detail = DetailAbsensiBorongan(
            ton_normal=ton_normal,
            ton_lembur=ton_lembur,
            tipe=tipe,
            total=total,
            user_id=user_id,
            absensi_borongan_id=absensi_borongan_id,
            harga_id=harga_id
        )
        db.session.add(new_detail)
        return new_detail