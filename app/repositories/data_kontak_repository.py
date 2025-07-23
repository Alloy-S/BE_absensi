from app.entity import DataKontak
from app.database import db


class DataKontakRepository(DataKontak):

    @staticmethod
    def get_data_kontak_by_user_id(user_id):
        return DataKontak.query.filter_by(user_id=user_id).first()