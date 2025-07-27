## Command to Run 

python -m venv be_absensi

source ./be_absensi/Scripts/activate

pip install -r requirements.txt
~~
## Command DB Migration

flask db init

flask db migrate -m "Initial migration"

flask db upgrade

## docker
docker-compose up --build

docker-compose up

docker-compose down

### untuk init db
docker-compose exec web flask db upgrade

### server
docker compose exec web flask db upgrade


### migration db

## API Endpoint List

### **1. Authentication & User Management**
- **`POST /api/auth/login`** *(User/PIC/Admin)*  
  *Login user (staf/PIC/admin)*
- **`POST /api/auth/logout`** *(User/PIC/Admin)*  
  *Logout user*
- **`GET /api/user/profile`** *(User/PIC/Admin)*  
  *Melihat profil user*
- **`PUT /api/user/profile`** *(User/PIC/Admin)*  
  *Mengedit profil user*

### **2. Presensi & Absensi**
- **`POST /api/presensi/staff`** *(User - Staf)*  
  *Melakukan presensi staf (Face Recognition)*
- **`POST /api/absensi`** *(PIC)*  
  *Input absensi karyawan borongan dan harian oleh PIC*
- **`PUT /api/absensi/koreksi/{absensi_id}`** *(PIC/Admin)*  
  *Koreksi absensi karyawan*
- **`GET /api/absensi/riwayat`** *(User/PIC/Admin)*  
  *Melihat riwayat absensi*
- **`POST /api/absensi/izin`** *(User/PIC/Admin)*  
  *Input izin karyawan*
- **`POST /api/absensi/lembur`** *(User/PIC/Admin)*  
  *Input lembur karyawan*
- **`PUT /api/absensi/approval/{absensi_id}`** *(Admin)*  
  *Melakukan approval absensi*

### **3. Pengumuman & Informasi**
- **`GET /api/perusahaan/profil`** *(User/PIC/Admin)*  
  *Melihat profil perusahaan*
- **`GET /api/pengumuman`** *(User/PIC/Admin)*  
  *Melihat daftar pengumuman*
- **`POST /api/pengumuman`** *(Admin)*  
  *Tambah pengumuman*
- **`PUT /api/pengumuman/{id}`** *(Admin)*  
  *Edit pengumuman*
- **`DELETE /api/pengumuman/{id}`** *(Admin)*  
  *Hapus pengumuman*

### **4. Manajemen Pegawai**
- **`GET /api/pegawai`** *(Admin)*  
  *Melihat daftar pegawai*
- **`POST /api/pegawai`** *(Admin)*  
  *Menambahkan pegawai baru*
- **`PUT /api/pegawai/{id}`** *(Admin)*  
  *Mengedit data pegawai*
- **`DELETE /api/pegawai/{id}`** *(Admin)*  
  *Menghapus pegawai*

### **5. Pengaturan & Konfigurasi**
- **`GET /api/pengaturan/lokasi`** *(Admin)*  
  *Melihat lokasi presensi*
- **`POST /api/pengaturan/lokasi`** *(Admin)*  
  *Menambah lokasi presensi*
- **`PUT /api/pengaturan/lokasi/{id}`** *(Admin)*  
  *Edit lokasi presensi*
- **`DELETE /api/pengaturan/lokasi/{id}`** *(Admin)*  
  *Hapus lokasi presensi*
- **`GET /api/pengaturan/harga`** *(Admin)*  
  *Melihat harga borongan dan harian*
- **`POST /api/pengaturan/harga`** *(Admin)*  
  *Input harga baru borongan dan harian*
- **`PUT /api/pengaturan/harga/{harga_id}`** *(Admin)*  
  *Mengubah harga borongan dan harian*

### **6. Laporan & Reimburse**
- **`GET /api/laporan/presensi`** *(Admin)*  
  *Generate laporan presensi*
- **`GET /api/laporan/gaji`** *(Admin)*  
  *Generate laporan gaji*
- **`GET /api/laporan/presensi/export`** *(Admin)*  
  *Export laporan presensi*
- **`GET /api/laporan/gaji/export`** *(Admin)*  
  *Export laporan gaji*
- **`POST /api/reimburse`** *(User/PIC/Admin)*  
  *Mengajukan reimburse*
- **`GET /api/reimburse`** *(User/PIC/Admin)*  
  *Melihat daftar reimburse*
- **`PUT /api/reimburse/{id}`** *(Admin)*  
  *Update status reimburse*
- **`PUT /api/reimburse/approval/{id}`** *(Admin)*  
  *Approval reimburse*





