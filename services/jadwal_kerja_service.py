from repositories.jadwal_kerja_repository import JadwalKerjaRepository

class JadwalKerjaService:
    @staticmethod
    def get_all():
        return JadwalKerjaRepository.get_all()
    
    @staticmethod
    def get_by_id(id):
        return JadwalKerjaRepository.get_by_id(id);
    
    @staticmethod
    def create(shift, timeIn, timeOut, tolerIn, tolerOut):
        jadwal = JadwalKerjaRepository.get_by_name(shift=shift)
    
        if jadwal:
            return None
        return JadwalKerjaRepository.create(shift, timeIn, timeOut, tolerIn, tolerOut);
    
    @staticmethod
    def update(id, shift, timeIn, timeOut, tolerIn, tolerOut):
        jadwal = JadwalKerjaRepository.get_by_id(id)
        if not jadwal:
            return None
        return JadwalKerjaRepository.update(jadwal, shift, timeIn, timeOut, tolerIn, tolerOut);
    
    @staticmethod
    def delete(id):
        jadwal = JadwalKerjaRepository.get_by_id(id)
        if not jadwal:
            return None
        JadwalKerjaRepository.delete(jadwalKerja=jadwal)
        return True