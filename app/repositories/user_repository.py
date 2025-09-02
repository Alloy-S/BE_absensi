from app.services.encryption_service import EncryptionServiceAES256
from app.utils.app_constans import AppConstants
from app.entity import Lokasi, Jabatan, UserRole, JatahKuotaCuti, ApprovalKoreksi, ApprovalIzin, ApprovalLembur, \
    ApprovalAbsensiBorongan, ApprovalReimburse, Roles
from app.entity.users import Users
from app.entity.data_karyawan import DataKaryawan
from app.entity.data_kontak import DataKontak
from app.entity.data_pribadi import DataPribadi
from app.database import db
from sqlalchemy import text, func
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload
from sqlalchemy import union_all, literal_column, or_


class UserRepository:
    @staticmethod
    def get_all_active_users():
        return Users.query.join(Users.data_karyawan).filter(Users.is_active == True).all()

    @staticmethod
    def get_all_active_bulanan_users():
        return Users.query.join(Users.data_karyawan).filter(Users.is_active == True, DataKaryawan.tipe_karyawan == 'bulanan').all()

    @staticmethod
    def get_all_users():
        query = db.session.query(
            Users.id,
            Users.fullname,
            Users.username,
            UserRole.name.label("role"),
            Lokasi.name.label("lokasi"),
            Jabatan.nama.label("jabatan")
        ).join(Users.data_karyawan).join(DataKaryawan.lokasi).join(DataKaryawan.jabatan).join(Users.user_role)

        query = query.filter(Users.is_active.is_(True))

        result = query.all()

        return result

    @staticmethod
    def get_users_pagination(page: int = 1, per_page: int = 10, search: str = None):
        query = db.session.query(
            Users.id,
            Users.fullname,
            Users.username,
            Users.is_active,
            Lokasi.name.label("lokasi"),
            Jabatan.nama.label("jabatan"),
            DataKaryawan.tipe_karyawan
        ).join(Users.data_karyawan).join(DataKaryawan.lokasi).join(DataKaryawan.jabatan)

        query = query.filter(Users.is_active.is_(True))

        if search:
            query = query.filter(Users.fullname.ilike(f"%{search}%"))

        query = query.order_by(DataKaryawan.nip.asc())

        result = query.paginate(page=page, per_page=per_page, error_out=False)

        return result

    @staticmethod
    def get_users_pagination_kuota_cuti(page: int = 1, per_page: int = 10, search: str = None):
        query = db.session.query(
            Users.id,
            Users.fullname,
            func.sum(JatahKuotaCuti.sisa_kuota).label("sisa_cuti_tahunan"),
            func.sum(JatahKuotaCuti.kuota_awal).label("total_cuti_tahunan")
        ).outerjoin(Users.jatah_kuota_cuti)

        query = query.join(Users.data_karyawan)

        query = query.filter(Users.is_active.is_(True), DataKaryawan.tipe_karyawan == 'bulanan')
        if search:
            query = query.filter(Users.fullname.ilike(f"%{search}%"))

        query = query.group_by(
            Users.id,
            Users.fullname,
            DataKaryawan.nip
        )

        query = query.order_by(DataKaryawan.nip.asc())

        return query.paginate(page=page, per_page=per_page, error_out=False)


    @staticmethod
    def get_user_by_id(user_id):
        return Users.query.filter_by(id=user_id, is_active=True).first()


    @staticmethod
    def get_user_by_username(username):
        query = Users.query.options(
            joinedload(Users.user_role)
        ).filter_by(username=username, is_active=True)

        return query.first()

    @staticmethod
    def create_user_admin(fullname, username, password, phone):

        new_user = Users(
            fullname=fullname,
            username=username,
            phone=EncryptionServiceAES256.encrypt(phone),
            user_role_id='11c155e7-a480-4697-9bc5-513cb2579b03'
        )

        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def create_user(fullname, username, password, data_pribadi, data_kontak, data_karyawan, nip):
        phone_user = EncryptionServiceAES256.encrypt(data_kontak['no_telepon'])

        new_data_pribadi = DataPribadi(
            gender=data_pribadi['gender'],
            tmpt_lahir=data_pribadi['tmpt_lahir'],
            tgl_lahir=EncryptionServiceAES256.encrypt(data_pribadi['tgl_lahir']),
            status_kawin=data_pribadi['status_kawin'],
            agama=data_pribadi['agama'],
            gol_darah=data_pribadi['gol_darah']
        )

        new_data_kontak = DataKontak(
            alamat=EncryptionServiceAES256.encrypt(data_kontak['alamat']),
            no_telepon=phone_user,
            nama_darurat=data_kontak['nama_darurat'],
            no_telepon_darurat=EncryptionServiceAES256.encrypt(data_kontak['no_telepon_darurat']),
            relasi_darurat=data_kontak['relasi_darurat'],
        )

        new_data_karyawan = DataKaryawan(
            nip=nip,
            tgl_gabung=data_karyawan['tgl_gabung'],
            tipe_karyawan=data_karyawan['tipe_karyawan'],
            gaji_pokok=data_karyawan['gaji_pokok'],
            face_recognition_mode=data_karyawan['face_recognition_mode'],
            lokasi_id=data_karyawan['lokasi_id'],
            jadwal_kerja_id=data_karyawan['jadwal_kerja_id'],
            jabatan_id=data_karyawan['jabatan_id'],
            user_pic_id=data_karyawan['user_pic_id'],
            grup_gaji_id=data_karyawan['grup_gaji_id']
        )

        new_user = Users(
            fullname=fullname,
            username=username,
            phone=phone_user,
            data_pribadi=new_data_pribadi,
            data_kontak=new_data_kontak,
            data_karyawan=new_data_karyawan
        )

        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()

        new_user_role = UserRole(
            user_id=new_user.id,
            role_id=1
        )

        db.session.add(new_user_role)

        db.session.commit()

        return new_user


    @staticmethod
    def update_user(user, data):
        user.fullname = data.get('fullname', user.fullname)

        if 'data_pribadi' in data and user.data_pribadi:
            data_pribadi_update = data['data_pribadi']
            user.data_pribadi.gender = data_pribadi_update.get('gender', user.data_pribadi.gender)
            user.data_pribadi.tmpt_lahir = data_pribadi_update.get('tmpt_lahir', user.data_pribadi.tmpt_lahir)
            user.data_pribadi.tgl_lahir = EncryptionServiceAES256.encrypt(data_pribadi_update.get('tgl_lahir', user.data_pribadi.tgl_lahir))
            user.data_pribadi.status_kawin = data_pribadi_update.get('status_kawin', user.data_pribadi.status_kawin)
            user.data_pribadi.agama = data_pribadi_update.get('agama', user.data_pribadi.agama)
            user.data_pribadi.gol_darah = data_pribadi_update.get('gol_darah', user.data_pribadi.gol_darah)

        if 'data_kontak' in data and user.data_kontak:
            data_kontak_update = data['data_kontak']
            user.data_kontak.alamat = EncryptionServiceAES256.encrypt(data_kontak_update.get('alamat', user.data_kontak.alamat))
            user.data_kontak.no_telepon = EncryptionServiceAES256.encrypt(data_kontak_update.get('no_telepon', user.data_kontak.no_telepon))
            user.data_kontak.nama_darurat = data_kontak_update.get('nama_darurat', user.data_kontak.nama_darurat)
            user.data_kontak.no_telepon_darurat = EncryptionServiceAES256.encrypt(data_kontak_update.get('no_telepon_darurat',
                                                                         user.data_kontak.no_telepon_darurat))
            user.data_kontak.relasi_darurat = data_kontak_update.get('relasi_darurat', user.data_kontak.relasi_darurat)
            user.phone = user.data_kontak.no_telepon

        if 'data_karyawan' in data and user.data_karyawan:
            data_karyawan_update = data['data_karyawan']
            user.data_karyawan.tgl_gabung = data_karyawan_update.get('tgl_gabung', user.data_karyawan.tgl_gabung)
            user.data_karyawan.tgl_resign = data_karyawan_update.get('tgl_resign', user.data_karyawan.tgl_resign)
            user.data_karyawan.tipe_karyawan = data_karyawan_update.get('tipe_karyawan',
                                                                        user.data_karyawan.tipe_karyawan)
            user.data_karyawan.lokasi_id = data_karyawan_update.get('lokasi_id', user.data_karyawan.lokasi_id)
            user.data_karyawan.jadwal_kerja_id = data_karyawan_update.get('jadwal_kerja_id',
                                                                          user.data_karyawan.jadwal_kerja_id)
            user.data_karyawan.jabatan_id = data_karyawan_update.get('jabatan_id', user.data_karyawan.jabatan_id)
            user.data_karyawan.user_pic_id = data_karyawan_update.get('user_pic_id', user.data_karyawan.user_pic_id)
            user.data_karyawan.grup_gaji_id = data_karyawan_update.get('grup_gaji_id', user.data_karyawan.grup_gaji_id)
            user.data_karyawan.gaji_pokok = data_karyawan_update.get('gaji_pokok', user.data_karyawan.gaji_pokok)
            user.data_karyawan.face_recognition_mode = data_karyawan_update.get('face_recognition_mode', user.data_karyawan.face_recognition_mode)
        db.session.commit()
        return user

    @staticmethod
    def edit_data_pribadi(user, data):
        user.data_pribadi.gender = data.get('gender', user.data_pribadi.gender)
        user.data_pribadi.tmpt_lahir = data.get('tmpt_lahir', user.data_pribadi.tmpt_lahir)
        user.data_pribadi.tgl_lahir = EncryptionServiceAES256.encrypt(data.get('tgl_lahir', user.data_pribadi.tgl_lahir))
        user.data_pribadi.status_kawin = data.get('status_kawin', user.data_pribadi.status_kawin)
        user.data_pribadi.agama = data.get('agama', user.data_pribadi.agama)
        user.data_pribadi.gol_darah = data.get('gol_darah', user.data_pribadi.gol_darah)

        db.session.commit()

    @staticmethod
    def edit_data_kontak(user, data):
        user.data_kontak.alamat = EncryptionServiceAES256.encrypt(data.get('alamat', user.data_kontak.alamat))
        user.data_kontak.no_telepon = EncryptionServiceAES256.encrypt(data.get('no_telepon', user.data_kontak.no_telepon))
        user.data_kontak.nama_darurat = data.get('nama_darurat', user.data_kontak.nama_darurat)
        user.data_kontak.no_telepon_darurat = EncryptionServiceAES256.encrypt(data.get('no_telepon_darurat',
                                                                     user.data_kontak.no_telepon_darurat))
        user.data_kontak.relasi_darurat = data.get('relasi_darurat', user.data_kontak.relasi_darurat)
        user.phone = user.data_kontak.no_telepon

        db.session.commit()

    @staticmethod
    def non_active_user(user):
        user.is_active = False
        db.session.commit()


    @staticmethod
    def get_posible_pic(jabatan_id):
        check_query = text("SELECT parent_id FROM jabatan WHERE id = :jabatan_id")
        jabatan = db.session.execute(check_query, {'jabatan_id': jabatan_id}).first()

        if not jabatan or jabatan.parent_id is None:
            return []

        query = text("""
                     WITH RECURSIVE atasan AS (SELECT id, nama, parent_id
                                               FROM jabatan
                                               WHERE id = :jabatan_id
    
                                               UNION ALL
    
                                               SELECT j.id, j.nama, j.parent_id
                                               FROM jabatan j
                                                        INNER JOIN atasan a ON j.id = a.parent_id)
                     SELECT u.fullname, u.id, a.nama as jabatan
                     FROM atasan a
                              join data_karyawan dk on dk.jabatan_id = a.id
                              join users u on u.id = dk.user_id
                     where a.id != :jabatan_id and u.is_active is true
                     """)

        result = db.session.execute(query, {'jabatan_id': jabatan_id})

        users = result.mappings().all()
        users = [dict(row) for row in users]
        return users

    @staticmethod
    def mark_done_notif_login(user):
        user.is_notif_login_send = True

        db.session.commit()

    @staticmethod
    def mark_done_register_face(user):
        user.is_face_registration_required = False


    @staticmethod
    def change_password(user, password):
        user.password = generate_password_hash(password)
        db.session.commit()

    @staticmethod
    def get_users_by_pic(pic_user_id):

        query = db.session.query(
            Users.id,
            Users.fullname,
            DataKaryawan.nip,
            Jabatan.nama.label('jabatan')
        ).join(
            DataKaryawan, Users.id == DataKaryawan.user_id
        ).outerjoin(
            Jabatan, DataKaryawan.jabatan_id == Jabatan.id
        ).filter(
            DataKaryawan.user_pic_id == pic_user_id,
            Users.is_active.is_(True)
        ).order_by(
            Users.fullname.asc()
        )

        return query.all()

    @staticmethod
    def update_fcm_token(user, fcm_token):
        user.fcm_token = fcm_token

        db.session.commit()

    @staticmethod
    def delete_fcm_token(user):
        user.fcm_token = None

        db.session.commit()

    @staticmethod
    def get_all_approval_status_waiting(user_id, filter_tipe_approval, page=1, size=10):

        q_koreksi = db.session.query(
            ApprovalKoreksi.id.label('approval_id'),
            ApprovalKoreksi.created_date.label('tanggal_pengajuan'),
            literal_column("'Koreksi Kehadiran'").label('tipe_approval'),
            ApprovalKoreksi.status.label('status'),
            Users.fullname.label('user')
        ).join(
            Users, ApprovalKoreksi.user_id == Users.id
        ).filter(
            ApprovalKoreksi.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalKoreksi.approval_user_id == user_id
        )

        q_izin = db.session.query(
            ApprovalIzin.id.label('approval_id'),
            ApprovalIzin.created_date.label('tanggal_pengajuan'),
            literal_column("'Izin'").label('tipe_approval'),
            ApprovalIzin.status.label('status'),
            Users.fullname.label('user')
        ).join(
            Users, ApprovalIzin.user_id == Users.id
        ).filter(
            ApprovalIzin.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalIzin.approval_user_id == user_id
        )

        q_lembur = db.session.query(
            ApprovalLembur.id.label('approval_id'),
            ApprovalLembur.created_date.label('tanggal_pengajuan'),
            literal_column("'Lembur'").label('tipe_approval'),
            ApprovalLembur.status.label('status'),
            Users.fullname.label('user')
        ).join(
            Users, ApprovalLembur.user_id == Users.id
        ).filter(
            ApprovalLembur.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalLembur.approval_user_id == user_id
        )

        q_borongan = db.session.query(
            ApprovalAbsensiBorongan.id.label('approval_id'),
            ApprovalAbsensiBorongan.created_date.label('tanggal_pengajuan'),
            literal_column("'Absensi Borongan'").label('tipe_approval'),
            ApprovalAbsensiBorongan.status.label('status'),
            Users.fullname.label('user')
        ).join(
            Users, ApprovalAbsensiBorongan.user_id == Users.id
        ).filter(
            ApprovalAbsensiBorongan.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalAbsensiBorongan.approval_user_id == user_id
        )

        q_reimburse = db.session.query(
            ApprovalReimburse.id.label('approval_id'),
            ApprovalReimburse.created_date.label('tanggal_pengajuan'),
            literal_column("'Reimburse'").label('tipe_approval'),
            ApprovalReimburse.status.label('status'),
            Users.fullname.label('user')
        ).join(
            Users, ApprovalReimburse.user_id == Users.id
        ).filter(
            ApprovalReimburse.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalReimburse.approval_user_id == user_id
        )

        all_queries = {
            "Koreksi Kehadiran": q_koreksi,
            "Izin": q_izin,
            "Lembur": q_lembur,
            "Absensi Borongan": q_borongan,
            "Reimburse": q_reimburse
        }

        queries_to_union = []
        if filter_tipe_approval and filter_tipe_approval.lower() != AppConstants.APPROVAL_STATUS_ALL.value:
            if filter_tipe_approval in all_queries:
                queries_to_union.append(all_queries[filter_tipe_approval])
        else:
            queries_to_union = list(all_queries.values())

        if not queries_to_union:
            return {
                "items": [], "total": 0, "page": page
            }

        query = union_all(*queries_to_union).subquery("approvals")

        total_query = db.session.query(func.count()).select_from(query)
        total = total_query.scalar()

        final_query = db.session.query(query).order_by(
            query.c.tanggal_pengajuan.desc()
        ).limit(size).offset((page - 1) * size)

        items = final_query.all()

        return {
            "items": items,
            "total": total,
            "pages": (total + size - 1) // size
        }

    @staticmethod
    def find_user_by_username_or_name(search):

        search_keyword = f"%{search}%"

        query = db.session.query(
            Users
        ).filter(
            or_(
                Users.username.ilike(search_keyword),
                Users.fullname.ilike(search_keyword),
            ),
            Users.is_active.is_(True),
        )

        return query.all()
