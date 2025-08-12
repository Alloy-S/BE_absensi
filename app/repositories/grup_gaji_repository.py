from app.database import db
from app.entity import GrupGaji, GrupGajiKom, Users, DataKaryawan, Jabatan


class GrupGajiRepository:
    @staticmethod
    def get_all_grup_gaji_paginated(page=1, size=10, search=None):
        query = GrupGaji.query
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(GrupGaji.grup_name.ilike(search_pattern))

        return query.order_by(GrupGaji.grup_kode.asc()).paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_grup_gaji_by_id(grup_id):
        return GrupGaji.query.options(db.joinedload(GrupGaji.grup_gaji_kom)).filter_by(id=grup_id).first()

    @staticmethod
    def create_grup_gaji(data):
        new_grup_gaji = GrupGaji(grup_kode=data['grup_kode'], grup_name=data['grup_name'])
        db.session.add(new_grup_gaji)
        db.session.flush()
        return new_grup_gaji

    @staticmethod
    def update_grup_gaji(grup_gaji, data):
        grup_gaji.grup_kode = data['grup_kode']
        grup_gaji.grup_name = data['grup_name']
        return grup_gaji

    @staticmethod
    def delete_grup_gaji(grup_gaji):
        GrupGajiKom.query.filter_by(grp_id=grup_gaji.id).delete()
        db.session.delete(grup_gaji)

    @staticmethod
    def delete_and_insert_grup_gaji_kom(grup_gaji, komponen_data):

        GrupGajiKom.query.filter_by(grp_id=grup_gaji.id).delete()

        for kom_data in komponen_data:
            new_kom = GrupGajiKom(
                grp_id=grup_gaji.id,
                kom_id=kom_data['kom_id'],
                use_kondisi=kom_data.get('use_kondisi', False),
                kode_kondisi=kom_data.get('kode_kondisi'),
                min_kondisi=kom_data.get('min_kondisi'),
                max_kondisi=kom_data.get('max_kondisi'),
                use_formula=kom_data.get('use_formula', False),
                kode_formula=kom_data.get('kode_formula'),
                operation_sum=kom_data.get('operation_sum'),
                nilai_uang=kom_data.get('nilai_uang', 0),
                hitung=kom_data.get('hitung')
            )
            db.session.add(new_kom)

    @staticmethod
    def get_grup_gaji_by_kode(kode):
        return GrupGaji.query.filter_by(grup_kode=kode).first()

    @staticmethod
    def get_all_grup_gaji():
        return GrupGaji.query.all()

    @staticmethod
    def get_grup_gaji_users(grup_gaji_id):
        query = ((db.session.query(
            Users.fullname,
            DataKaryawan.nip,
            Jabatan.nama.label('jabatan')
        ).select_from(Users)
                 .join(DataKaryawan, Users.id == DataKaryawan.user_id))
                 .join(Jabatan, Jabatan.id == DataKaryawan.jabatan_id))

        query = query.filter(
            Users.is_active == True,
            DataKaryawan.grup_gaji_id == grup_gaji_id
        )

        result = query.order_by(DataKaryawan.nip).all()

        return result