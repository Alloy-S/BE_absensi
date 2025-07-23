# Gunakan image resmi Python 3.9 sebagai dasar
FROM python:3.9-slim

# Tetapkan direktori kerja di dalam kontainer
WORKDIR /app

# Atur environment variable agar Python tidak membuat file .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LANG id_ID.UTF-8
ENV LANGUAGE id_ID:id
ENV LC_ALL id_ID.UTF-8

# Instal dependensi sistem yang mungkin diperlukan (misalnya untuk psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i -e 's/# id_ID.UTF-8 UTF-8/id_ID.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales

# Salin file requirements.txt terlebih dahulu untuk caching
COPY requirements.txt .

# Instal semua dependensi Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Salin seluruh kode aplikasi Anda ke dalam direktori kerja
COPY . .

# Buat direktori untuk menyimpan file upload
RUN mkdir -p /app/uploads/photos

# Ekspos port yang akan digunakan oleh Gunicorn
EXPOSE 5000

# Perintah untuk menjalankan aplikasi saat kontainer dimulai
# Menggunakan Gunicorn sebagai server WSGI yang siap untuk produksi
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]