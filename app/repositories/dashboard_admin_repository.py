from app import AppConstants
from app.database import db
from sqlalchemy import text
from datetime import datetime


class DashboardAdminRepository:

    @staticmethod
    def get_today_attendance_summary():
        target_date = datetime.today()
        # target_date = '2025-07-23'
        query = text("""
                     WITH user_status_for_day AS (SELECT user_id,
                                                         status
                                                  FROM absensi
                                                  WHERE date::date = :target_date
                                                  UNION ALL
                                                  SELECT user_id,
                                                         'Izin' AS status
                                                  FROM izin
                                                  WHERE (:target_date)::date BETWEEN tgl_izin_start::date AND tgl_izin_end::date
                                                    AND status = 'Disetujui'),
                          final_user_status AS (SELECT u.id                          as user_id,
                                                       u.fullname,
                                                       COALESCE(usc.status, 'Alpha') AS final_status
                                                FROM users u
                                                         LEFT JOIN user_status_for_day usc ON u.id = usc.user_id
                                                         JOIN data_karyawan dk ON u.id = dk.user_id)
                     SELECT fus.final_status,
                            count(*) AS jumlah
                     FROM final_user_status fus
                     group by fus.final_status;
                     """)

        result = db.session.execute(query, {'target_date': target_date})

        return result.mappings().all()


    @staticmethod
    def get_total_active_user():

        query =  text("""
                      SELECT COUNT(u.id)
                      FROM users u
                          JOIN data_karyawan dk ON u.id = dk.user_id
                      WHERE is_active is true
                      """)

        count_result = db.session.execute(query)

        return count_result.scalar() or 0
