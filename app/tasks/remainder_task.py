from datetime import datetime, timedelta
from sqlalchemy import text
from app.entity import Libur
from app.repositories.reminder_log_repository import ReminderLogRepository
from app.services.notification_service import NotificationService
from app.utils.app_constans import AppConstants
from app import create_app
from rq import Queue
from redis import Redis
from app.database import db
import os


def check_for_clock_in_reminders():
    app = create_app()
    with app.app_context():
        now = datetime.now()
        today = now.date()

        is_holiday = db.session.query(Libur.id).filter(
            Libur.date == today,
        ).first() is not None

        if is_holiday:
            print(f"[{now}] Hari ini libur. tidak ada notif.")
            return

        check_from = now - timedelta(minutes=15)
        current_day_str = AppConstants.DAY_MAP.value[now.weekday()]

        sql_query = text("""
                         SELECT u.id, u.fullname, u.fcm_token, djk.time_in
                         FROM users u
                                  JOIN data_karyawan dk ON u.id = dk.user_id
                                  JOIN jadwal_kerja jk ON dk.jadwal_kerja_id = jk.id
                                  JOIN detail_jadwal_kerja djk ON jk.id = djk.jadwal_kerja_id
                                  LEFT JOIN absensi a ON u.id = a.user_id AND a.date = :today
                         WHERE u.is_active = TRUE
                           AND u.fcm_token IS NOT NULL
                           AND djk.hari = :day_of_week
                           AND djk.is_active = TRUE
                           AND djk.time_in BETWEEN :check_from_time AND :now_time
                           AND a.id IS NULL
                           AND u.id NOT IN (SELECT rl.user_id
                                            FROM reminder_log rl
                                            WHERE rl.date = :today
                                              AND rl.reminder_type = 'CLOCK_IN');
                         """)

        params = {
            "today": today,
            "day_of_week": current_day_str,
            "check_from_time": check_from.time(),
            "now_time": now.time()
        }

        result = db.session.execute(sql_query, params).mappings().all()

        if not result:
            print(f"[{now}] Tidak ada karyawan yang perlu dinotif untuk absen masuk.")
            return

        print(f"[{now}] Menemukan {len(result)} karyawan untuk dinotif absen masuk.")
        redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
        redis_conn = Redis.from_url(redis_url)
        q = Queue(connection=redis_conn)
        for user_data in result:
            q.enqueue(send_single_clock_in_reminder,
                      user_data['id'],
                      user_data['fullname'],
                      user_data['fcm_token'],
                      user_data['time_in'])


def check_for_clock_out_reminders():
    app = create_app()
    with app.app_context():
        now = datetime.now()
        today = now.date()

        is_holiday = db.session.query(Libur.id).filter(
            Libur.date == today,
        ).first() is not None

        if is_holiday:
            print(f"[{now}] Hari ini libur. tidak perlu dinotif.")
            return

        check_until = now + timedelta(minutes=15)
        current_day_str = AppConstants.DAY_MAP.value[now.weekday()]

        sql_query = text("""
                         SELECT a.user_id, u.fullname, u.fcm_token, djk.time_out
                         FROM absensi a
                                  JOIN users u ON a.user_id = u.id
                                  JOIN data_karyawan dk ON a.user_id = dk.user_id
                                  JOIN jadwal_kerja jk ON dk.jadwal_kerja_id = jk.id
                                  JOIN detail_jadwal_kerja djk ON jk.id = djk.jadwal_kerja_id
                         WHERE a.date = :today
                           AND u.fcm_token IS NOT NULL
                           AND EXISTS (SELECT 1
                                       FROM detail_absensi da_in
                                       WHERE da_in.absensi_id = a.id
                                         AND da_in.type = 'IN')
                           AND NOT EXISTS (SELECT 1
                                           FROM detail_absensi da_out
                                           WHERE da_out.absensi_id = a.id
                                             AND da_out.type = 'OUT')
                           AND djk.hari = :day_of_week
                           AND djk.is_active = TRUE
                           AND djk.time_out BETWEEN :now_time AND :check_until_time
                           AND a.user_id NOT IN (SELECT rl.user_id
                                                 FROM reminder_log rl
                                                 WHERE rl.date = :today
                                                   AND rl.reminder_type = 'CLOCK_OUT');
                         """)

        params = {
            "today": today,
            "day_of_week": current_day_str,
            "now_time": now.time(),
            "check_until_time": check_until.time()
        }

        result = db.session.execute(sql_query, params).mappings().all()

        if not result:
            print(f"[{now}] Tidak ada karyawan yang perlu dinotif untuk absen pulang.")
            return

        print(f"[{now}] Menemukan {len(result)} karyawan untuk dinotif absen pulang.")
        redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
        redis_conn = Redis.from_url(redis_url)
        q = Queue(connection=redis_conn)
        for user_data in result:
            q.enqueue(send_single_clock_out_reminder,
                      user_data['user_id'],
                      user_data['fullname'],
                      user_data['fcm_token'],
                      user_data['time_out'])


def send_single_clock_in_reminder(user_id, fullname, fcm_token, time_in):
    app = create_app()
    with app.app_context():
        judul = "Pengingat Absen Masuk"
        isi_pesan = f"Jadwal masuk Anda hari ini adalah pukul {time_in.strftime('%H:%M')}. Jangan lupa absen."

        sent = NotificationService.send_single_notification(fcm_token, judul, isi_pesan)

        if sent:
            ReminderLogRepository.create_reminder_log({
                'user_id': user_id,
                'reminder_type': 'CLOCK_IN',
                'date': datetime.now().date()
            })

            print(f"notif absen masuk berhasil dikirim ke {fullname}")
        else:
            print(
                f"Gagal kirim notif absen masuk ke {fullname}.")


def send_single_clock_out_reminder(user_id, fullname, fcm_token, time_out):
    app = create_app()
    with app.app_context():
        judul = "Pengingat Absen Pulang"
        isi_pesan = f"Jadwal pulang Anda hari ini adalah pukul {time_out.strftime('%H:%M')}. Jangan lupa absen."

        sent = NotificationService.send_single_notification(fcm_token, judul, isi_pesan)

        if sent:
            ReminderLogRepository.create_reminder_log({
                'user_id': user_id,
                'reminder_type': 'CLOCK_OUT',
                'date': datetime.now().date()
            })

            print(f"notif absen pulang berhasil dikirim ke {fullname}")
        else:
            print(
                f"Gagal kirim notif absen pulang ke {fullname}.")
