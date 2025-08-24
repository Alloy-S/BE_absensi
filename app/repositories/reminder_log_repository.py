from app.database import db
from app.entity import ReminderLog

class ReminderLogRepository:

    @staticmethod
    def create_reminder_log(data):
        new_reminder_log = ReminderLog(
            user_id=data['user_id'],
            reminder_type=data['reminder_type'],
            date=data['date'],
        )

        db.session.add(new_reminder_log)
        db.session.commit()

        return new_reminder_log