import sqlite3
import datetime

class Manager:
	def __init__(self):
		# self.managerId
		# self.first_name
		# self.last_name
		# self.age 
		# self.yrs_of_experience
		
		
		self.connection = sqlite3.connect("music.db")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS manager (
			managerId INTEGER PRIMARY KEY,
			first_name TEXT,
			last_name TEXT,
			age INTEGER,
			yrs_of_experience INTEGER
		)
		""")
		
		
	def add_manager(self, managerId, first_name, last_name, age, yrs_of_experience):
		self.cursor.execute("""
		INSERT INTO 
			manager 
				(managerId, 
				first_name, 
				last_name,
				age, 
				yrs_of_experience)
		VALUES 
			(?, ?, ?, ?, ?)
		""",	(managerId, 
				first_name, 
				last_name, 
				age, 
				yrs_of_experience))
		self.connection.commit()
		
			
	def del_manager(self, managerId):
		self.cursor.execute("""
		DELETE FROM manager
		WHERE managerId = ?
		""", (managerId,))
		
		print(f"Manager: {managerId} deleted successfully")
		self.connection.commit()
				
	def display_manager(self, managerId):
		self.cursor.execute("""
		SELECT * FROM manager 
		WHERE managerId= ?
		""",(managerId,))
		
		for row in self.cursor:
			print(row)
			
	def update_manager(self, managerId, to_update, update_to):
		self.cursor.execute("""
		UPDATE
		  manager
		SET
		  ? = ?
		WHERE
		  managerId = ?
		""",(to_update, update_to, managerId))
		self.connection.commit()

			
class Album:
	def __init__(self):
		# self.album_name
		# self.artist_name
		# self.date_created
		## Will have the artist name as a foreign key and as a primary key
	
		self.connection = sqlite3.connect("music.db")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS album (
			artist_name INTEGER PRIMARY KEY,
			album_name TEXT,
			date_created DATE,
			FOREIGN KEY (artist_name) REFERENCES artist (artist_name) 
		)
		""")

	def add_album(self, album_name, artist_name):
		
		date_created= datetime.date.today()
		
		self.cursor.execute("""
		INSERT INTO 
			album 
				(artist_name, 
				album_name, 
				date_created)
		VALUES 
			(?, ?, ?)
		""",	(artist_name, 
				album_name, 
				date_created))
		self.connection.commit()
	
	def del_album(self, album_name):
		self.cursor.execute("""
		DELETE FROM album
		WHERE album_name = ?
		""", (album_name,))
		
		print(f"Album: {album_name} deleted successfully")
		self.connection.commit()
		
	def display_album(self, album_name):
		self.cursor.execute("""
		SELECT * FROM album 
		WHERE album_name= ?
		""",(album_name,))
		
		for row in self.cursor:
			print(row)
			
	def update_album(self, album_name, to_update, update_to):
		self.cursor.execute("""
		UPDATE
		  album
		SET
		  ? = ?
		WHERE
		  album_name = ?
		""",(to_update, update_to, album_name))
		self.connection.commit()

			
