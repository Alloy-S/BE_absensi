from app.database import db
from app.entity import BackupLog


class BackupLogRepository:
    @staticmethod
    def create_backup_log(data):
        new_backup_log = BackupLog(
            start_date=data['start_date'],
            end_date=data['end_date'],
            status=data['status'],
        )

        db.session.add(new_backup_log)
        db.session.flush()
        return new_backup_log

    @staticmethod
    def get_backup_log_by_id(id):
        return BackupLog.query.filter_by(id=id).first()

    @staticmethod
    def get_all_backup_log():
        return BackupLog.query.order_by(BackupLog.date_created.desc()).all()

    @staticmethod
    def get_all_backup_log_paginated(page=1, size=10):
        query = BackupLog.query

        return query.order_by(BackupLog.date_created.desc()).paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def delete_backup_log(log):
        db.session.delete(log)
