import faker 
import random
from functions import create_ISBN
fake = faker.Faker()
random.seed(0)


ISBNS=create_ISBN(200)


def generate_book_title():
    words = ['The', 'A', 'An', 'In', 'Of', 'To', 'And', 'On', 'With', 'For', 'From', 'By', 'At', 'Into', 'Out', 'About']
    adjectives = ['Amazing', 'Brilliant', 'Fantastic', 'Incredible', 'Magnificent', 'Wonderful', 'Fascinating', 'Captivating']
    nouns = ['Adventure', 'Mystery', 'Thriller', 'Fantasy', 'Romance', 'Science Fiction', 'Biography', 'History', 'Horror']

    title = random.choice(words) + ' ' + random.choice(adjectives) + ' ' + random.choice(nouns)
    return title

titles = []

# Generate 200 unique book titles
while len(titles) < 200:
    title = generate_book_title()
    if title not in titles:
        titles.append(title)


publishers = [
    "Stellar Publishing",
    "Moonstone Books",
    "Enigma Press",
    "Starlight Publications",
    "Twilight House",
    "Crystal Books",
    "Whispering Willow Publishing",
    "Arcadia Press",
    "Celestial Publishing",
    "Shadowland Publishers"
]

languages = [
    "English",
    "Spanish",
    "French",
    "German",
    "Mandarin",
    "Arabic",
    "Japanese",
    "Russian",
    "Portuguese",
    "Swahili"
]

DUMMY_DATA_NUMBER = 200;
TABLE_NAME = "Books";
TABLE_COLUMNS = ["ISBN", "title","publication_date","publisher","number_of_pages","summary","available_copies","language","keywords","Schools_id_school"]
content = "";



for i in range(DUMMY_DATA_NUMBER):
    ISBN=ISBNS[i]
    title=titles[i]
    publication_date=fake.date()
    publisher=publishers[random.randint(0,9)]
    number_of_pages=random.randint(100,1000)
    available_copies=random.randint(1,5)
    summary=fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
    language=languages[random.randint(0,9)]
    Schools_id_school=random.randint(1,3)
    keywords=f"keywords of {title}"
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{ISBN}", "{title}","{publication_date}","{publisher}","{number_of_pages}","{summary}","{available_copies}","{language}","{keywords}","{Schools_id_school}");\n'


with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)
    
    
    
    
    
    
    
    
    
    
    
    
    