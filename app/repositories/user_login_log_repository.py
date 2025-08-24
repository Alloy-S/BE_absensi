from app.database import db
from app.entity import UserLoginLog
from datetime import datetime

class UserLoginLogRepository:

    @staticmethod
    def create_login_log(data):
        new_login_log = UserLoginLog(
            user_id=data['user_id'],
            status=data['status'],
        )

        db.session.add(new_login_log)
        db.session.commit()

        return new_login_log

    @staticmethod
    def update_login_to_logout_log(user_id):
        login_log = UserLoginLog.query.filter_by(user_id=user_id, status='LOGIN').order_by(UserLoginLog.date_time.desc()).first()

        if login_log:
            login_log.status = 'LOGOUT'
            login_log.date_time = datetime.now()
            db.session.commit()