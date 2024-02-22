from app import app, db
from app.models import Employee, Experience

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all database tables are created based on models
    app.run(debug=True)  # Turn off debug mode for production
