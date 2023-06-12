import faker 
import random
from functions import create_ISBN
import datetime
fake = faker.Faker()


#to set up the end of the borrow 
def modulo_date(a,b,c):
    month_31=[1,3,5,7,8,10,12]
    if b in month_31:
        day=c+7
        month=b
        if day>31:
            day=day%31
            month=month+1
    elif b==2:
        day=c+7
        month=b
        if day>28:
            day=day%28
            month=month+1
    else:
        day=c+7
        month=b
        if day>30:
            day=day%30
            month=month+1
    if month>12:
        year=a+1
        month=month%12
    else:
        year=a
    return(year,month,day)



DUMMY_DATA_NUMBER = 300;
TABLE_NAME = "Borrow";
TABLE_COLUMNS = ["Books_ISBN","Users_id_user","start_date","end_date","approved"]
content = "";
ISBNS=create_ISBN(200)

for i in range(DUMMY_DATA_NUMBER):
    Book_ISBN=ISBNS[random.randint(0,199)]
    Users_id_user=random.randint(1,350)
    start_date=fake.date_between(datetime.date(2015, 9, 1), datetime.date(2023, 6, 2))
    a=str(start_date).split("-")
    year,month,day=modulo_date(int(a[0]), int(a[1]), int(a[2]))
    if i<DUMMY_DATA_NUMBER-10:
        end_date=fake.date_between(datetime.date(int(a[0]), int(a[1]), int(a[2])), datetime.date(year,month,day))
    else:
        y,m,d=modulo_date(year,month,day)
        end_date=fake.date_between(datetime.date(year,month,day),datetime.date(y,m,d))
    approved=1
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Book_ISBN}","{Users_id_user}","{start_date}","{end_date}","{approved}");\n'


with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)
    
    
    
    
    
    
    
    
    
    
    
    
    