import mysql.connector
from mysql.connector import Error
import random
import numpy as np

def opn(host_name, user_name, user_password, db_name):
    """Here is an example use: cnx = soyeon.opn("127.0.0.1", "root", "J@Y@Hr0m", "<@@@DATABASE@@@>").

    Follow this with:
    cursor = cnx.cursor()

    Sandwich your sql queries with a mandatory:
    cnx.commit()
    cursor.close()
    cnx.close()

    Don't forget about the power of frequent commits."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def pullquiz(size,joyo,cursor):
    """Pulls randomized quiz data in the form of a list of entries.

    Kanji Data:
    Bin Counts: (20,55,147,466,1324) for (11,8),(8,6),(6,4),(4,2),(2,0.15)
    """
    listy=[]
    #Set quiz size, and tier ranges.
    #I'm sorry the order of the comments and the dist-bins are reversed

    if size == 'small': #25ct => 5,5,5,5,5 (25%,9%,3.4%,1.1%,0.4%)
        dist = ([.15,2,5],[2,4,5],[4,6,5],[6,8,5],[8,100,5])

    elif size == 'medium': #50ct => 5,10,10,10,15 (25%,18%,6.8%,2.2%,1.1%)
        dist = ([.15,2,15],[2,4,10],[4,6,10],[6,8,10],[8,100,5])

    elif size == 'large': #100ct => 5,10,15,25,45 (25%,18%,10%,5.4%,3.4%)
        dist = ([.15,2,45],[2,4,25],[4,6,15],[6,8,10],[8,100,5])

    elif size == 'special':  #106ct => (25%,9%,5%,5%,5%)
        #5x5x5 Rule => [Min,Max,Bins : 5,5%,5]
        dist = ([.15,2,66],[2,4,23],[4,6,7],[6,8,5],[8,100,5])

    else: #2012ct => Full Table
        print('Invalid size. Pulling full table...')
        cursor.execute(f"SELECT kanji,onyom,kunyom,meaning FROM core WHERE score >= 0.15")
        for i in cursor:
            listy.append(i[0])
        random.shuffle(listy)
        return listy

    for d in dist:
        print(d)
        if joyo == True:
            cursor.execute(f"SELECT idcore FROM core WHERE score >= {d[0]} AND score < {d[1]} AND joyo = 1")
        else:
            cursor.execute(f"SELECT idcore FROM core WHERE score >= {d[0]} AND score < {d[1]}")
        ids = cursor.fetchall()
        setty=set()
        while len(setty) < d[2]:
            setty.add(np.random.randint(ids[0][0],ids[len(ids)-1][0]))
        listy = listy + list(setty)
        random.shuffle(listy)

    quiz = []
    for l in listy:
        cursor.execute(f"SELECT kanji,onyom,kunyom,meaning FROM core WHERE idcore = {l}")
        quiz.append(cursor.fetchone())
    return quiz