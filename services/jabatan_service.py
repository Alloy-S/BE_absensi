from repositories.jabatan_repository import JabatanRepository

class JabatanService:
    @staticmethod
    def get_all_pagination(page, size, search):
        print("Fetching all Jabatan service")
        return JabatanRepository.get_all_pagination(page=page, per_page=size, search=search)
    
    @staticmethod
    def get_all():
        return JabatanRepository.get_all()
    
    @staticmethod
    def create(nama, parent_id):
        
        jabatan = JabatanRepository.get_by_name(nama)
        
        if jabatan:
            return None
        
        return JabatanRepository.create(nama=nama, parent_id=parent_id)
    
    @staticmethod
    def get_by_id(id):
        return JabatanRepository.get_by_id(id)
    
    @staticmethod
    def update(id, nama, parent_id):
        
        if JabatanRepository.get_by_name(nama):
            return None
        
        jabatan = JabatanRepository.get_by_id(id)
        
        if not jabatan:
            return None
        
        jabatan = JabatanRepository.update(id, nama, parent_id)
        
        return jabatan
    
    @staticmethod
    def delete(id):

        return JabatanRepository.delete(id)