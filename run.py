from app import app
from database import db

# Create tables before starting the app
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
