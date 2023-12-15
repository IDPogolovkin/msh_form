from app import app, bcrypt, db
from app.models import *
import csv


app.app_context().push()

csv_file_path = 'MSH_USER_OBL.csv' #change
counter = 0
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    next(csv_reader)
    for row in csv_reader:
        hashed_password = bcrypt.generate_password_hash(row[2]).decode('utf-8') 

        user = User( # change
            login = row[0],
            kato_2=row[0],
            kato_2_name=row[1],
            is_district = False, #change
            is_obl = True,
            password=hashed_password
        )
                
        db.session.add(user)
        db.session.commit()
        counter += 1
        print(counter, '-', user)