import pymysql
pymysql.install_as_MySQLdb()

db = pymysql.connect(
    host="127.0.0.1",
    user="admin",
    passwd="12345",
    db="first_db",
    charset="utf8"
)

cursor = db.cursor()

cursor.execute("""INSERT INTO Books(name, discription)VALUES(%s, %s),(%s, %s)""",
               ( "Преступление и наказание", "Классика",
                "Три товарища", "Зарубежная литература")
               )

db.commit()

#cursor.execute("DELETE FROM Books WHERE id>1")
#db.commit()

cursor.execute("SELECT * FROM Books;")

books = cursor.fetchall()

for book in books:
    print(book)

cursor.close()
db.close()
