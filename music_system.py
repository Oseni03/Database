import sqlite3
import datetime
connection= sqlite3.connect("music.db")
cursor= connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS managers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname VARCHAR(100),
    lname VARCHAR(100),
    birthdate DATE,
    experience INTEGER,
    email VARCHAR(100),
    date_created DATE,
    password VARCHAR(100)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname VARCHAR(100),
    lname VARCHAR(100),
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    mgr_id INTEGER,
    date_created DATE,
    FOREIGN KEY (mgr_id) REFERENCES managers (id) ON DELETE CASCADE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS albums (
id INTEGER AUTO_INCREMENT,
artist_id INTEGER,
title VARCHAR(100),
date_created DATE,
PRIMARY KEY (id, artist_id)
FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS tracks (
id INTEGER AUTO_INCREMENT,
title VARCHAR(100),
album_id INTEGER,
date_created DATE,
PRIMARY KEY (id, album_id)
FOREIGN KEY (album_id) REFERENCES albums (id) ON DELETE CASCADE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS singles (
id INTEGER AUTO_INCREMENT,
title VARCHAR(100),
artist_id INTEGER,
date_created DATE,
FOREIGN KEY (artist_id) REFERENCES artists (id) ON DELETE CASCADE
)
""")


def sign_up():
    print()
    print("Manager Sign Up")
    fname = input(str("Enter your first name: "))
    lname = input(str("Enter your last name: "))
    birthdate= input("Enter your date of birth: DD/MM/YYYY: ")
    experience= input("Enter your years of experience: ")
    email= input(str("Email: "))
    password= input(str("Password: "))
    date = datetime.date.today()
    
    cursor.execute("""
                   INSERT INTO 
                   managers 
                    (fname, lname, birthdate, experience, email, password, date_created)
                   VALUES
                    (?, ?, ?, ?, ?, ?, ?)
                   """,(fname,lname, birthdate, int(experience), email, password, date))
    connection.commit()
    print(f"{fname.title()} account created successfully")
    auth_manager()

def create_artist(id):
  print()
  print("Create Artist account")
  fname= input(str("First name: "))
  lname= input(str("Last name: "))
  username= input(str("Username: "))
  password= input(str("Password: "))
  date = datetime.date.today()
  
  cursor.execute("""
  INSERT INTO artists 
    (fname,lname,username,password,mgr_id,date_created)
  VALUES
    (?,?,?,?,?,?)
  """,(fname,lname,username,password,id,date))
  connection.commit()
  print(f"{username} account created successfully")
  
def delete_artist(id):
  print()
  print("Delete Artist")
  username = input(str("Artist username to delete: "))
  cursor.execute("""
  DELETE FROM artists 
  WHERE username = ?
  AND mgr_id = ?
  """,(username,id))
  print(f"{username} account deleted successfully")
  
def search():
  while True:
    print()
    print("Search Menu")
    print("1. Search for album")
    print("2. Search for track")
    print("3. Search for single")
    print("4. Exit")
    
    user_option= input(str("Option: "))
    if user_option == "1":
          print()
          print("Album Search")
          to_search= input(str("Album title to search: "))
          cursor.execute("""
                          SELECT title FROM albums;
                          """)          
          titles= cursor.fetchall()
          result = []
          for title in titles:
                for name in title:
                      result.append(name)
          if to_search in result:
                cursor.execute("""
                               SELECT title, date_created
                               FROM tracks
                               WHERE album_id = (
                               SELECT id FROM albums 
                               WHERE title = ? 
                               """,(to_search,))
                titles = cursor.fetchall()
                for title in titles:
                      print()
                      print(to_search)
                      print("Search results include:")
                      print(title)                      
    elif user_option == "2":
          print()
          print("Track Search")
          track = input(str("Enter track to search: "))
          cursor.execute("SELECT title, date_created FROM tracks WHERE title = ? ",(track,))
          a = cursor.fetchall()
          if a:
              print(track + " found")
              for b in a:
                  print(b)
          else:
            print(track + " not found")
            
    elif user_option == "3":
          print()
          print("Single Search")
          single = input(str("Enter single title to search: "))
          cursor.execute("SELECT title, date_created FROM singles WHERE title = ? ",(single,))
          a = cursor.fetchall()
          if a:
              print(single + " found")
              for b in a:
                  print(b)
          else:
            print(single + " not found")

def manager_session(id):
    while True:
        print()
        print("Welcome Manager")
        print("Manager Menu")
        print("1. Create Artist")
        print("2. Delete Artist")
        print("3. View Artists")
        print("4. View Artist albums, tracks and singles")
        print("5. Search")
        print("6. Logout")
        
        user_option= input(str("Option: "))
        if user_option == "1":
            create_artist(id)
        elif user_option == "2":
            delete_artist(id)
        elif user_option == "3":
            cursor.execute("SELECT * FROM artists WHERE mgr_id= ?",(id,))
            a= cursor.fetchall()
            for rows in a:
                print("Artists info:")
                print(rows)
        elif user_option == "4":
            print()
            cursor.execute("""
                           SELECT id, fname, lname, username, date_created
                           FROM artists
                           """)
            rows = cursor.fetchall()
            for row in rows:
                  print()
                  print(f"Artist: {row[3]}")
                  print(row)
                  cursor.execute("SELECT id, title, date_created FROM albums WHERE artist_id = ?",(row[0],))
                  rows=cursor.fetchall()
                  for row in rows:
                      print("Albums")
                      print(f"\t{row}")
                      cursor.execute("SELECT id, title, date_created FROM tracks WHERE album_id = ?",(row[0],))
                      rows = cursor.fetchall()
                      for row in rows:
                        print(f"\t{row}")
                  print("Singles")
                  cursor.execute("SELECT title, date_created FROM singles WHERE artist_id = ? ",(row[0],))
                  rows = cursor.fetchall()
                  for row in rows:
                      print(f"\t{row}")
        elif user_option == "5":
            search()
        elif user_option == "6":
            break
        else:
            print("Invalid option selected")
        
def add_track(album_id):
  while True:
    print()
    print("Add Track")
    title= input(str("Enter track title: "))
    date = datetime.date.today()
    cursor.execute("""
    INSERT INTO tracks (title, album_id, date_created)
    VALUES (?, ?, ?)
    """,(title, album_id, date))
    connection.commit()
    print(f"Track-{title} added successfully")
    print()
    exit= input("Add another(Y/N): ")
    if exit == "N":
      break
    elif exit == "Y":
      continue
    else:
      print("Invalid selection")

def create_album(id):
  print()
  print("Create Album")
  title = input(str("Album title: "))
  date = datetime.date.today()
  cursor.execute("""
  INSERT INTO albums (artist_id, title, date_created)
  VALUES
    (?, ?, ?)
  """,(int(id), title, date))
  connection.commit()
  print(f"Album {title} created successfully")
  
  cursor.execute("""
  SELECT id FROM albums 
  WHERE artist_id = ?
  AND title = ?
  """,(int(id), title))
  a= cursor.fetchall()
  for row in a:
    album_id = row[0]
    print(album_id)
    add_track(album_id)
  #exit= input("Done(Y/N): ")
  #if exit == "Y":
  #  break
  #elif exit == "N":
  #  continue
  #else:
  #  print("Invalid selection")
    
def create_single(id):
  print()
  print("Create Single")
  title= input(str("Single title: "))
  date = datetime.date.today()

  cursor.execute("""
  INSERT INTO singles (title, artist_id, date_created)
  VALUES (?, ?, ?)
  """,(title, int(id), date))
  print(f"Single-{title} created successfully")

def artist_session(id, username):
  while True:
    print()
    print(f"Welcome {username}")
    print()
    print("Artist Menu")
    print("1. Create New Album")
    print("2. Create New single")
    print("3. Logout")
    
    user_option = input(str("Option: "))
    if user_option == "1":
      create_album(id)
    elif user_option == "2":
      create_single(id)
    elif user_option == "3":
      break
    else:
      print("Invalid option selected")

def auth_manager():
    print()
    print("Manager Login")
    email= input(str("Email: "))
    password= input(str("Password: "))

    cursor.execute("""
                SELECT * FROM managers
                WHERE email = ?
                AND password = ?
                """,(email, password))
    a = cursor.fetchall()
    if a:
        cursor.execute("""SELECT id 
                    FROM managers 
                    WHERE email= ? 
                    AND password= ?
                      """,(email, password))
        b= cursor.fetchall()
        for row in b:
            for id in row:
                manager_session(id)
    else:
        print("Invalid login details")
                
def auth_artist():
    print()
    print("Artist Login")
    username= input(str("Username: "))
    password= input(str("Password: "))

    cursor.execute("SELECT * FROM artists WHERE username = ? AND password = ? ",(username, password))
    a = cursor.fetchall()
    if a:
        cursor.execute("""SELECT id 
                    FROM artists 
                    WHERE username= ? 
                    AND password= ?
                    """,(username,password))
        a= cursor.fetchall()
        for row in a:
            for id in row:
                artist_session(id, username)
    else:
        print("Incorrect login details")

def main():
    while True:
        print()
        print("Welcome to Music System")
        print("1. Login as Manager")
        print("2. Login as Artist")
        print("3. Manager Sign up")
        print("4. Exit")

        user_option = input(str("Option: "))
        if user_option == "1":
            auth_manager()
        elif user_option == "2":
            auth_artist()
        elif user_option == "3":
            sign_up()
        elif user_option == "4":
            break
        else:
            print("Invalid option selected")
main()