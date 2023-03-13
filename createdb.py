from project import db, create_app, models

app = create_app()
with app.app_context():
    db.create_all()
    

# app = create_app()
# db.create_all(app) # pass the create_app result so Flask-SQLAlchemy gets the configuration.