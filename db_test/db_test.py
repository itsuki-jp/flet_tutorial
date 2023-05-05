from tinydb import TinyDB, Query

db = TinyDB("./todo_app/db.json")

for item in db:
    print(item.doc_id)