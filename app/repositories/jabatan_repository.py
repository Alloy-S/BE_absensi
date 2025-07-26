from app.entity.jabatan import Jabatan
from app.database import db
from sqlalchemy import or_

class JabatanRepository:

    @staticmethod
    def get_all_pagination(page: int = 1, per_page: int = 10, search: str = None):
        print(f"Fetching all Jabatan with pagination: page={page}, per_page={per_page}, search={search}")

        parent = db.aliased(Jabatan)

        query = db.session.query(
            Jabatan.id,
            Jabatan.nama,
            parent.nama.label('parent_name')
        ).select_from(Jabatan)
        query = query.outerjoin(parent, Jabatan.parent_id == parent.id)

        if search:
            query = query.filter(Jabatan.nama.ilike(f"%{search}%"))
            
        query = query.order_by(Jabatan.nama.asc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination
    
    @staticmethod
    def get_all():
        print(f"Fetching all Jabatan")

        query = db.session.query(
            Jabatan.id,
            Jabatan.nama
        )

        query = query.order_by(Jabatan.nama.asc())
        
        result = query.all()

        return result

    @staticmethod
    def get_by_id(id) -> Jabatan:
        return Jabatan.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_name(name) -> Jabatan:
        return Jabatan.query.filter_by(nama=name).first()

    @staticmethod
    def get_by_name_and_jabatan_id(name, jabatan_id) -> Jabatan:
        return db.session.query(
            Jabatan.id,
        ).filter(
            or_(
                Jabatan.nama == name,
                Jabatan.id == jabatan_id
            )
        )
    
    @staticmethod
    def create(nama, parent_id) -> Jabatan:
        jabatan = Jabatan(nama=nama, parent_id=parent_id)
        db.session.add(jabatan)
        db.session.commit()
        return jabatan
    
    @staticmethod
    def update_jabatan(jabatan, nama, parent_id) -> Jabatan:
        jabatan.nama = nama
        jabatan.parent_id = parent_id
        
        db.session.commit()
        
        return jabatan
    
    @staticmethod
    def delete_jabatan(jabatan) -> bool:

        db.session.delete(jabatan)
        db.session.commit()
        
        return True
