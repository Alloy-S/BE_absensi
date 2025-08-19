import os
import json
import shutil
import uuid
from datetime import datetime, date, time
from decimal import Decimal
from app.database import db
from app.entity import Absensi, AbsensiBorongan, Izin, Lembur, Reimburse, RiwayatPenggajian
from app import create_app
from app.execption.custom_execption import GeneralExceptionWithParam
from app.repositories.backup_log_repository import BackupLogRepository
from app.utils.error_code import ErrorCode


def serialize_model(obj):
    if obj is None:
        return None
    data = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)

        if isinstance(value, (datetime, date, time)):
            data[column.name] = value.isoformat()
        elif isinstance(value, uuid.UUID):
            data[column.name] = str(value)
        elif isinstance(value, Decimal):
            data[column.name] = str(value)
        else:
            data[column.name] = value
    return data


def run_periodic_backup_and_erase(log_id):

    app = create_app()
    with app.app_context():
        log = BackupLogRepository.get_backup_log_by_id(log_id)

        if not log:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': 'backup log'})

        log.status = 'IN PROGRESS'
        db.session.commit()

        start_date = log.start_date
        end_date = log.end_date

        temp_backup_path = None
        try:

            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            backup_dir_name = f"backup_{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}_{timestamp}"
            temp_backup_path = os.path.join('/tmp', backup_dir_name)
            os.makedirs(temp_backup_path, exist_ok=True)

            full_backup_data = {}
            all_photos_to_backup = set()

            parent_tables_to_process = {
                'absensi': (Absensi, Absensi.date),
                'absensi_borongan': (AbsensiBorongan, AbsensiBorongan.date),
                'izin': (Izin, Izin.tgl_izin_start),
                'lembur': (Lembur, Lembur.date_start),
                'reimburse': (Reimburse, Reimburse.date),
                'riwayat_penggajian': (RiwayatPenggajian, RiwayatPenggajian.periode_end)
            }

            for name, (model, date_column) in parent_tables_to_process.items():
                print(f"Memproses tabel: {name}...")
                records = model.query.filter(date_column.between(start_date, end_date)).all()

                serialized_records = []
                for record in records:
                    serialized_record = serialize_model(record)

                    if name == 'absensi':
                        serialized_record['detail_absensi'] = [serialize_model(d) for d in record.detail_absensi]
                        serialized_record['approval'] = [serialize_model(a) for a in record.approval]

                    if name == 'absensi_borongan':
                        serialized_record['detail_absensi_borongan'] = [serialize_model(d) for d in record.detail_absensi_borongan]
                        serialized_record['approval_absensi_borongan'] = serialize_model(record.approval_absensi_borongan)

                    if name == 'izin':
                        serialized_record['approval_izin'] = serialize_model(record.approval_izin)

                    if name == 'lembur':
                        serialized_record['approval_lembur'] = [serialize_model(d) for d in record.approval_lembur]

                    if name == 'reimburse':
                        serialized_record['detail_reimburse'] = [serialize_model(d) for d in record.detail_reimburse]
                        serialized_record['approval_reimburse'] = [serialize_model(d) for d in record.approval_reimburse]
                        serialized_record['photo'] = serialize_model(record.photo)

                        if record.photo:
                            all_photos_to_backup.add(record.photo.filename)

                    if name == 'riwayat_penggajian':
                        details_data = []
                        if hasattr(record, 'riwayat_penggajian_detail'):
                            for detail in record.riwayat_penggajian_detail:
                                serialized_detail = serialize_model(detail)
                                if hasattr(detail, 'riwayat_penggajian_rincian'):
                                    serialized_detail['riwayat_penggajian_rincian'] = [serialize_model(r) for r in
                                                                                       detail.riwayat_penggajian_rincian]
                                details_data.append(serialized_detail)
                        serialized_record['riwayat_penggajian_detail'] = details_data

                    serialized_records.append(serialized_record)

                full_backup_data[name] = serialized_records
                print(f"Berhasil memproses {len(records)} record dari {name}.")

            with open(os.path.join(temp_backup_path, 'backup_data.json'), 'w') as f:
                json.dump(full_backup_data, f, indent=4)
            print("Berhasil menyimpan data ke backup_data.json.")

            uploads_folder = 'uploads'
            photos_backup_path = os.path.join(temp_backup_path, 'photos')
            os.makedirs(photos_backup_path, exist_ok=True)

            for filename in all_photos_to_backup:
                source_path = os.path.join(uploads_folder, 'photos', filename)
                if os.path.exists(source_path):
                    shutil.copy(source_path, photos_backup_path)
            print(f"Berhasil menyalin {len(all_photos_to_backup)} file foto.")

            # Buat arsip ZIP final

            final_archive_folder = os.path.join(uploads_folder, 'backups')
            os.makedirs(final_archive_folder, exist_ok=True)
            final_archive_base_name = os.path.join(final_archive_folder, backup_dir_name)
            final_zip_path = shutil.make_archive(final_archive_base_name, 'zip', temp_backup_path)

            print(f"Backup final berhasil dibuat di: {os.path.basename(final_zip_path)}")

            print("Memulai proses hapus data...")
            for name, (model, date_column) in parent_tables_to_process.items():
                num_deleted = model.query.filter(date_column.between(start_date, end_date)).delete(
                    synchronize_session=False)
                print(f"Berhasil menghapus {num_deleted} record dari {name} (cascade).")

            for filename in all_photos_to_backup:
                file_path = os.path.join(uploads_folder, 'photos', filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            print("File foto terkait berhasil dihapus.")

            log.status = 'READY TO DOWNLOAD'
            log.filename = os.path.basename(final_zip_path)
            log.file_path = final_zip_path
            db.session.commit()

        except Exception as e:
            db.session.rollback()

            log.status = 'FAILED'
            log.error_message = str(e)
            db.session.commit()
            print(f"Terjadi error saat menjalankan tugas periodik: {e}")
        finally:
            if temp_backup_path and os.path.exists(temp_backup_path):
                shutil.rmtree(temp_backup_path)
                print("Direktori sementara berhasil dibersihkan.")
