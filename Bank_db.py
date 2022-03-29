import sqlite3
from sqlite3 import Error
import datetime

			
class Branch:
	def __init__(self):
		
		self.connection = sqlite3.connect(":memory:")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS branches (
			branch_code INTEGER PRIMARY KEY,
			city TEXT
		)
		""")

		
	def add_branch(self, branch_code, city):
		self.cursor.execute("""
		INSERT INTO 
			branches (branch_code, city)
		VALUES 
			(?, ?)
		""",(branch_code, city))
		self.connection.commit()
	
	def remove_branch(self, branch_code):
		self.cursor.execute("""
		DELETE FROM branches 
		WHERE 
			branch_code= ?
		""",(branch_code,))
		self.connection.commit()
	
	def get_branch(self, branch_code):
		self.cursor.execute("""
		SELECT * FROM branches 
		WHERE branch_code= ?
		""",(branch_code,))
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
	
	def update_branch(self,to_update, update_to, branch_code):
		self.cursor.execute(f"""
		UPDATE
		  branches
		SET {to_update} = ?
		WHERE
		  branch_code = ?
		""",(update_to, branch_code,))
		self.connection.commit()
	
	def get_allbranch(self):
		self.cursor.execute("""
		SELECT * FROM branches 
		""")
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
		
		
class Loan:
	def __init__(self):
		
		self.connection = sqlite3.connect(":memory:")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS loans (
			branch_code INTEGER,
			account_no INTEGER PRIMARY KEY,
			date_of_opening DATE,
			closing_date DATE DEFAULT NULL,
			amount INTEGER,
			Type TEXT,
			prepayment INTEGER,
			balance INTEGER,
			status TEXT DEFAULT UNPAID,
			FOREIGN KEY (branch_code) REFERENCES branches (branch_code),
			FOREIGN KEY (account_no) REFERENCES current_accounts (account_no)
		)
		""")
		
	def addLoan(self, branch_code, account_no, amount, Type, prepayment):
		date_of_opening= datetime.date.today()
		balance= int(amount) - int(prepayment)
		# status= "UNPAID"
		self.cursor.execute("""
		INSERT INTO 
			loans (branch_code, account_no, date_of_opening, amount, Type, prepayment, balance)
		VALUES 
			(?, ?, ?, ?, ?, ?, ?)
		""",(branch_code, account_no, date_of_opening, amount, Type, prepayment, balance))
		self.connection.commit()
	
	def terminate_Loan(self, account_no):
		closing_date= datetime.date.today()
		self.cursor.execute("""
		UPDATE
		  loans
		SET
		  balance = 0,
		  status = "PAID",
		  closing_date = ?
		WHERE
		  account_no = ?
		""",(closing_date, account_no))
		self.connection.commit()
	
	def pay_part(self, account_no, amount):
		self.cursor.execute("""
		UPDATE
		  loans
		SET
		  balance = balance - ?
		WHERE
		  account_no = ?
		""",(int(amount), account_no))
		self.connection.commit()
		
	def update_Loan(self, account_no, to_update, update_to):
		self.cursor.execute(f"""
		UPDATE
		  loans
		SET
		  {to_update} = ?
		WHERE
		  account_no = ?
		""",(update_to, account_no))
		self.connection.commit()
	
	def get_Loan(self, account_no):
		self.cursor.execute("""
		SELECT * FROM loans 
		WHERE account_no= ?
		""",(account_no,))
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)	
			
	def get_allLoans(self):
		self.cursor.execute("""
		SELECT * FROM loans 
		""")
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
		
	def getBalance(self, account_no):
		self.cursor.execute("""
		SELECT balance FROM loans 
		WHERE account_no = ?
		""",(account_no,))
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
		
	def getEMI(self):
		pass 
		
		
