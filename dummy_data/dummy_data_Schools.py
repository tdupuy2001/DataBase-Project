import faker 
import random
fake = faker.Faker(["en_GB"])


DUMMY_DATA_NUMBER = 3;
TABLE_NAME = "Schools";
TABLE_COLUMNS = ["name", "address","city","phone_number","email","director_name","Administrator_id_admin","Operators_id_operators"]
content = "";
school=["Civil Engineering","Chemical Engineering","Electrical and Computer Engineering"]

for i in range(DUMMY_DATA_NUMBER):
    name = school[i]
    email = fake.ascii_safe_email()
    address=str(random.randint(1,99))+' '+fake.street_name()
    city=fake.city()
    phone_number=fake.phone_number()
    director_name = fake.name()
    Administrator_id_admin=1
    Operators_id_operators=i+1
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{name}","{address}","{city}","{phone_number}","{email}","{director_name}","{Administrator_id_admin}","{Operators_id_operators}");\n'


with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)