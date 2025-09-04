from app.database import db
from sqlalchemy import text, func, or_
from app.entity import Users, JatahKuotaCuti, DataKaryawan
from datetime import date


class LaporanRepository:

    @staticmethod
    def generate_laporan_periode_pagination(start_date, end_date, search, page=1, size=10):
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
                                             WHERE a.date::date BETWEEN (:start_date)::date AND (:end_date)::date
                                             GROUP BY a.user_id),
                          izin_agg AS (SELECT i.user_id,
                                              SUM(i.durasi_hari_kerja) AS total_izin,
                                              SUM(CASE WHEN ji.is_paid = true THEN i.durasi_hari_kerja ELSE 0 END) AS total_izin_berbayar,
                                              SUM(CASE WHEN ji.is_paid = false THEN i.durasi_hari_kerja ELSE 0 END) AS total_izin_tidak_berbayar
                                       FROM izin i
                                       JOIN jenis_izin ji ON i.jenis_izin_id = ji.id
                                       WHERE i.status = 'Disetujui'
                                         AND i.tgl_izin_start <= :end_date
                                         AND i.tgl_izin_end >= :start_date
                                       GROUP BY i.user_id),
                          lembur_agg AS (SELECT l.user_id,
                                                ROUND((SUM(EXtract(epoch FROM (l.date_end - l.date_start)) / 3600)) / 0.25) *
                                                0.25 AS total_jam_lembur
                                         FROM lembur l
                                         WHERE l.status = 'Disetujui' AND l.date_start::date BETWEEN (:start_date)::date AND (:end_date)::date
                                         GROUP BY l.user_id),
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
                                                WHERE hl.id IS NULL 
                                                AND c.calendar_date >= dk.tgl_gabung 
                                                AND (dk.tgl_resign IS NULL OR c.calendar_date <= dk.tgl_resign)),
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
                            COALESCE(ia.total_izin_berbayar, 0)       AS total_izin_berbayar,
                            COALESCE(ia.total_izin_tidak_berbayar, 0) AS total_izin_tidak_berbayar,
                            COALESCE(alpha.total_tidak_hadir, 0)      AS total_tidak_hadir,
                            COALESCE(aa.total_absen_tidak_lengkap, 0) AS total_absen_tidak_lengkap,
                            COALESCE(aa.total_terlambat, 0)           AS total_terlambat,
                            COALESCE(aa.total_pulang_awal, 0)         AS total_pulang_awal,
                            COALESCE(aa.total_menit_kehadiran, 0)     AS total_menit_kehadiran,
                            COALESCE(aa.total_menit_terlambat, 0)     AS total_menit_terlambat,
                            COALESCE(aa.total_menit_pulang_awal, 0)   AS total_menit_pulang_awal,
                            COALESCE(la.total_jam_lembur, 0)          AS total_jam_lembur
                     FROM data_karyawan dk
                              JOIN users u ON dk.user_id = u.id AND u.is_active = true
                              JOIN jabatan j ON dk.jabatan_id = j.id
                              JOIN lokasi l ON dk.lokasi_id = l.id
                              LEFT JOIN attendance_agg aa ON u.id = aa.user_id
                              LEFT JOIN izin_agg ia ON u.id = ia.user_id
                              LEFT JOIN alpha_agg alpha ON u.id = alpha.user_id
                              LEFT JOIN lembur_agg la ON u.id = la.user_id
                     WHERE u.is_active = true AND (u.fullname ILIKE :search OR dk.nip ILIKE :search) AND dk.tipe_karyawan = 'bulanan'
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

    @staticmethod
    def generate_laporan_periode(list_user, start_date, end_date):
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
                                             WHERE a.date::date BETWEEN (:start_date)::date AND (:end_date)::date
                                             GROUP BY a.user_id),
                          izin_agg AS (SELECT i.user_id,
                                              SUM(i.durasi_hari_kerja) AS total_izin,
                                              SUM(CASE WHEN ji.is_paid = true THEN i.durasi_hari_kerja ELSE 0 END) AS total_izin_berbayar,
                                              SUM(CASE WHEN ji.is_paid = false THEN i.durasi_hari_kerja ELSE 0 END) AS total_izin_tidak_berbayar
                                       FROM izin i
                                       JOIN jenis_izin ji ON i.jenis_izin_id = ji.id
                                       WHERE i.status = 'Disetujui'
                                         AND i.tgl_izin_start <= :end_date
                                         AND i.tgl_izin_end >= :start_date
                                       GROUP BY i.user_id),
                          lembur_agg AS (SELECT l.user_id,
                                                ROUND((SUM(EXTRACT(epoch FROM (l.date_end - l.date_start)) / 3600)) / 0.25) * 
                                                0.25 AS total_jam_lembur
                                         FROM lembur l
                                         WHERE l.status = 'Disetujui' AND l.date_start::date BETWEEN (:start_date)::date AND (:end_date)::date
                                         GROUP BY l.user_id),
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
                                                WHERE hl.id IS NULL
                                                AND c.calendar_date >= dk.tgl_gabung 
                                                AND (dk.tgl_resign IS NULL OR c.calendar_date <= dk.tgl_resign)),
                          count_workdays AS (SELECT ew.user_id, COUNT(ew.calendar_date) AS total_hari_kerja
                                             FROM expected_workdays ew
                                             GROUP BY ew.user_id),
                          count_full_workday AS (SELECT u.id as user_id,
                                                        COUNT(c.calendar_date) AS total_hari_kerja_penuh
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
                                                WHERE hl.id IS NULL
                                                GROUP BY u.id
                          ),
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
                     SELECT u.id,
                            dk.nip,
                            u.fullname                                AS nama,
                            dk.tipe_karyawan,
                            j.nama                                    AS jabatan,
                            l.name                                    AS lokasi,
                            dk.gaji_pokok,
                            (dk.gaji_pokok / COALESCE(cfw.total_hari_kerja_penuh, 0)) AS gaji_harian,
                            COALESCE(aa.total_kehadiran, 0)           AS total_kehadiran,
                            COALESCE(ia.total_izin, 0)                AS total_izin,
                            COALESCE(ia.total_izin_berbayar, 0)       AS total_izin_berbayar,
                            COALESCE(ia.total_izin_tidak_berbayar, 0) AS total_izin_tidak_berbayar,
                            COALESCE(alpha.total_tidak_hadir, 0)      AS total_tidak_hadir,
                            COALESCE(aa.total_absen_tidak_lengkap, 0) AS total_absen_tidak_lengkap,
                            COALESCE(aa.total_terlambat, 0)           AS total_terlambat,
                            COALESCE(aa.total_pulang_awal, 0)         AS total_pulang_awal,
                            COALESCE(aa.total_menit_kehadiran, 0)     AS total_menit_kehadiran,
                            COALESCE(aa.total_menit_terlambat, 0)     AS total_menit_terlambat,
                            COALESCE(aa.total_menit_pulang_awal, 0)   AS total_menit_pulang_awal,
                            COALESCE(cw.total_hari_kerja, 0)          AS total_hari_kerja,
                            COALESCE(la.total_jam_lembur, 0)          AS total_jam_lembur,
                            COALESCE(cfw.total_hari_kerja_penuh, 0)   AS total_hari_kerja_penuh
                     FROM data_karyawan dk
                              JOIN users u ON dk.user_id = u.id AND u.is_active = true
                              JOIN jabatan j ON dk.jabatan_id = j.id
                              JOIN lokasi l ON dk.lokasi_id = l.id
                              LEFT JOIN attendance_agg aa ON u.id = aa.user_id
                              LEFT JOIN izin_agg ia ON u.id = ia.user_id
                              LEFT JOIN alpha_agg alpha ON u.id = alpha.user_id
                              LEFT JOIN count_workdays cw ON cw.user_id = u.id
                              LEFT JOIN lembur_agg la ON u.id = la.user_id
                              LEFT JOIN count_full_workday cfw ON cfw.user_id = u.id
                     WHERE u.id IN :list_user
                     ORDER BY u.fullname
                     """)

        params = {
            'start_date': start_date,
            'end_date': end_date,
            'list_user': tuple(list_user),
        }

        result = db.session.execute(query, params)

        result = result.mappings().all()

        return {
            item['id']: item for item in result
        }

    @staticmethod
    def generate_laporan_terlambat(start_date, end_date, search, page=1, size=10):
        query = text("""
                     SELECT dk.nip,
                            u.fullname  AS nama,
                            j.nama      AS jabatan,
                            jk.shift    AS jadwal_kerja,
                            l.name      AS lokasi,
                            a.date      as date_absensi,
                            da.date     as waktu_absen,
                            a.jadwal_time_in,
                            COALESCE(ROUND(EXTRACT(epoch FROM da.date - (a.date + a.jadwal_time_in)) / 60, 2),
                                     0) AS menit_terlambat
                     FROM absensi a
                              JOIN detail_absensi da ON a.id = da.absensi_id and da.type = 'IN'
                              JOIN users u ON a.user_id = u.id
                              JOIN data_karyawan dk ON u.id = dk.user_id
                              JOIN jabatan j ON dk.jabatan_id = j.id
                              JOIN jadwal_kerja jk ON a.jadwal_kerja_id = jk.id
                              JOIN lokasi l ON dk.lokasi_id = l.id
                     WHERE a.status IN ('Datang Terlambat', 'Datang Terlambat & Pulang Cepat')
                       AND a.date BETWEEN :start_date AND :end_date
                       AND (u.fullname ILIKE :search OR dk.nip ILIKE :search)
                     ORDER BY a.date DESC
                     LIMIT :size OFFSET :offset
                     """)

        count_query = text("""
                           SELECT COUNT(u.id)
                           FROM absensi a
                                    JOIN users u ON a.user_id = u.id AND u.is_active = true
                                    JOIN data_karyawan dk ON u.id = dk.user_id
                           WHERE (u.fullname ILIKE :search OR dk.nip ILIKE :search)
                             AND a.status IN ('Datang Terlambat', 'Datang Terlambat & Pulang Cepat')
                             AND a.date BETWEEN :start_date AND :end_date
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

        result_count = db.session.execute(count_query, {'start_date': start_date,
                                                        'end_date': end_date,
                                                        'search': search_pattern})

        items = result.mappings().all()
        total = result_count.scalar() or 0

        return {
            'total': total,
            'pages': (total + size - 1) // size if total > 0 else 0,
            'items': items
        }

    @staticmethod
    def generate_laporan_kuota_cuti(page=1, size=10, search=None, year=None):
        query = db.session.query(
            DataKaryawan.nip,
            Users.fullname.label('nama'),
            JatahKuotaCuti.periode,
            func.sum(JatahKuotaCuti.sisa_kuota).label("sisa_cuti_tahunan"),
            func.sum(JatahKuotaCuti.kuota_awal).label("total_cuti_tahunan"),
            func.sum(JatahKuotaCuti.kuota_terpakai).label("cuti_tahunan_terpakai")
        ).select_from(JatahKuotaCuti).join(
            Users, JatahKuotaCuti.user_id == Users.id
        ).join(
            DataKaryawan, Users.id == DataKaryawan.user_id
        )

        query = query.filter(Users.is_active.is_(True), DataKaryawan.tipe_karyawan == 'bulanan')

        if year:
            query = query.filter(JatahKuotaCuti.periode == year)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Users.fullname.ilike(search_pattern),
                    DataKaryawan.nip.ilike(search_pattern)
                )
            )

        query = query.group_by(
            Users.id,
            Users.fullname,
            DataKaryawan.nip,
            JatahKuotaCuti.periode,
        )

        query = query.order_by(DataKaryawan.nip.asc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def generate_laporan_upah_borongan_pagination(start_date, end_date, search, page=1, size=10):

        query = text("""
                     with calendar
                              AS (SELECT generate_series((:start_date)::date, (:end_date)::date,
                                                         '1 day'::interval)::date AS calendar_date),
                          paginated_users
                              AS (SELECT u.id, u.fullname AS nama, dk.nip, j.nama AS jabatan
                                  FROM users u
                                           JOIN data_karyawan dk ON u.id = dk.user_id
                                           JOIN jabatan j ON j.id = dk.jabatan_id
                                  WHERE dk.tipe_karyawan = 'harian/borongan'
                                    AND (u.fullname ILIKE :search OR
                                         dk.nip ILIKE :search)
                                  ORDER BY u.fullname
                                  LIMIT :size OFFSET :offset),
                          filtered_borongan
                              AS (SELECT dab.user_id,
                                         ab.date::date  AS date,
                                         SUM(dab.total) AS upah
                                  FROM detail_absensi_borongan dab
                                           JOIN
                                       absensi_borongan ab ON dab.absensi_borongan_id = ab.id
                                  WHERE ab.status = 'Disetujui'
                                    AND ab.date::date BETWEEN :start_date AND :end_date
                                  GROUP BY dab.user_id, ab.date::date)
                     select pu.nip, pu.nama, pu.jabatan, c.calendar_date, COALESCE(fb.upah, 0) AS upah
                     FROM paginated_users pu
                              CROSS JOIN calendar c
                              LEFT JOIN filtered_borongan fb ON fb.user_id = pu.id AND fb.date = c.calendar_date
                     """)

        count_query = text("""
                           SELECT COUNT(u.id)
                           FROM users u
                                    JOIN data_karyawan dk ON u.id = dk.user_id
                           WHERE dk.tipe_karyawan = 'harian/borongan'
                             AND (u.fullname ILIKE :search OR
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

        result_count = db.session.execute(count_query, {'search': search_pattern})

        items = result.mappings().all()
        total = result_count.scalar() or 0

        return {
            'items': items,
            'total': total,
        }

    @staticmethod
    def generate_laporan_upah_borongan(start_date, end_date, search):

        query = text("""
                     with calendar
                              AS (SELECT generate_series((:start_date)::date, (:end_date)::date,
                                                         '1 day'::interval)::date AS calendar_date),
                          paginated_users
                              AS (SELECT u.id, u.fullname AS nama, dk.nip, j.nama AS jabatan
                                  FROM users u
                                           JOIN data_karyawan dk ON u.id = dk.user_id
                                           JOIN jabatan j ON j.id = dk.jabatan_id
                                  WHERE dk.tipe_karyawan = 'harian/borongan'
                                    AND (u.fullname ILIKE :search OR
                                         dk.nip ILIKE :search)
                                  ORDER BY u.fullname),
                          filtered_borongan
                              AS (SELECT dab.user_id,
                                         ab.date::date  AS date,
                                         SUM(dab.total) AS upah
                                  FROM detail_absensi_borongan dab
                                           JOIN
                                       absensi_borongan ab ON dab.absensi_borongan_id = ab.id
                                  WHERE ab.status = 'Disetujui'
                                    AND ab.date::date BETWEEN :start_date AND :end_date
                                  GROUP BY dab.user_id, ab.date::date)
                     select pu.nip, pu.nama, pu.jabatan, c.calendar_date, COALESCE(fb.upah, 0) AS upah
                     FROM paginated_users pu
                              CROSS JOIN calendar c
                              LEFT JOIN filtered_borongan fb ON fb.user_id = pu.id AND fb.date = c.calendar_date
                     """)

        search_pattern = f"%{search}%"

        params = {
            'start_date': start_date,
            'end_date': end_date,
            'search': search_pattern
        }

        result = db.session.execute(query, params)

        return result.mappings().all()

    @staticmethod
    def generate_rekap_full(start_date, end_date):
        query_rekap = text("""
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
                                                                       ('Pulang Cepat',
                                                                        'Datang Terlambat & Pulang Cepat') AND
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
                                                               JOIN detail_jadwal_kerja djk
                                                                    ON jk.id = djk.jadwal_kerja_id
                                                                        AND djk.is_active = TRUE
                                                                        AND djk.hari =
                                                                            CAST(CASE EXTRACT(DOW FROM c.calendar_date)
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
                                                                 ON ew.user_id = i.user_id AND
                                                                    i.status = 'Disetujui' AND
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
                           WHERE dk.tipe_karyawan = 'bulanan'
                           ORDER BY u.fullname
                           """)

        query_terlambat = text("""
                               SELECT dk.nip,
                                      u.fullname  AS nama,
                                      j.nama      AS jabatan,
                                      jk.shift    AS jadwal_kerja,
                                      l.name      AS lokasi,
                                      a.date      as date_absensi,
                                      da.date     as waktu_absen,
                                      a.jadwal_time_in,
                                      COALESCE(ROUND(EXTRACT(epoch FROM da.date - (a.date + a.jadwal_time_in)) / 60, 2),
                                               0) AS menit_terlambat
                               FROM absensi a
                                        JOIN detail_absensi da ON a.id = da.absensi_id and da.type = 'IN'
                                        JOIN users u ON a.user_id = u.id
                                        JOIN data_karyawan dk ON u.id = dk.user_id
                                        JOIN jabatan j ON dk.jabatan_id = j.id
                                        JOIN jadwal_kerja jk ON a.jadwal_kerja_id = jk.id
                                        JOIN lokasi l ON dk.lokasi_id = l.id
                               WHERE a.status IN ('Datang Terlambat', 'Datang Terlambat & Pulang Cepat')
                                 AND a.date BETWEEN :start_date AND :end_date
                               ORDER BY a.date DESC
                               """)

        query_izin = db.session.query(
            DataKaryawan.nip,
            Users.fullname.label('nama'),
            JatahKuotaCuti.periode,
            func.sum(JatahKuotaCuti.sisa_kuota).label("sisa_cuti_tahunan"),
            func.sum(JatahKuotaCuti.kuota_awal).label("total_cuti_tahunan"),
            func.sum(JatahKuotaCuti.kuota_terpakai).label("cuti_tahunan_terpakai")
        ).select_from(JatahKuotaCuti).join(
            Users, JatahKuotaCuti.user_id == Users.id
        ).join(
            DataKaryawan, Users.id == DataKaryawan.user_id
        )

        query_izin = query_izin.filter(Users.is_active.is_(True))

        year = date.fromisoformat(start_date).year

        query_izin = query_izin.filter(JatahKuotaCuti.periode == year)

        query_izin = query_izin.group_by(
            Users.id,
            Users.fullname,
            DataKaryawan.nip,
            JatahKuotaCuti.periode,
        )

        query_izin = query_izin.order_by(DataKaryawan.nip.asc())

        params = {
            'start_date': start_date,
            'end_date': end_date,
        }

        result_rekap = db.session.execute(query_rekap, params)
        result_terlambat = db.session.execute(query_terlambat, params)
        result_izin = query_izin.all()

        result_rekap = result_rekap.mappings().all()
        result_terlambat = result_terlambat.mappings().all()

        return {
            "rekap": result_rekap,
            "terlambat": result_terlambat,
            "izin": result_izin,
        }
