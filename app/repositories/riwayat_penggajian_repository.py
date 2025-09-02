from app.database import db
from datetime import datetime

from app.entity import RiwayatPenggajian, RiwayatPenggajianDetail, RiwayatPenggajianRincian, GrupGaji


class RiwayatPenggajianRepository:

    @staticmethod
    def create_draft_riwayat_penggajian(data):
        try:
            new_riwayat = RiwayatPenggajian(
                grup_gaji_id=data['grup_gaji_id'],
                periode_start=data['periode_start'],
                periode_end=data['periode_end'],
                status='DRAFT',
                total_karyawan=data['total_karyawan'],
                total_gaji_keseluruhan=data['total_gaji_keseluruhan'],
                created_by=data['created_by']
            )

            for hasil_karyawan in data['hasil_karyawan']:
                new_detail = RiwayatPenggajianDetail(
                    user_id=hasil_karyawan['user_id'],
                    total_tunjangan=hasil_karyawan['total_tunjangan'],
                    total_potongan=hasil_karyawan['total_potongan'],
                    gaji=hasil_karyawan['gaji']
                )
                for rincian in hasil_karyawan['rincian']:
                    new_rincian = RiwayatPenggajianRincian(
                        komponen=rincian['komponen'],
                        tipe=rincian['tipe'],
                        jumlah=rincian['jumlah'],
                        nilai_a=rincian['nilai_a'],
                        nilai_b=rincian['nilai_b'],
                        operasi=rincian['operasi'],
                    )
                    new_detail.riwayat_penggajian_rincian.append(new_rincian)

                new_riwayat.riwayat_penggajian_detail.append(new_detail)

            db.session.add(new_riwayat)
            db.session.commit()

            return new_riwayat.id

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def finalisasi_riwayat_penggajian(riwayat_penggajian):

        riwayat_penggajian.status = 'FINAL'
        riwayat_penggajian.date_updated = datetime.now()

        db.session.commit()
        return riwayat_penggajian

    @staticmethod
    def get_riwayat_penggajian_by_id(riwayat_id):
        return RiwayatPenggajian.query.filter_by(id=riwayat_id).first()

    @staticmethod
    def get_riwayat_penggajian_pagination(page=1, size=10, periode_start=None, periode_end=None, grup_gaji_id=None, status=None):
        query = db.session.query(
            RiwayatPenggajian.id,
            RiwayatPenggajian.periode_start,
            RiwayatPenggajian.periode_end,
            RiwayatPenggajian.status,
            GrupGaji.grup_name,
        ).join(GrupGaji, RiwayatPenggajian.grup_gaji_id == GrupGaji.id)

        if periode_start:
            query = query.filter(periode_start >= RiwayatPenggajian.periode_start)
        if periode_end:
            query = query.filter(periode_end <= RiwayatPenggajian.periode_end)

        if grup_gaji_id:
            query = query.filter(RiwayatPenggajian.grup_gaji_id == grup_gaji_id)

        if status and status in ['DRAFT', 'FINAL']:
            query = query.filter(RiwayatPenggajian.status == status)

        query = query.order_by(RiwayatPenggajian.date_created.asc())

        pagination = query.paginate(page=page, per_page=size, error_out=False)

        return pagination

    @staticmethod
    def delete_riwayat_penggajian(riwayat):
        db.session.delete(riwayat)
        db.session.commit()






