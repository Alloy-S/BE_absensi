from app import AppConstants
from app.database import db
from sqlalchemy import text



class DashboardAdminRepository:

    @staticmethod
    def get_today_attendance_summary(target_date):


        query = text("""
                     WITH users_by_today_schedule AS (SELECT u.id
                                                      FROM users u
                                                               Join data_karyawan dk ON u.id = dk.user_id
                                                               JOIN detail_jadwal_kerja djk
                                                                    ON djk.jadwal_kerja_id = dk.jadwal_kerja_id
                                                                        AND djk.is_active = true
                                                                        AND djk.hari =
                                                                            CAST(CASE EXTRACT(DOW FROM (:target_date)::date)
                                                                                     WHEN 0 THEN 'MINGGU'
                                                                                     WHEN 1 THEN 'SENIN'
                                                                                     WHEN 2 THEN 'SELASA'
                                                                                     WHEN 3 THEN 'RABU'
                                                                                     WHEN 4 THEN 'KAMIS'
                                                                                     WHEN 5 THEN 'JUMAT'
                                                                                     WHEN 6 THEN 'SABTU' END AS hari)
                                                      where dk.tipe_karyawan = 'bulanan'),
                          user_status_for_day AS (SELECT user_id,
                                                         status
                                                  FROM absensi
                                                  WHERE date::date = (:target_date)::date
                                                  UNION ALL
                                                  SELECT user_id,
                                                         'Izin' AS status
                                                  FROM izin
                                                  WHERE (:target_date)::date BETWEEN tgl_izin_start::date AND tgl_izin_end::date
                                                    AND status = 'Disetujui'),
                          final_user_status AS (SELECT u.id                          as user_id,
                                                       COALESCE(usc.status, 'Alpha') AS final_status
                                                FROM users_by_today_schedule u
                                                         LEFT JOIN user_status_for_day usc ON u.id = usc.user_id)
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
                      SELECT COUNT(u.id) as jumlah, dk.tipe_karyawan
                      FROM users u
                               JOIN data_karyawan dk ON u.id = dk.user_id
                      WHERE is_active is true
                      GROUP BY dk.tipe_karyawan
                      """)

        result = db.session.execute(query)

        return result.mappings().all()
