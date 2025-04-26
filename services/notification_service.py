from dotenv import load_dotenv
import os
import requests


class NotificationService:
    @staticmethod
    def send_notification(phone, username, password):
        print("Send notification.")

        load_dotenv()

        apiKey = os.getenv("WABLAS_API_KEY")

        url = "https://tegal.wablas.com/api/send-message"

        template = (
            f"📢 *Akun Anda telah terdaftar!*\n\n"
            f"Username: *{username}*\n"
            f"Password: *{password}*\n\n"
            "Silakan login dan segera ganti password Anda.\n"
            "Silakan login di http://example.com \n\n"
            "Terima kasih 🙏"
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
