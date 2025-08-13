import pymongo
print("Welcome to pmongo")
client=pymongo.MongoClient("mongodb://localhost:27017/") #this here is connection to by database
print(client)
db=client["Learning"] #making database name,forming a database
collection=db["expense"]
collection1=db["categories"]
