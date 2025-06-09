from app import create_app

# Buat aplikasi menggunakan factory
app = create_app()

if __name__ == '__main__':
    # Jalankan aplikasi
    app.run(debug=True)