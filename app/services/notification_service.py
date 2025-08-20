from dotenv import load_dotenv
import os
import requests
from firebase_admin import messaging
from app.repositories.user_repository import UserRepository



class NotificationService:
    @staticmethod
    def send_notification_login_data(phone, username, password, fullname, nip):
        print("Send notification.")

        load_dotenv()

        api_key = os.getenv("WABLAS_API_KEY")

        url = os.getenv("WABLAS_API") + "/api/send-message"

        template = (
            f"*Pendaftaran Akun*\n\n"
            f"Kepada, {fullname}\n\n"
            f"Selamat, Anda telah terdaftar di PT. Benz Cahaya Suprana pada Sistem Absensi. Melalui Benz Absensi, Anda dapat melakukan berbagai hal seperti mengelola absensi, melihat data personal, melihat informasi kepegawaian, mengelola cuti, serta melakukan permohonan reimburse.\n"
            f"Berikut adalah detail akun Anda:\n\n"
            f"*Nama Pengguna*: {fullname}\n"
            f"*Nomor Karyawan*: {nip}\n"
            f"*Username*: {username}\n"
            f"*Password*: {password}\n\n"
            "Silakan login dan segera ganti password Anda.\n"
            "Silakan login di https://mybenz.site/login \n\n"
            "Terima kasih"
        )

        payload = {
            "phone": phone,
            "message": template
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": api_key
        }

        response = requests.post(url, headers=headers, json=payload)

        print(response)

        user = UserRepository.get_user_by_username(username)

        UserRepository.mark_done_notif_login(user)

    @staticmethod
    def send_single_notification(fcm_token: str, judul: str, isi_pesan: str):
        if not fcm_token:
            print("Tidak ada FCM token, notifikasi tidak dikirim.")
            return False

        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=judul,
                    body=isi_pesan,
                ),
                token=fcm_token,
            )


            response = messaging.send(message)
            print('Notifikasi berhasil dikirim:', response)
            return True
        except Exception as e:
            print(f"Gagal mengirim notifikasi ke token {fcm_token}: {e}")
            return False

    @staticmethod
    def send_notification_logout(old_token):
        try:
            message = messaging.Message(
                data={
                    "action": "FORCE_LOGOUT",
                    "message": "Sesi Anda telah dihentikan karena login di perangkat lain."
                },
                token=old_token,
            )
            messaging.send(message)
            print(f"Sinyal logout terkirim ke token: {old_token}")
        except Exception as e:
            print(f"Gagal mengirim sinyal logout: {e}")
