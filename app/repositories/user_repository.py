from app.entity import Lokasi, Jabatan, UserRole
from app.entity.users import Users
from app.entity.data_karyawan import DataKaryawan
from app.entity.data_kontak import DataKontak
from app.entity.data_pribadi import DataPribadi
from app.database import db
from sqlalchemy import text
from werkzeug.security import generate_password_hash


class UserRepository:
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
            UserRole.name.label("role"),
            Lokasi.name.label("lokasi"),
            Jabatan.nama.label("jabatan")
        ).join(Users.data_karyawan).join(DataKaryawan.lokasi).join(DataKaryawan.jabatan).join(Users.user_role)

        query = query.filter(Users.is_active.is_(True))

        if search:
            query = query.filter(Users.fullname.ilike(f"%{search}%"))

        query = query.order_by(DataKaryawan.nip.asc())

        result = query.paginate(page=page, per_page=per_page, error_out=False)

        return result


    @staticmethod
    def get_user_by_id(user_id):
        return Users.query.filter_by(id=user_id, is_active=True).first()


    @staticmethod
    def get_user_by_username(username):
        return Users.query.filter_by(username=username, is_active=True).first()


    @staticmethod
    def create_user(fullname, username, password, data_pribadi, data_kontak, data_karyawan, nip):
        new_data_pribadi = DataPribadi(
            gender=data_pribadi['gender'],
            tmpt_lahir=data_pribadi['tmpt_lahir'],
            tgl_lahir=data_pribadi['tgl_lahir'],
            status_kawin=data_pribadi['status_kawin'],
            agama=data_pribadi['agama'],
            gol_darah=data_pribadi['gol_darah']
        )

        new_data_kontak = DataKontak(
            alamat=data_kontak['alamat'],
            no_telepon=data_kontak['no_telepon'],
            nama_darurat=data_kontak['nama_darurat'],
            no_telepon_darurat=data_kontak['no_telepon_darurat'],
            relasi_darurat=data_kontak['relasi_darurat'],
        )

        new_data_karyawan = DataKaryawan(
            nip=nip,
            tgl_gabung=data_karyawan['tgl_gabung'],
            tipe_karyawan=data_karyawan['tipe_karyawan'],
            lokasi_id=data_karyawan['lokasi_id'],
            jadwal_kerja_id=data_karyawan['jadwal_kerja_id'],
            jabatan_id=data_karyawan['jabatan_id'],
            user_pic_id=data_karyawan['user_pic_id']
        )

        new_user = Users(
            fullname=fullname,
            username=username,
            phone=data_kontak['no_telepon'],
            data_pribadi=new_data_pribadi,
            data_kontak=new_data_kontak,
            data_karyawan=new_data_karyawan,
            user_role_id='ea3cf287-fcb4-411e-a07a-f5b609f0e2b5'
        )

        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return new_user


    @staticmethod
    def update_user(user, data):
        user.fullname = data.get('fullname', user.fullname)

        if 'data_pribadi' in data and user.data_pribadi:
            data_pribadi_update = data['data_pribadi']
            user.data_pribadi.gender = data_pribadi_update.get('gender', user.data_pribadi.gender)
            user.data_pribadi.tmpt_lahir = data_pribadi_update.get('tmpt_lahir', user.data_pribadi.tmpt_lahir)
            user.data_pribadi.tgl_lahir = data_pribadi_update.get('tgl_lahir', user.data_pribadi.tgl_lahir)
            user.data_pribadi.status_kawin = data_pribadi_update.get('status_kawin', user.data_pribadi.status_kawin)
            user.data_pribadi.agama = data_pribadi_update.get('agama', user.data_pribadi.agama)
            user.data_pribadi.gol_darah = data_pribadi_update.get('gol_darah', user.data_pribadi.gol_darah)

        if 'data_kontak' in data and user.data_kontak:
            data_kontak_update = data['data_kontak']
            user.data_kontak.alamat = data_kontak_update.get('alamat', user.data_kontak.alamat)
            user.data_kontak.no_telepon = data_kontak_update.get('no_telepon', user.data_kontak.no_telepon)
            user.data_kontak.nama_darurat = data_kontak_update.get('nama_darurat', user.data_kontak.nama_darurat)
            user.data_kontak.no_telepon_darurat = data_kontak_update.get('no_telepon_darurat',
                                                                         user.data_kontak.no_telepon_darurat)
            user.data_kontak.relasi_darurat = data_kontak_update.get('relasi_darurat', user.data_kontak.relasi_darurat)
            user.phone = user.data_kontak.no_telepon

        if 'data_karyawan' in data and user.data_karyawan:
            data_karyawan_update = data['data_karyawan']
            user.data_karyawan.tgl_gabung = data_karyawan_update.get('tgl_gabung', user.data_karyawan.tgl_gabung)
            user.data_karyawan.tipe_karyawan = data_karyawan_update.get('tipe_karyawan',
                                                                        user.data_karyawan.tipe_karyawan)
            user.data_karyawan.lokasi_id = data_karyawan_update.get('lokasi_id', user.data_karyawan.lokasi_id)
            user.data_karyawan.jadwal_kerja_id = data_karyawan_update.get('jadwal_kerja_id',
                                                                          user.data_karyawan.jadwal_kerja_id)
            user.data_karyawan.jabatan_id = data_karyawan_update.get('jabatan_id', user.data_karyawan.jabatan_id)
            user.data_karyawan.user_pic_id = data_karyawan_update.get('user_pic_id', user.data_karyawan.user_pic_id)
        db.session.commit()
        return user


    @staticmethod
    def non_active_user(user):
        user.is_active = False
        db.session.commit()


    @staticmethod
    def get_posible_pic(jabatan_id):
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
                              join users u on u.data_karyawan_id = dk.id
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

        db.session.commit()

    @staticmethod
    def change_password(user, password):
        user.password = generate_password_hash(password)
        db.session.commit()
