from app.database import db
from app.entity import Lembur

class LemburRepository:
    @staticmethod
    def create_lembur(data):

        new_lembur = Lembur(
            date_start=data['date_start'],
            date_end=data['date_end'],
            keterangan=data['keterangan'],
            status=data['status'],
            user_id= data['user_id'],
        )
        db.session.add(new_lembur)
        db.session.flush()
        return new_lembur