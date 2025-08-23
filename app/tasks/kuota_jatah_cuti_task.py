from app.services.jatah_cuti_service import JatahCutiService
from app import create_app
from datetime import date


def generate_kuota_cuti_tahunan_otomatis():
    app = create_app()
    with app.app_context():
        target_year = date.today().year
        print(f"Memulai tugas terjadwal: generate_kuota_cuti_tahunan untuk tahun {target_year}")

        try:
            result = JatahCutiService.generate_kuota_tahunan(target_year)
            print(f"job selesai: {result.get('message')}")
            return result
        except Exception as e:
            print(f"Error saat menjalankan tugas generate_kuota_tahunan: {e}")
            raise e