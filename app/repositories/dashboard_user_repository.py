from app import AppConstants
from app.database import db

from sqlalchemy import union_all, literal_column

from app.entity import ApprovalKoreksi, ApprovalIzin, ApprovalLembur, ApprovalAbsensiBorongan, ApprovalReimburse, Users


class DashboardUserRepository:

    @staticmethod
    def get_all_approval_status_waiting(user_id):

        q_koreksi = db.session.query(
            ApprovalKoreksi.id.label('approval_id'),
            ApprovalKoreksi.created_date.label('tanggal_pengajuan'),
            literal_column("'Koreksi Kehadiran'").label('tipe_approval'),
            ApprovalKoreksi.status.label('status')
        ).join(
            Users, ApprovalKoreksi.approval_user_id == Users.id
        ).filter(
            ApprovalKoreksi.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalKoreksi.user_id == user_id
        )

        q_izin = db.session.query(
            ApprovalIzin.id.label('approval_id'),
            ApprovalIzin.created_date.label('tanggal_pengajuan'),
            literal_column("'Izin'").label('tipe_approval'),
            ApprovalIzin.status.label('status')
        ).join(
            Users, ApprovalIzin.approval_user_id == Users.id
        ).filter(
            ApprovalIzin.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalIzin.user_id == user_id
        )

        q_lembur = db.session.query(
            ApprovalLembur.id.label('approval_id'),
            ApprovalLembur.created_date.label('tanggal_pengajuan'),
            literal_column("'Lembur'").label('tipe_approval'),
            ApprovalLembur.status.label('status')
        ).join(
            Users, ApprovalLembur.approval_user_id == Users.id
        ).filter(
            ApprovalLembur.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalLembur.user_id == user_id
        )

        q_borongan = db.session.query(
            ApprovalAbsensiBorongan.id.label('approval_id'),
            ApprovalAbsensiBorongan.created_date.label('tanggal_pengajuan'),
            literal_column("'Absensi Borongan'").label('tipe_approval'),
            ApprovalAbsensiBorongan.status.label('status')
        ).join(
            Users, ApprovalAbsensiBorongan.approval_user_id == Users.id
        ).filter(
            ApprovalAbsensiBorongan.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalAbsensiBorongan.user_id == user_id
        )

        q_reimburse = db.session.query(
            ApprovalReimburse.id.label('approval_id'),
            ApprovalReimburse.created_date.label('tanggal_pengajuan'),
            literal_column("'Reimburse'").label('tipe_approval'),
            ApprovalReimburse.status.label('status')
        ).join(
            Users, ApprovalReimburse.approval_user_id == Users.id
        ).filter(
            ApprovalReimburse.status == AppConstants.WAITING_FOR_APPROVAL.value,
            ApprovalReimburse.user_id == user_id
        )

        query = union_all(q_koreksi, q_izin, q_lembur, q_borongan, q_reimburse).alias("approvals")

        final_query = db.session.query(query).order_by(
            query.c.tanggal_pengajuan.asc(),
        ).limit(AppConstants.GET_LATEST_DATA.value)


        return final_query.all()