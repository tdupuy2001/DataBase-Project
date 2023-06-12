import faker 
from functions import create_password
import random

fake = faker.Faker()

#students creation
DUMMY_DATA_NUMBER = 300;
TABLE_NAME = "Users";
TABLE_COLUMNS = ["first_name", "last_name","birth_date","email","username","password","Roles_role","Schools_id_school","approved"]
content = "";

for _ in range(DUMMY_DATA_NUMBER):
    firstName = fake.first_name()
    lastName = fake.last_name()
    birth_date=fake.date_of_birth(minimum_age=20,maximum_age=30)
    email = fake.ascii_safe_email()
    username=firstName[0]+lastName
    password=create_password(random.randint(8,16))
    Schools_id_school=random.randint(1,3)
    approved=1
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{firstName}", "{lastName}","{birth_date}","{email}", "{username}","{password}","student","{Schools_id_school}","{approved}");\n'


with open("dummy_data_Students.txt", 'w') as f:
    f.write(content)