from app.entity import HargaHarianBorongan
from app.database import db

class HargaHarianBoronganRepository:

    @staticmethod
    def get_harga_pagination(page: int = 1, size: int = 10, search: str = None):
        query = db.session.query(
            HargaHarianBorongan
        )

        query = query.filter(HargaHarianBorongan.is_deleted.is_(False))

        if search:
            query = query.filter(HargaHarianBorongan.nama.ilike(f"%{search}%"))

        query = query.order_by(HargaHarianBorongan.nama.asc())

        pagination = query.paginate(page=page, per_page=size, error_out=False)

        return pagination

    @staticmethod
    def get_harga_by_id(harga_id):
        return HargaHarianBorongan.query.filter_by(id=harga_id).first()

    @staticmethod
    def get_harga_by_harga_grup(harga_grup):
        return HargaHarianBorongan.query.filter_by(harga_grup=harga_grup).order_by(HargaHarianBorongan.date.desc()).all()

    @staticmethod
    def create_harga(data):
        new_harga = HargaHarianBorongan(
            nama=data['nama'],
            harga_normal=data['harga_normal'],
            harga_lembur=data['harga_lembur'],
            jam_start_normal=data['jam_start_normal'],
            jam_end_normal=data['jam_end_normal'],
            toleransi_waktu=data['toleransi_waktu'],
            type=data['type'],
        )

        db.session.add(new_harga)
        db.session.flush()
        return new_harga

    @staticmethod
    def update_harga(data):
        new_harga = HargaHarianBorongan(
            nama=data['nama'],
            harga_normal=data['harga_normal'],
            harga_lembur=data['harga_lembur'],
            jam_start_normal=data['jam_start_normal'],
            jam_end_normal=data['jam_end_normal'],
            toleransi_waktu=data['toleransi_waktu'],
            grup_id=data['grup_id'],
            type=data['type'],
        )

        db.session.add(new_harga)
        db.session.flush()
        return new_harga


    @staticmethod
    def non_active_harga(harga):
        harga.is_deleted = True


    @staticmethod
    def get_all_harga_active():
        query = db.session.query(
            HargaHarianBorongan
        )

        query = query.filter(
            HargaHarianBorongan.is_deleted.is_(False)
        )

        query = query.order_by(HargaHarianBorongan.grup_id)

        return query.all()


