from database import Database

db = Database("database.db")
db.remove_db()
db.create_db()
