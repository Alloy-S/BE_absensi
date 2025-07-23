from app.database import db
from app.entity import Photo
from datetime import date
from sqlalchemy.orm import joinedload
from dateutil.relativedelta import relativedelta

class PhotoRepository:

    @staticmethod
    def create(data):
        new_photo = Photo(
            type='reimburse',  # atau dari request
            path=data['path'],
            filename=data['filename'],
            mimetype=data['mimetype'],
        )
        db.session.add(new_photo)
        db.session.flush()

        return new_photo

    @staticmethod
    def get_photo_by_id(photo_id):
        return Photo.query.filter_by(id=photo_id).first()

    @staticmethod
    def delete_photo(photo):
        db.session.delete(photo)

