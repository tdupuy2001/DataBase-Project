import faker 
import random
from functions import create_ISBN
import datetime
fake = faker.Faker()




DUMMY_DATA_NUMBER = 150;
TABLE_NAME = "Review";
TABLE_COLUMNS = ["Books_ISBN","Users_id_user","date","grade","comment","approved"]
content = "";
ISBNS=create_ISBN(200)

for i in range(DUMMY_DATA_NUMBER):
    Book_ISBN=ISBNS[random.randint(0,199)]
    Users_id_user=random.randint(1,350)
    date=fake.date_between(datetime.date(2015, 9, 1), datetime.date(2023, 6, 2))
    grade=random.randint(0,10)
    comment=fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
    approved=1
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Book_ISBN}","{Users_id_user}","{date}","{grade}","{comment}","{approved}");\n'


with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)
    
    
    
    
    
    
    
    
    
    
    
    
    