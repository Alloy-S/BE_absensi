from app.repositories.rekap_periode_repository import RekapPeriodeRepository

class RekapPeriodeService:

    @staticmethod
    def rekap_periode(request):
        return RekapPeriodeRepository.generate_laporan_periode(request.get('start_date'), request.get('end_date'), request.get('search'), request.get('page'), request.get('size'))