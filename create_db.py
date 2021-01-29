import sqlite3  
      
con = sqlite3.connect("pass_manager.db")  
print("Database opened successfully")  
      
con.execute("create table admin_cred (userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)")  
print("admin_cred table created successfully") 
con.execute("create table s_admin_cred (userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)")  
print("s_admin_cred table created successfully") 
con.execute("create table intern_cred (userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)")  
print("intern_cred table created successfully")  
con.execute("create table login_cred (userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)")  
print("login_cred table created successfully")
con.execute("create table login_cred_adm (userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)")  
print("login_cred_adm table created successfully")     
con.close()  