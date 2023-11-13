from app import app, bcrypt, db
from app.models import User

app.app_context().push()

hashed_password = bcrypt.generate_password_hash('Test123').decode('utf-8') 
user = User(
    kato_2="test",
    kato_2_name="test",
    kato_4="test",
    kato_4_name="test",
    kato_6="test",
    kato_6_name="test",
    password=hashed_password 
) 
db.session.add(user)
db.session.commit()