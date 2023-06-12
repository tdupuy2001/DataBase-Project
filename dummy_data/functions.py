import random
import string
random.seed(0)

def create_password(n):
    letters=string.ascii_letters
    nb=string.digits
    str=letters+nb
    return ''.join(random.choice(str) for i in range(n))
    
def create_ISBN(a):
    ISBN=[]
    for i in range(a):
        g=random.randint(1000000000000,9999999999999)
        while g in ISBN:
            g=random.randint(1000000000000,9999999999999)
        ISBN.append(g)
    return ISBN

