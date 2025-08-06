from app.repositories.laporan_repository import LaporanRepository


class LaporanService:

    @staticmethod
    def rekap_periode(request):
        return LaporanRepository.generate_laporan_periode(request.get('start_date'), request.get('end_date'),
                                                          request.get('search'), request.get('page'),
                                                          request.get('size'))

    @staticmethod
    def laporan_datang_terlambat(request):
        return LaporanRepository.generate_laporan_terlambat(request.get('start_date'), request.get('end_date'),
                                                            request.get('search'), request.get('page'),
                                                            request.get('size'))

    @staticmethod
    def laporan_kuota_cuti(request):
        return LaporanRepository.generate_laporan_kuota_cuti(request.get('page'),
                                                             request.get('size'), request.get('search'),
                                                             request.get('periode'), )
