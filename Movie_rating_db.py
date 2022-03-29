import sqlite3


class Movies:
	def __init__(self):
						
		self.Id= None
		self.title= None
		self.release_year= None
		self.genre= None
		self.collection_in_mil= None
		
		self.connection = sqlite3.connect(":memory:")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS movies (
			id INTEGER PRIMARY KEY,
			title TEXT,
			release_year TEXT,
			genre TEXT,
			collection_in_mil INTEGER
		)
		""")
		
	def addMovies(self):
		print("Enter 'stop' to stop entry")
		while True:
			Id= input("Enter the movie id: ")
			if Id == "stop":
				break
			title= input("Enter the movie title: ")
			release_year= input("Enter the movie release year: ")
			genre= input("Enter the movie genre: ")
			collection_in_mil= input("Enter the movie collection in millions: ")
			
			self.cursor.execute(
				"""
				INSERT INTO
				  movies (id, title, release_year, genre, collection_in_mil)
				VALUES
				  (?, ?, ?, ?, ?);
				""",(Id, title, release_year, genre, collection_in_mil)
				)
			self.connection.commit()
			
	def addMovieList(self, movie_list):
		for Id, title, release_year, genre, collection_in_mil in movie_list:
			
			self.cursor.execute("""
			INSERT INTO
				movies (id, title, release_year, genre, collection_in_mil)
			VALUES
				(?, ?, ?, ?, ?);
				""",(Id, title, release_year, genre, collection_in_mil)
				)
		self.connection.commit()
		
		
	def getAllMovies(self):
		self.cursor.execute("""
		SELECT * FROM movies
		""")
		self.result= self.cursor.fetchall()
		return self.result
			
	def getMovie(self, Id):
		self.cursor.execute("""
			SELECT * FROM movies WHERE id= ? ;
			""",(Id,))
		self.result = self.cursor.fetchall()
		return self.result
		
	def deleteMovie(self, Id):
		self.cursor.execute(f"""
		DELETE FROM movies
		WHERE id = ? ;
		""",(Id,))
		self.connection.commit()

		
class Reviewers:
	def __init__(self):
		self.Id= None
		self.first_name= None
		self.last_name= None
		
		self.connection = sqlite3.connect(":memory:")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS reviewers (
			id INTEGER PRIMARY KEY,
			first_name TEXT,
			last_name TEXT
		)
		""")
		
	def addReviewers(self, Id, first_name, last_name):
		self.cursor.execute("""
		INSERT INTO 
			reviewers (id, first_name, last_name)
		VALUES 
			(?, ?, ?)
		""",(Id, first_name, last_name))
		self.connection.commit()
		
	def addReviewersList(self, reviewers_list):
		insert_reviewers_query = """
		INSERT INTO reviewers 
		(id, first_name, last_name)
		VALUES (?, ?, ? )
		"""
		
		self.cursor.executemany(insert_reviewers_query, reviewers_list)
		self.connection.commit()
		
	def getAllReviewers(self):
		self.cursor.execute("""
		SELECT * FROM reviewers
		""")
		self.result= self.cursor.fetchall()
		return self.result
			
	def getReviewer(self, Id):
		self.cursor.execute("""
			SELECT * FROM reviewers WHERE id= ? ;""", (Id,))
		self.result = self.cursor.fetchall()
		return self.result
		
	def deleteReviewer(self, Id):
		self.cursor.execute("""
		DELETE FROM reviewers
		WHERE id = ? ;""", (Id,))
		self.connection.commit()
		
		
