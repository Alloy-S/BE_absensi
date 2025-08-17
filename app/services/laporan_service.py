from app.repositories.laporan_repository import LaporanRepository
from datetime import date, timedelta
import pandas as pd
import io
import base64
from app.utils.app_constans import AppConstants


class LaporanService:

    @staticmethod
    def rekap_periode(request):
        return LaporanRepository.generate_laporan_periode_pagination(request.get('start_date'), request.get('end_date'),
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
                                                             request.get('periode'))

    @staticmethod
    def laporan_upah_absensi_borongan(request):
        result = LaporanRepository.generate_laporan_upah_borongan_pagination(request.get('start_date'),
                                                                             request.get('end_date'),
                                                                             request.get('search'), request.get('page'),
                                                                             request.get('size'))

        date_headers = []
        current_date = date.fromisoformat(request.get('start_date'))
        end_date = date.fromisoformat(request.get('end_date'))

        items = result.get('items')
        total = result.get('total')
        size = request.get('size')

        while current_date <= end_date:
            date_headers.append({
                "day": AppConstants.DAY_MAP.value.get(current_date.weekday()),
                "date": current_date.isoformat(),
            })
            current_date += timedelta(days=1)

        pivoted_data = {}
        for row in items:
            if row['nip'] not in pivoted_data:
                pivoted_data[row['nip']] = {
                    "nip": row['nip'],
                    "nama": row['nama'],
                    "upah": [],
                    "total_upah": 0
                }

            date_key = row['calendar_date'].isoformat()
            pivoted_data[row['nip']]['upah'].append({
                "date": date_key,
                "upah": row['upah']
            })
            pivoted_data[row['nip']]['total_upah'] += row['upah']

        return {
            "items": list(pivoted_data.values()),
            "headers": date_headers,
            "total": total,
            "pages": (total + size - 1) // size if total > 0 else 0
        }

    @staticmethod
    def generate_excel_laporan_upah_borongan(request):
        start_date = request.get('start_date')
        end_date = request.get('end_date')
        result = LaporanRepository.generate_laporan_upah_borongan(start_date, end_date,
                                                                  request.get('search'))

        df = pd.DataFrame(result)
        pivot_df = df.pivot_table(index=['nip', 'nama'], columns='calendar_date', values='upah').fillna(0)

        pivot_df['Total'] = pivot_df.sum(axis=1)

        pivot_df.reset_index(inplace=True)
        pivot_df.rename(columns={'nip': 'NIP', 'nama': 'Nama'}, inplace=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            pivot_df.to_excel(writer, index=False, sheet_name='Laporan Upah Borongan')

        output.seek(0)

        excel_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

        file_name = f'Laporan_Upah_Borongan_{start_date}_-_{end_date}.xlsx'

        return {
            'filename': file_name,
            'file': excel_base64
        }

    @staticmethod
    def format_minutes_to_hours(total_minutes):
        if not total_minutes or total_minutes == 0: return "0 menit"
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        return f"{hours} jam {minutes} menit"

    @staticmethod
    def export_rekap_full(request):

        start_date = request.get('start_date')
        end_date = request.get('end_date')

        result = LaporanRepository.generate_rekap_full(start_date, end_date)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:

            df_rekap = pd.DataFrame(result['rekap'])
            if not df_rekap.empty:
                df_rekap['total_menit_kehadiran'] = df_rekap['total_menit_kehadiran'].apply(
                    LaporanService.format_minutes_to_hours)
                df_rekap['total_menit_terlambat'] = df_rekap['total_menit_terlambat'].apply(
                    LaporanService.format_minutes_to_hours)
                df_rekap['total_menit_pulang_awal'] = df_rekap['total_menit_pulang_awal'].apply(
                    LaporanService.format_minutes_to_hours)
                df_rekap.rename(columns={'nama': 'Nama Karyawan',
                                         'tipe_karyawn': 'Tipe Karyawan',
                                         'total_kehadiran': 'Total Hadir',
                                         'total_absen_tidak_lengkap': 'Total Absen Tidak Lengkap',
                                         'total_izin': 'Total Izin',
                                         'total_pulang_awal': 'Total Pulang Awal',
                                         'total_terlambat': 'Total Terlambat',
                                         'total_tidak_hadir': 'Total Tidak Hadir',
                                         'total_menit_kehadiran': 'Total Menit Kehadiran',
                                         'total_menit_terlambat': 'Total Menit Terlambat',
                                         'total_menit_pulang_awal': 'Total Menit Pulang Awal',
                                         }, inplace=True)
            df_rekap.to_excel(writer, index=False, sheet_name='Rekap Periode')

            df_terlambat = pd.DataFrame(result['terlambat'])
            if not df_terlambat.empty:
                df_terlambat['menit_terlambat'] = df_terlambat['menit_terlambat'].apply(
                    LaporanService.format_minutes_to_hours)
                df_terlambat.rename(columns={'nama': 'Nama Karyawan',
                                             'jadwal_kerja': 'Jadwal Kerja',
                                             'date_absensi': 'Tanggal Absen',
                                             'waktu_absen': 'Waktu Absen',
                                             'jadwal_time_in': 'Jadwal Masuk',
                                             'menit_terlambat': 'Menit Terlambat',
                                             },
                                    inplace=True)
            df_terlambat.to_excel(writer, index=False, sheet_name='Detail Terlambat')

            df_izin = pd.DataFrame(result['izin'])
            if not df_izin.empty:
                df_izin.rename(columns={'nama': 'Nama Karyawan',
                                        'sisa_cuti_tahunan': 'Sisa Cuti Tahunan',
                                        'total_cuti_tahunan': 'Total Cuti Tahunan',
                                        'cuti_tahunan_terpakai': 'Cuti Tahunan Terpakai'
                                        }, inplace=True)
            df_izin.to_excel(writer, index=False, sheet_name='Detail Izin')

        output.seek(0)

        excel_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

        file_name = f'Laporan_Rekap_Periode_{start_date}_-_ {end_date}.xlsx'

        return {
            'filename': file_name,
            'file': excel_base64
        }