class Savings_Account:
	def __init__(self):
		
		self.connection = sqlite3.connect(":memory:")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS savings_accounts (
			customer_Id INTEGER,
			branch_code INTEGER,
			account_no INTEGER PRIMARY KEY,
			date_of_opening DATE,
			min_balance INTEGER,
			balance INTEGER,
			FOREIGN KEY (branch_code) REFERENCES branches (branch_code),
			FOREIGN KEY (customer_Id) REFERENCES customers (customer_Id) 
		)
		""")
		
		
	def add_savingsAccount(self, customer_Id, branch_code, account_no, min_balance, balance):
		
		date_of_opening= datetime.date.today()
		
		self.cursor.execute("""
		INSERT INTO 
			savings_accounts (customer_Id, branch_code, account_no, date_of_opening, min_balance, balance)
		VALUES 
			(?, ?, ?, ?, ?, ?)
		""",(customer_Id, branch_code, account_no, date_of_opening, min_balance, balance))
		self.connection.commit()
		
	def get_savingsAccount(self, account_no):
		self.cursor.execute("""
		SELECT * FROM savings_accounts
		WHERE 
			account_no = ?
		""",(account_no,))
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
		
	def get_allSavingsAccount(self):
		self.cursor.execute("""
		SELECT * FROM savings_accounts
		""")
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
			
	def update_savingsAccount(self, account_no, to_update, update_to):
		self.cursor.execute(f"""
		UPDATE
		  savings_accounts
		SET
		  {to_update} = ?
		WHERE
		  account_no = ?
		""",(update_to, account_no))
		self.connection.commit()
		
		
	def del_savingsAccount(self, account_no):
		self.cursor.execute("""
		DELETE FROM savings_accounts
		WHERE account_no = ?
		""",(account_no,))
		self.connection.commit()
		
	def debitAccount(self,account_no, amount):
		self.cursor.execute("""
		UPDATE
		  savings_accounts
		SET
		  balance = int(balance) - int(?)
		WHERE
		  account_no = ?
		""",(int(amount), account_no))
		self.connection.commit()
		
	def creditAccount(self, amount):
		self.cursor.execute("""
		UPDATE
		  savings_accounts
		SET
		  balance += int(?)
		WHERE
		  account_no = ?
		""",(int(amount), account_no))
		self.connection.commit()
		
	def getBalance(self, account_no):
		self.cursor.execute("""
		SELECT balance 
		FROM savings_accounts
		WHERE account_no = ?
		""",(account_no,))
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
		
class Current_Account():
	def __init__(self):
		
		self.connection = sqlite3.connect(":memory:")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS current_accounts (
			customer_Id INTEGER,
			branch_code INTEGER,
			account_no INTEGER PRIMARY KEY,
			date_of_opening DATE,
			interest_rate INTEGER,
			balance INTEGER,
			FOREIGN KEY (branch_code) REFERENCES branches (branch_code),
			FOREIGN KEY (customer_Id) REFERENCES customers (customer_Id) 
		)
		""")
		
		
	def add_currentAccount(self, customer_Id, branch_code, account_no, interest_rate, balance):
		
		date_of_opening= datetime.date.today()
		
		self.cursor.execute("""
		INSERT INTO 
			current_accounts (customer_Id, branch_code, account_no, date_of_opening, interest_rate, balance)
		VALUES 
			(?, ?, ?, ?, ?, ?)
		""",(customer_Id, branch_code, account_no, date_of_opening, interest_rate, balance))
		self.connection.commit()
		
	def get_currentAccount(self, account_no):
		self.cursor.execute("""
		SELECT * FROM current_accounts
		WHERE 
			account_no = ?
		""",(account_no,))
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
		
	def get_allCurrentAccount(self):
		self.cursor.execute("""
		SELECT * FROM current_accounts
		""")
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
			
	def update_currentAccount(self, account_no, to_update, update_to):
		self.cursor.execute(f"""
		UPDATE
		  current_accounts
		SET
		  {to_update} = ?
		WHERE
		  account_no = ?
		""",(update_to, account_no))
		self.connection.commit()
		
		
	def del_currentAccount(self, account_no):
		self.cursor.execute("""
		DELETE FROM current_accounts
		WHERE account_no = ?
		""",(account_no,))
		self.connection.commit()
		
	def debitAccount(self,account_no, amount):
		self.cursor.execute("""
		UPDATE
		  current_accounts
		SET
		  balance = balance - ?
		WHERE
		  account_no = ?
		""",(int(amount), account_no))
		self.connection.commit()
		
	def creditAccount(self, amount, account_no):
		self.cursor.execute("""
		UPDATE
		  current_accounts
		SET
		  balance += ?
		WHERE
		  account_no = ?
		""",(int(amount), account_no))
		self.connection.commit()
		
	def getBalance(self, account_no):
		self.cursor.execute("""
		SELECT balance 
		FROM current_accounts
		WHERE account_no = ?
		""",(account_no,))
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
		
		
		
