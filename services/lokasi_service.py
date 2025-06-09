from repositories.lokasi_repository import LokasiRepository

class LokasiService:
    @staticmethod
    def get_all_lokasi():
        return LokasiRepository.get_all_lokasi()

    @staticmethod
    def get_all_lokasi_pagination(page, size, search):
        return LokasiRepository.get_all_pagination(page=page, per_page=size, search=search)
    
    @staticmethod
    def get_lokasi_by_id(id):
        return LokasiRepository.get_lokasi_by_id(id)
    
    @staticmethod
    def create_lokasi(name , latitude, longitude, toleransi):
        print("========== ADD NEW LOKASI")
        lokasi = LokasiRepository.get_lokasi_by_name(name=name)
        
        if lokasi:
            return None
        return LokasiRepository.create_lokasi(name , latitude, longitude, toleransi);
    
    @staticmethod
    def update_lokasi(id, name, latitude, longitude, toleransi):
        lokasi = LokasiRepository.get_lokasi_by_id(id)
        if not lokasi:
            return None
        return LokasiRepository.update_lokasi(lokasi, name, latitude, longitude, toleransi);
    
    @staticmethod
    def delete_lokasi(id):
        lokasi = LokasiRepository.get_lokasi_by_id(id)
        if not lokasi:
            return None
        LokasiRepository.delete_lokasi(lokasi)
        return True