class Tracks:
	def __init__(self):
		# self.title
		# self.album_name
		### ablum_name as foreign key
		
		self.connection = sqlite3.connect("music.db")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS tracks (
			album_name TEXT PRIMARY KEY,
			title TEXT,
			FOREIGN KEY (album_name) REFERENCES album (album_name)
		)
		""")

	def add_track(self, album_name, title):
		
		self.cursor.execute("""
		INSERT INTO 
			tracks 
				(album_name, 
				title)
		VALUES 
			(?, ?)
		""",(album_name, title))
		self.connection.commit()
	
	def del_track(self, title):
		self.cursor.execute("""
		DELETE FROM tracks
		WHERE title = ?
		""", (title,))
		
		print(f"Track: {title} deleted successfully")
		self.connection.commit()
		
	def display_track(self, title):
		self.cursor.execute("""
		SELECT * FROM tracks 
		WHERE title= ?
		""",(title,))
		
		for row in self.cursor:
			print(row)
			
	def update_track(self, title, to_update, update_to):
		self.cursor.execute("""
		UPDATE
		  tracks
		SET
		  ? = ?
		WHERE
		  title = ?
		""",(to_update, update_to, title))
		self.connection.commit()
			

class Singles:
	def __init__(self):
		# self.title
		# self.style
		# self.artist_name
		
		## Will have the artist name as a foreign key and as a primary key

		self.connection = sqlite3.connect("music.db")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS singles (
			artist_name TEXT PRIMARY KEY,
			title TEXT,
			style TEXT,
			FOREIGN KEY (artist_name) REFERENCES artist (artist_name)
		)
		""")

	def add_single(self, artist_name, title, style):
		
		self.cursor.execute("""
		INSERT INTO 
			singles 
				(artist_name, 
				title,
				style)
		VALUES 
			(?, ?, ?)
		""",(artist_name, title, style))
		self.connection.commit()
	
	def del_single(self, title):
		self.cursor.execute("""
		DELETE FROM singles
		WHERE title = ?
		""", (title,))
		
		print(f"Single: {title} deleted successfully")
		self.connection.commit()
		
	def display_single(self, title):
		self.cursor.execute("""
		SELECT * FROM tracks 
		WHERE title= ?
		""",(title,))
		
		for row in self.cursor:
			print(row)
			
	def update_single(self, title, to_update, update_to):
		self.cursor.execute("""
		UPDATE
		  tracks
		SET
		  ? = ?
		WHERE
		  title = ?
		""",(to_update, update_to, title))
		self.connection.commit()
		
			
class Artist:
	def __init__(self):
		
		# self.managerId
		# self.artist_name
		# self.style
		
		self.connection = sqlite3.connect("music.db")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS artists (
			managerId INTEGER,
			artist_name TEXT PRIMARY KEY,
			age INTEGER,
			style TEXT,
			FOREIGN KEY (managerId) REFERENCES manager (managerId)
		)
		""")
		
		
	def add_artist(self,managerId, artist_name, age, style):
		self.cursor.execute("""
		INSERT INTO 
			artists (managerId, artist_name, age, style)
		VALUES 
			(?, ?, ?, ?)
		""",(managerId, artist_name, age, style))
		self.connection.commit()
		
			
	def del_artist(self, artist_name):
		self.cursor.execute("""
		DELETE FROM artists
		WHERE artist_name = ?
		""", (artist_name,))
		
		print(f"Artist: {artist_name} deleted successfully")
		self.connection.commit()
		
	def display_artist(self, artist_name):
		self.cursor.execute("""
		SELECT * FROM artists 
		WHERE artist_name= ?
		""",(artist_name,))
		
		for row in self.cursor:
			print(row)
			
	def update_artist(self, artist_name, to_update, update_to):
		self.cursor.execute("""
		UPDATE
		  tracks
		SET
		  ? = ?
		WHERE
		  artist_name = ?
		""",(to_update, update_to, artist_name))
		self.connection.commit()
		
		
		
if __name__=="__main__":
	
	manager= Manager()
	album= Album()
	singles= Singles()
	tracks= Tracks()
	artist= Artist()
	
	# while True:
	# 	print("Enter 'stop' to stop entry")
	# 	managerId= input("Create a manager Id: ")
	# 	if managerId=="stop":
	# 		break
	# 	first_name=input("Enter your first name: ")
	# 	last_name= input("Enter your last name: ")
	# 	age = input("Enter your age: ")
	# 	yrs_of_experience= input("Enter your years of experience: ")
	# 	manager.add_manager(managerId, first_name, last_name, age, yrs_of_experience)
		
	# Id = input("Enter manager Id to display")
	# manager.display_manager(Id)
	
	
	
	# while True:
	# 	print("Enter 'stop' to stop entry")
	# 	managerId= input("Enter your manager Id: ")
	# 	if managerId=="stop":
	# 		break
	# 	artist_name=input("Enter your stage name: ")
	# 	age = input("Enter your age: ")
	# 	style= input("Enter your year style of singer: ")
	# 	artist.add_artist(managerId, artist_name, age, style)
		
	# artist_name = input("Enter artist name to display")
	# artist.display_artist(artist_name)
	
	

	
	
	
	
# ursor.execute("""
# 	SELECT * FROM manager, artists 
# 	WHERE 
# 		managerId= 101
# 	""")
# 	for details in artist.cursor:
# 		for detail in details:
# 			print(detail)

	
	
	
	
