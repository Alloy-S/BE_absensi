from app.database import db
from sqlalchemy import text, func


class RekapPeriodeRepository:

    @staticmethod
    def generate_laporan_periode(start_date, end_date, search, page=1, size=10):
        query = text("""
                     WITH daily_attendance_times AS (SELECT absensi_id,
                                                            MIN(CASE WHEN type = 'IN' THEN date END)  AS time_in,
                                                            MAX(CASE WHEN type = 'OUT' THEN date END) AS time_out
                                                     FROM detail_absensi
                                                     GROUP BY absensi_id),
                          attendance_agg AS (SELECT a.user_id,
                                                    COUNT(CASE WHEN dat.time_in IS NOT NULL AND dat.time_out IS NOT NULL THEN 1 END) AS total_kehadiran,
                                                    COUNT(CASE
                                                              WHEN a.status IN ('Datang Terlambat',
                                                                                'Datang Terlambat & Pulang Cepat') AND
                                                                   dat.time_out IS NOT NULL
                                                                  THEN 1 END)                                                        AS total_terlambat,
                                                    COUNT(CASE
                                                              WHEN a.status IN ('Pulang Cepat',
                                                                                'Datang Terlambat & Pulang Cepat') AND
                                                                   dat.time_out IS NOT NULL
                                                                  THEN 1 END)                                                        AS total_pulang_awal,
                                                    COUNT(CASE WHEN dat.time_out IS NULL THEN 1 END)                                 AS total_absen_tidak_lengkap,
                                                    SUM(EXTRACT(epoch FROM
                                                                (COALESCE(dat.time_out, dat.time_in) - dat.time_in)) /
                                                        60)                                                                          AS total_menit_kehadiran,
                                                    SUM(CASE
                                                            WHEN a.status IN ('Datang Terlambat', 'Datang Terlambat & Pulang Cepat')
                                                                THEN EXTRACT(epoch FROM
                                                                             (dat.time_in - (a.date::date + a.jadwal_time_in))) /
                                                                     60
                                                            ELSE 0
                                                        END)                                                                         AS total_menit_terlambat,
                                                    SUM(CASE
                                                            WHEN a.status IN
                                                                 ('Pulang Cepat', 'Datang Terlambat & Pulang Cepat') AND
                                                                 dat.time_out IS NOT NULL
                                                                THEN EXTRACT(epoch FROM
                                                                             ((a.date::date + a.jadwal_time_out) - dat.time_out)) /
                                                                     60
                                                            ELSE 0
                                                        END)                                                                         AS total_menit_pulang_awal

                                             FROM absensi a
                                                      JOIN daily_attendance_times dat ON a.id = dat.absensi_id
                                             WHERE a.date BETWEEN :start_date AND :end_date
                                             GROUP BY a.user_id),
                          izin_agg AS (SELECT izin.user_id,
                                              SUM(
                                                      izin.durasi_hari_kerja
                                              ) AS total_izin
                                       FROM izin
                                       WHERE izin.status = 'Disetujui'
                                         AND izin.tgl_izin_start <= :end_date
                                         AND izin.tgl_izin_end >= :start_date
                                       GROUP BY izin.user_id),
                          calendar AS (SELECT generate_series((:start_date)::date, (:end_date)::date,
                                                              '1 day'::interval)::date AS calendar_date),
                          expected_workdays AS (SELECT u.id as user_id,
                                                       c.calendar_date
                                                FROM users u
                                                         CROSS JOIN calendar c
                                                         JOIN data_karyawan dk ON u.id = dk.user_id
                                                         JOIN jadwal_kerja jk ON dk.jadwal_kerja_id = jk.id
                                                         JOIN detail_jadwal_kerja djk ON jk.id = djk.jadwal_kerja_id
                                                    AND djk.is_active = TRUE
                                                    AND djk.hari = CAST(CASE EXTRACT(DOW FROM c.calendar_date)
                                                                            WHEN 0 THEN 'MINGGU'
                                                                            WHEN 1 THEN 'SENIN'
                                                                            WHEN 2 THEN 'SELASA'
                                                                            WHEN 3 THEN 'RABU'
                                                                            WHEN 4 THEN 'KAMIS'
                                                                            WHEN 5 THEN 'JUMAT'
                                                                            WHEN 6 THEN 'SABTU' END AS hari)
                                                         LEFT JOIN libur hl ON c.calendar_date = hl.date
                                                WHERE hl.id IS NULL),
                          alpha_agg AS (SELECT ew.user_id,
                                               COUNT(ew.calendar_date) AS total_tidak_hadir
                                        FROM expected_workdays ew
                                                 LEFT JOIN absensi a ON ew.user_id = a.user_id AND ew.calendar_date = a.date::date
                                                 LEFT JOIN izin i
                                                           ON ew.user_id = i.user_id AND i.status = 'Disetujui' AND
                                                              ew.calendar_date BETWEEN i.tgl_izin_start AND i.tgl_izin_end
                                        WHERE a.id IS NULL
                                          AND i.id IS NULL
                                        GROUP BY ew.user_id)
                     SELECT dk.nip,
                            u.fullname                                AS nama,
                            dk.tipe_karyawan,
                            j.nama                                    AS jabatan,
                            l.name                                    AS lokasi,
                            COALESCE(aa.total_kehadiran, 0)           AS total_kehadiran,
                            COALESCE(ia.total_izin, 0)                AS total_izin,
                            COALESCE(alpha.total_tidak_hadir, 0)      AS total_tidak_hadir,
                            COALESCE(aa.total_absen_tidak_lengkap, 0) AS total_absen_tidak_lengkap,
                            COALESCE(aa.total_terlambat, 0)           AS total_terlambat,
                            COALESCE(aa.total_pulang_awal, 0)         AS total_pulang_awal,
                            COALESCE(aa.total_menit_kehadiran, 0)     AS total_menit_kehadiran,
                            COALESCE(aa.total_menit_terlambat, 0)     AS total_menit_terlambat,
                            COALESCE(aa.total_menit_pulang_awal, 0)   AS total_menit_pulang_awal
                     FROM data_karyawan dk
                              JOIN users u ON dk.user_id = u.id AND u.is_active = true
                              JOIN jabatan j ON dk.jabatan_id = j.id
                              JOIN lokasi l ON dk.lokasi_id = l.id
                              LEFT JOIN attendance_agg aa ON u.id = aa.user_id
                              LEFT JOIN izin_agg ia ON u.id = ia.user_id
                              LEFT JOIN alpha_agg alpha ON u.id = alpha.user_id
                     WHERE (u.fullname ILIKE :search OR dk.nip ILIKE :search)
                     ORDER BY u.fullname
                     LIMIT :size OFFSET :offset;

                     """)

        sql_count_query = text("""
                               SELECT COUNT(u.id)
                               FROM data_karyawan dk
                                        JOIN users u ON dk.user_id = u.id AND u.is_active = true
                               WHERE (u.fullname ILIKE :search OR
                                      dk.nip ILIKE :search)
                               """)

        offset = (page - 1) * size
        search_pattern = f"%{search}%"

        params = {
            'start_date': start_date,
            'end_date': end_date,
            'search': search_pattern,
            'size': size,
            'offset': offset
        }

        result = db.session.execute(query, params)

        result_count = db.session.execute(sql_count_query, {'search': search_pattern})

        items = result.mappings().all()
        total = result_count.scalar() or 0

        return {
            'total': total,
            'pages': (total + size - 1) // size if total > 0 else 0,
            'items': items
        }
