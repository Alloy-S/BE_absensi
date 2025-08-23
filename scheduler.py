import os
from redis import Redis
from rq_scheduler import Scheduler

from app.tasks.kuota_jatah_cuti_task import generate_kuota_cuti_tahunan_otomatis
from app.tasks.remainder_task import check_for_clock_in_reminders, check_for_clock_out_reminders

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_conn = Redis.from_url(redis_url)

scheduler = Scheduler(connection=redis_conn)

for job in scheduler.get_jobs():
    print(f"Membatalkan jadwal lama: {job.id}")
    scheduler.cancel(job)

scheduler.cron(
    cron_string="*/15 * * * *",
    func=check_for_clock_in_reminders,
    id="job_cek_absen_masuk",
    repeat=None,
    queue_name="default"
)

scheduler.cron(
    cron_string="*/15 * * * *",
    func=check_for_clock_out_reminders,
    id="job_cek_absen_pulang",
    repeat=None,
    queue_name="default"
)

# setiap 1 januari
scheduler.cron(
    cron_string="0 1 1 1 *",
    func=generate_kuota_cuti_tahunan_otomatis(),
    id="job_generate_kuota_cuti",
    repeat=None,
    queue_name="default"
)

print("scheduler berhasil di inisialisasi")
