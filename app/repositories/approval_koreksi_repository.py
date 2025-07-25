from app.database import db
from app.entity import ApprovalKoreksi
from datetime import date
from sqlalchemy.orm import joinedload
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract
from datetime import date, datetime

from app.utils.app_constans import AppConstants


class ApprovalKoreksiRepository:

    @staticmethod
    def get_list_pagination(user_id, page=1, size=10, search=None, filter_status=None):
        query = ApprovalKoreksi.query.filter(
            ApprovalKoreksi.user_id == user_id
        )

        if search:
            try:
                search_date = datetime.strptime(search, '%Y-%m')

                query = query.filter(
                    extract('year', ApprovalKoreksi.absensi_date) == search_date.year,
                    extract('month', ApprovalKoreksi.absensi_date) == search_date.month
                )
            except ValueError:
                pass

        if filter_status and filter_status != AppConstants.APPROVAL_STATUS_ALL.value:
            query = query.filter(
                ApprovalKoreksi.status == filter_status
            )

        query = query.order_by(ApprovalKoreksi.created_date.desc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_detail_by_id(user_id, approval_id):
        query = ApprovalKoreksi.query.options(
            joinedload(ApprovalKoreksi.detail_approval),
            joinedload(ApprovalKoreksi.approval_user)
        ).filter_by(id=approval_id,
                                                                                             user_id=user_id)
        return query.first()

    @staticmethod
    def create_approval_koreksi_user(data):
        new_koreksi = ApprovalKoreksi(
            absensi_date=data['absensi_date'],
            status=data['status'],
            approval_user_id=data['approval_user_id'],
            absensi_id=data['absensi_id'],
            user_id=data['user_id'],
            catatan_pengajuan=data['catatan_pengajuan']
        )

        db.session.add(new_koreksi)
        db.session.flush()

        return new_koreksi

    @staticmethod
    def delete_koreksi(approval):
        parent_absensi = approval.absensi

        for detail_approval in approval.detail_approval:
            db.session.delete(detail_approval)

        db.session.delete(approval)

        if parent_absensi and parent_absensi.metode == AppConstants.KOREKSI_KEHADIRAN.value:
            db.session.delete(parent_absensi)

    @staticmethod
    def find_by_user_and_date(user_id, absensi_date):
        return ApprovalKoreksi.query.filter_by(
            user_id=user_id,
            absensi_date=absensi_date
        ).first()