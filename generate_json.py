import random 
def random_json():

    Book_id = random.randint(1,733)
    Customer_grade = random.randint(1,5)

    Customer_names_1 = ["Pelle","Sara","Sexbomb","Häxan","Trollet","Tomte"]
    Customer_names_2 = ["Kat69","98_","Oskulden","Satmara","Pojke","Nisse"]
    Customer_names_3 = ["oro_","läskunnig","plugghäst","74","stalker_","96"]
    Customer_txt = ["Bra att somna till","Boring","Best I ever did not read","Read it and liked it" ]

    cs1 = random.randint(0,5)
    cs2 = random.randint(0,5)
    cs3 = random.randint(0,5)
    cn = random.randint(0,1)
    ct = random.randint(0,3)

    Customer_nameX = Customer_names_1[cs1]+Customer_names_2[cs2]
    Customer_nameY = Customer_names_3[cs3]+Customer_names_2[cs1]

    Customer_name = []
    Customer_name.append(Customer_nameX)
    Customer_name.append(Customer_nameY)

    review = '{\n'+f'\n\t"book_id":{Book_id},\n\t"rating":{Customer_grade},\n\t"review_name":"{Customer_name[cn]}",\n\t"review_text":"{Customer_txt[ct]}"\n'+'}\n'
    review_text = f'{Book_id},{Customer_grade},{Customer_name[cn]},{Customer_txt[ct]}\n'
    return review, review_text

def generate_json():

    with open("random_rew.txt","w", encoding="utf8") as sav:

        for i in range(100):
            review, review_text = random_json()     
            sav.write(str(review))

    with open("random_rev_text.txt","w", encoding="utf8") as sav:

        for i in range(3000):
            review, review_text = random_json()     
            sav.write(str(review_text))


from sqlite__db_OOP import *

def db_search(book_id):
    query_Book_id = "SELECT * FROM Books WHERE Books.Book_id = ?"
    db = get_db_conn()
    post = db.GET_query(query_Book_id, (book_id,) )
    db.db_close()
    return post

def db_post_reviews():
    db = get_db_conn()

    with open('random_rev_text.txt','r') as f:
        for i in f:
            i = i.replace('\n','')
            i = i.split(',')
            print(i)
            query_add = "INSERT INTO review (book_id, review_name, rating, review_text) VALUES \
            (?, ?, ?, ?)"
            db.execute_query(query_add, (i[0], i[2], i[1], i[3]))
    db.db_close()
    
generate_json()
db_post_reviews()

