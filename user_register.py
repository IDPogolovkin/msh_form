from app import app, bcrypt, db
from app.models import User

app.app_context().push()

hashed_password = bcrypt.generate_password_hash('Test123').decode('utf-8') 
user = User( 
    username="test",
    kato_1="test",
    kato_1_name="test",
    kato_2="test",
    kato_2_name="test",
    kato_3="test",
    kato_3_name="test",
    first_name="test", 
    last_name="test", 
    middle_name="test", 
    district = "test", 
    password=hashed_password 
) 
db.session.add(user)
db.session.commit()