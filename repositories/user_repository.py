from entity.users import Users
from entity.data_karyawan import DataKaryawan
from entity.data_kontak import DataKontak
from entity.data_pribadi import DataPribadi
from database import db
from sqlalchemy import text

class UserRepository:
    @staticmethod
    def get_all_users():
        return Users.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return Users.query.filter_by(id=user_id).first()
    
    @staticmethod
    def get_user_by_username(username):
        return Users.query.filter_by(username=username).first()

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
            jabatan_id=data_karyawan['jabatan_id']
        )

        new_user = Users(
            fullname=fullname,
            username=username,
            phone=data_kontak['no_telepon'],
            data_pribadi=new_data_pribadi,
            data_kontak=new_data_kontak,
            data_karyawan=new_data_karyawan
        )

        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def update_user(user, name, email):
        user.name = name
        user.email = email
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def get_posible_pic(jabatan_id):
        query = text("""
            WITH RECURSIVE atasan AS (
                SELECT id, nama, parent_id
                FROM jabatan
                WHERE id = :jabatan_id

                UNION ALL

                SELECT j.id, j.nama, j.parent_id
                FROM jabatan j
                INNER JOIN atasan a ON j.id = a.parent_id
            )
            SELECT u.fullname, a.id, a.nama as jabatan FROM atasan a
            join data_karyawan dk on dk.jabatan_id=a.id
            join users u on u.data_karyawan_id=dk.id
            where a.id != :jabatan_id
        """)

        result = db.session.execute(query, {'jabatan_id': jabatan_id})

        users = result.mappings().all()
        users = [dict(row) for row in users]
        return users