class Customer:
	def __init__(self):
		
		self.connection = sqlite3.connect(":memory:")
		self.cursor = self.connection.cursor()
		self.result = None
		
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS customers (
			customer_Id INTEGER PRIMARY KEY,
			first_name TEXT,
			last_name TEXT,
			address TEXT,
			phone_number INTEGER,
			occupation TEXT
		)
		""")
		
	def add_Customer(self, customer_Id, first_name, last_name, address, phone_number, occupation):
		self.cursor.execute("""
		INSERT INTO 
		customers 
			(customer_Id, first_name, last_name, address, phone_number, occupation)
		VALUES 
			(?, ?, ?, ?, ?, ?)
		""", (customer_Id, first_name, last_name, address, phone_number, occupation))
		
		self.connection.commit()
		
	def del_customer(self, customer_Id):
		self.cursor.execute("""
		DELETE FROM customers
		WHERE 
			customer_Id = ?
		""",(customer_Id,))
		
		self.connection.commit()
		
	def get_Customer(self, customer_Id):
		self.cursor.execute("""
		SELECT * FROM customers
		WHERE 
			customer_Id= ?
		""",(customer_Id,))
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
			
	def get_AllCustomers(self):
		self.cursor.execute("""
		SELECT * FROM customers
		""")
		self.result= self.cursor.fetchall()
		for result in self.result:
			print(result)
			
	def update_Customer(self, customer_Id, to_update, update_to):
		self.cursor.execute(f"""
		UPDATE
		  customers
		SET
		  {to_update} = ?
		WHERE
		  customer_Id = ?
		""",(update_to, customer_Id))
		self.connection.commit()
		
		
		
		
if __name__=="__main__":
	
	
	branch= Branch()
	loan= Loan()
	curr_acc = Current_Account()
	sav_acc = Savings_Account()
	customer= Customer()
	
	
	branch.add_branch(101, "Ikorodu")
	branch.add_branch(102, "Ogijo")
	branch.add_branch(103, "Ibeshe")
	branch.get_allbranch()
	branch.update_branch("Isawo", 103)
	branch.get_branch(103)
	
	
	
	loan.addLoan(101, 2051445167, 100000, "Long term", 10000)
	loan.addLoan(101, 2051445154, 150000, "Long term", 12500)
	loan.addLoan(102, 2051486167, 100000, "Long term", 10000)
	loan.addLoan(102, 2059845167, 150000, "Long term", 12500)
	loan.addLoan(103, 2051842667, 100000, "Long term", 10000)
	loan.addLoan(103, 2045445167, 150000, "Long term", 12500)
	loan.get_allLoans()
	loan.terminate_Loan(2045445167)
	loan.pay_part(2051842667, 30000)
	loan.getBalance(2051842667,)
	loan.get_allLoans()


	
	# while True:
	# 	print("Create customer account. Enter 'stop' to stop entry")
	# 	customer_Id= input("Customer Id: ")
	# 	if customer_Id == "stop":
	# 		break
	# 	first_name= input("First name: ")
	# 	last_name= input("Last name: ")
	# 	address= input("Address: ")
	# 	phone_number= input("Phone number: ")
	# 	occupation= input("Occupation: ")
		
	customer.add_Customer(1, "Ayomide", "Oseni", "Ogijo", 8024413341, "programmer")
	customer.add_Customer(2, "Baist", "Buruji", "Ogijo", 9024413341, "Bus. Administrator")
	customer.add_Customer(3, "Mojirola", "Ola", "Ogijo", 7024413341, "Trader")
	customer.add_Customer(4, "Daniel", "Ade", "Olomu", 6024413341, "programmer")
	customer.add_Customer(5, "Teju", "Akeem", "Yaba", 5024413341, "Mathematician")
		
	customer.get_AllCustomers()
	customer.update_Customer(5, "occupation", "Data scientist")
	customer.get_AllCustomers()
	# customer.del_customer(3)
	# customer.get_AllCustomers()
	
	
	curr_acc.add_currentAccount(1, 101, 2051445167, 5, 50000)
	curr_acc.add_currentAccount(3, 102, 2059845167, 5, 45000)
	curr_acc.add_currentAccount(5, 102, 2051486167, 5, 68000)
	curr_acc.get_allCurrentAccount()
	
	
	sav_acc.add_savingsAccount(2, 103, 2045445167, 2000, 5000)
	sav_acc.add_savingsAccount(4, 103, 2051842667, 2000, 6500)
	sav_acc.get_allSavingsAccount()

	
				
	
			
	
				
	
		
	
			
	
		