class Ratings:
	def __init__(self):
		self.movies_id= None
		self.reviewers_id= None
		self.rating= None
		
		self.connection = sqlite3.connect(":memory:")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE ratings (
		   movie_id INT,
		   reviewer_id INT,
		   rating DECIMAL(2,1),
		   FOREIGN KEY(movie_id) REFERENCES movies(id),
		   FOREIGN KEY(reviewer_id) REFERENCES reviewers(id))
		""")
		
	def addRatings(self, movie_id, reviewer_id, rating):
		self.cursor.execute("""
		INSERT INTO 
			ratings (movie_id, reviewer_id, rating)
		VALUES 
			(?, ?, ?)
		""",(movie_id, reviewer_id, rating))
		self.connection.commit()
		
	def addRatingsList(self, ratings_list):
		insert_ratings_query = """
		INSERT INTO ratings 
			(movie_id, reviewer_id, rating)
		VALUES (?, ?, ? )
		"""
		
		self.cursor.executemany(insert_ratings_query, ratings_list)
		self.connection.commit()
		
	def getAllRatings(self):
		self.cursor.execute("""
		SELECT * FROM ratings
		""")
		self.result= self.cursor.fetchall()
		return self.result
			
	def getRating(self, movie_id, reviewer_id):
		self.cursor.execute("""
			SELECT * FROM ratings WHERE 
				reviewer_id= ?,
				movie_id= ? ;""", (reviewer_id, movie_id))
		self.result = self.cursor.fetchall()
		return self.result
		
	def deleteRating(self, movie_id, reviewer_id):
		self.cursor.execute("""
		DELETE FROM ratings
		WHERE 
			movie_id= ?,
			reviewer_id= ?;""", (movie_id, reviewer_id))
		self.connection.commit()
		
		
if __name__=="__main__":
	
	admin= Movies()
	
	movie_list= [
	   (1, "Forrest Gump", 1994, "Drama", 330.2),
	   (2, "3 Idiots", 2009, "Drama", 2.4),
	   (3, "Eternal Sunshine of the Spotless Mind", 2004, "Drama", 34.5),
	   (4, "Good Will Hunting", 1997, "Drama", 138.1),
	   (5, "Skyfall", 2012, "Action", 304.6),
	   (6, "Gladiator", 2000, "Action", 188.7),
	   (7, "Black", 2005, "Drama", 3.0),
	   (8, "Titanic", 1997, "Romance", 659.2),
	   (9, "The Shawshank Redemption", 1994, "Drama",28.4),
	   (10, "Udaan", 2010, "Drama", 1.5),
	   (11, "Home Alone", 1990, "Comedy", 286.9),
	   (12, "Casablanca", 1942, "Romance", 1.0),
	   (13, "Avengers: Endgame", 2019, "Action", 858.8),
	   (14, "Night of the Living Dead", 1968, "Horror", 2.5),
	   (15, "The Godfather", 1972, "Crime", 135.6),
	   (16, "Haider", 2014, "Action", 4.2),
	   (30, "Inception", 2010, "Adventure", 293.7),
	   (17, "Evil", 2003, "Horror", 1.3),
	   (18, "Toy Story 4", 2019, "Animation", 434.9),
	   (19, "Air Force One", 1997, "Drama", 138.1),
	   (20, "The Dark Knight", 2008, "Action",535.4),
	   (21, "Bhaag Milkha Bhaag", 2013, "Sport", 4.1),
	   (22, "The Lion King", 1994, "Animation", 423.6),
	   (23, "Pulp Fiction", 1994, "Crime", 108.8),
	   (24, "Kai Po Che", 2013, "Sport", 6.0),
	   (25, "Beasts of No Nation", 2015, "War", 1.4),
	   (26, "Andadhun", 2018, "Thriller", 2.9),
	   (27, "The Silence of the Lambs", 1991, "Crime", 68.2),
	   (28, "Deadpool", 2016, "Action", 363.6),
	   (29, "Drishyam", 2015, "Mystery", 3.0),
		]
	
	admin.addMovieList(movie_list)
	print(admin.getAllMovies())
	print(admin.getMovie(30))
	admin.deleteMovie(30)
	print(admin.getAllMovies())
	
	review= Reviewers()
	review.addReviewers(30, "Ayomide", "Oseni")
	
	reviewers_records = [
	   (1, "Chaitanya", "Baweja"),
	   (2, "Mary", "Cooper"),
	   (3, "John", "Wayne"),
	   (4, "Thomas", "Stoneman"),
	   (5, "Penny", "Hofstadter"),
	   (6, "Mitchell", "Marsh"),
	   (7, "Wyatt", "Skaggs"),
	   (8, "Andre", "Veiga"),
	   (9, "Sheldon", "Cooper"),
	   (10, "Kimbra", "Masters"),
	   (11, "Kat", "Dennings"),
	   (12, "Bruce", "Wayne"),
	   (13, "Domingo", "Cortes"),
	   (14, "Rajesh", "Koothrappali"),
	   (15, "Ben", "Glocker"),
	   (16, "Mahinder", "Dhoni"),
	   (17, "Akbar", "Khan"),
	   (18, "Howard", "Wolowitz"),
	   (19, "Pinkie", "Petit"),
	   (20, "Gurkaran", "Singh"),
	   (21, "Amy", "Farah Fowler"),
	   (22, "Marlon", "Crafford"),
	]
	review.addReviewersList(reviewers_records)
	print(review.getAllReviewers())
	print(review.getReviewer(30))
	print()
	review.deleteReviewer(30)
	print()
	print(review.getAllReviewers())
	
	
	rating= Ratings()
	
	ratings_records = [
	    (6.4, 17, 5), (5.6, 19, 1), (6.3, 22, 14), (5.1, 21, 17),
	    (5.0, 5, 5), (6.5, 21, 5), (8.5, 30, 13), (9.7, 6, 4),
	    (8.5, 24, 12), (9.9, 14, 9), (8.7, 26, 14), (9.9, 6, 10),
	    (5.1, 30, 6), (5.4, 18, 16), (6.2, 6, 20), (7.3, 21, 19),
	    (8.1, 17, 18), (5.0, 7, 2), (9.8, 23, 3), (8.0, 22, 9),
	    (8.5, 11, 13), (5.0, 5, 11), (5.7, 8, 2), (7.6, 25, 19),
	    (5.2, 18, 15), (9.7, 13, 3), (5.8, 18, 8), (5.8, 30, 15),
	    (8.4, 21, 18), (6.2, 23, 16), (7.0, 10, 18), (9.5, 30, 20),
	    (8.9, 3, 19), (6.4, 12, 2), (7.8, 12, 22), (9.9, 15, 13),
	    (7.5, 20, 17), (9.0, 25, 6), (8.5, 23, 2), (5.3, 30, 17),
	    (6.4, 5, 10), (8.1, 5, 21), (5.7, 22, 1), (6.3, 28, 4),
	    (9.8, 13, 1)
	]
	
	rating.addRatingsList(ratings_records)
	print(rating.getAllRatings())
	
	
	
	
# lRatings())
	
	
	
	
	
