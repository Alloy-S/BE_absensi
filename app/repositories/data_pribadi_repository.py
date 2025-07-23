from app.entity import DataPribadi
from app.database import db

class DataPribadiRepository(DataPribadi):

    @staticmethod
    def get_data_pribadi_by_user_id(user_id):
        return DataPribadi.query.filter_by(user_id=user_id).first()