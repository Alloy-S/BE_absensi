from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.repositories.backup_log_repository import BackupLogRepository
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.database import db

import os
from datetime import datetime
from flask import current_app
from redis import Redis
from rq import Queue

try:
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    conn = Redis.from_url(redis_url)
    q = Queue(connection=conn)
except Exception as e:
    current_app.logger.error(f"Tidak bisa terhubung ke Redis: {e}")
    q = None
class BackupService:

    @staticmethod
    def get_all_log(params):
        return BackupLogRepository.get_all_backup_log_paginated(params.get('page'), params.get('size'))

    @staticmethod
    def get_log_by_id(log_id):
        return BackupLogRepository.get_backup_log_by_id(log_id)

    @staticmethod
    def start_backup_and_erase(data):

        if not q:
            raise GeneralException(ErrorCode.CONN_FAILED_REDIS)

        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()

        new_log = BackupLogRepository.create_backup_log({
            'start_date': start_date,
            'end_date': end_date,
            'status': 'PENDING'
        })

        job = q.enqueue(
            'app.tasks.backup_tasks.run_periodic_backup_and_erase',
            new_log.id
        )

        db.session.commit()

        return new_log, job

    @staticmethod
    def delete_file_and_update_status(log_id):
        log = BackupService.get_log_by_id(log_id)
        if not log:
            GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': 'backup log'})

        if log.file_path and os.path.exists(log.file_path):
            os.remove(log.file_path)

        log.status = 'COMPLETED'
        db.session.commit()

