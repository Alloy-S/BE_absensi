from dotenv import load_dotenv
import os
import requests


class NotificationService:
    @staticmethod
    def send_notification(phone, username, password, fullname, nip):
        print("Send notification.")

        load_dotenv()

        apiKey = os.getenv("WABLAS_API_KEY")

        url = os.getenv("WABLAS_API") + "/api/send-message"

        template = (
            f"*Pendaftaran Akun*\n\n"
            f"Kepada, {fullname}\n\n"
            f"Selamat, Anda telah terdaftar di PT. Benz Cahaya Purnama pada Sistem Absensi. Melalui Benz Absensi, Anda dapat melakukan berbagai hal seperti mengelola absensi, melihat data personal, melihat informasi kepegawaian, mengelola cuti, serta melakukan permohonan reimburse.\n"
            f"Berikut adalah detail akun Anda:\n\n"
            f"*Nama Pengguna*: {fullname}\n"
            f"*Nomor Karyawan*: {nip}\n"
            f"*Username*: {username}\n"
            f"*Password*: {password}\n\n"
            "Silakan login dan segera ganti password Anda.\n"
            "Silakan login di http://example.com \n\n"
            "Terima kasih"
        )

        payload = {
            "phone": phone,
            "message": template
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": apiKey
        }

        response = requests.post(url, headers=headers, json=payload)

        return response.json()
