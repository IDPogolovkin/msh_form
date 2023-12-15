from app import app, bcrypt, db
from app.models import *
import csv


app.app_context().push()

csv_file_path = 'MSH_USER.csv' #change
counter = 0
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    next(csv_reader)
    for row in csv_reader:
        hashed_password = bcrypt.generate_password_hash(row[6]).decode('utf-8') 

        user = User( # change
            login = row[4],
            kato_2=row[0],
            kato_2_name=row[1],
            kato_4=row[2],
            kato_4_name=row[3],
            kato_6 = row[4],
            kato_6_name = row[5],
            is_district = False, #change
            is_obl = False,
            password=hashed_password
        )
                
        db.session.add(user)
        db.session.commit()
        counter += 1
        print(counter, '-', user)


# hashed_password = bcrypt.generate_password_hash('Test123').decode('utf-8') 

# user = User(
#     login = 'test2',
#     kato_2='35',
#     kato_2_name='КАРАГАНДИНСКАЯ ОБЛАСТЬ',
#     kato_4='3540',
#     kato_4_name='БУХАР-ЖЫРАУСКИЙ',
#     is_district = True,
#     is_obl = False,
#     password=hashed_password
# )

# db.session.add(user)
# db.session.commit()




# for user in User_district.query.all():
#     db.session.delete(user)
#     db.session.commit()