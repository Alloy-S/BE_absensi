from app.database import db
from app.entity import GrupGaji, GrupGajiKom, Users, DataKaryawan, Jabatan
from sqlalchemy import text, func, or_

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
                nilai_statis=kom_data.get('nilai_statis'),
                use_nilai_dinamis=kom_data.get('use_nilai_dinamis', False),
                kode_nilai_dinamis=kom_data.get('kode_nilai_dinamis'),
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
            Users.id,
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

    @staticmethod
    def get_grup_gaji_detail_by_id(grup_gaji_id):

        query = text("""
                     SELECT gg.grup_kode,
                            gg.grup_name,
                            kg.kom_name,
                            kg.no_urut,
                            kg.tipe,
                            ggk.use_kondisi,
                            ggk.kode_kondisi,
                            ggk.min_kondisi,
                            ggk.max_kondisi,
                            ggk.use_formula,
                            ggk.kode_formula,
                            ggk.operation_sum,
                            ggk.nilai_statis,
                            ggk.use_nilai_dinamis,
                            ggk.kode_nilai_dinamis
                     FROM grup_gaji gg
                              JOIN grup_gaji_kom ggk ON gg.id = ggk.grp_id
                              JOIN komponen_gaji kg ON ggk.kom_id = kg.id
                     WHERE gg.id = :grup_gaji_id
                     order by kg.no_urut, ggk.min_kondisi;
                     """)

        result = db.session.execute(query, {'grup_gaji_id': grup_gaji_id})

        return result.mappings().all()