from repositories.jadwal_kerja_repository import JadwalKerjaRepository

class JadwalKerjaService:
    @staticmethod
    def get_all():
        return JadwalKerjaRepository.get_all()

    @staticmethod
    def get_all_pagination(page, size, search):
        return JadwalKerjaRepository.get_all_pagination(page=page, size=size, search=search)
    
    @staticmethod
    def get_by_id(id):
        return JadwalKerjaRepository.get_by_id(id)
    
    @staticmethod
    def create(kode, shift, details: list):
        jadwal = JadwalKerjaRepository.get_by_kode(kode=kode)
    
        if jadwal:
            return None
        return JadwalKerjaRepository.create(kode, shift, details)
    
    @staticmethod
    def update(id, kode, shift, details: list):
        jadwal = JadwalKerjaRepository.get_by_id(id)
        if not jadwal:
            return None
        return JadwalKerjaRepository.update(jadwal, kode, shift, details)
    
    @staticmethod
    def delete(id):
        jadwal = JadwalKerjaRepository.get_by_id(id)
        if not jadwal:
            return None
        JadwalKerjaRepository.delete(jadwalKerja=jadwal)
        return True