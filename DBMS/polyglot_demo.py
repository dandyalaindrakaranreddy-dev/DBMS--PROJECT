import psycopg2
from pymongo import MongoClient


# ==========================================
# 1. CONNECT TO POSTGRESQL
# ==========================================

pg_connection = psycopg2.connect(
    host="localhost",
    database="polyglot_demo",
    user="postgres",
    password="9347204784",
    port="5432"
)

pg_cursor = pg_connection.cursor()

# Student to search
student_id = 1

# Get student data from PostgreSQL
pg_cursor.execute(
    """
    SELECT student_id, name, marks
    FROM students
    WHERE student_id = %s
    """,
    (student_id,)
)

student = pg_cursor.fetchone()

print("====================================")
print("POSTGRESQL DATA")
print("====================================")

if student:
    print("Student ID :", student[0])
    print("Name       :", student[1])
    print("Marks      :", student[2])
else:
    print("Student not found")


# ==========================================
# 2. CONNECT TO MONGODB ATLAS
# ==========================================

mongo_uri = "YOUR_MONGODB_ATLAS_CONNECTION_STRING"

mongo_client = MongoClient(mongo_uri)

mongo_db = mongo_client["polyglot_demo"]

collection = mongo_db["students1"]

# Get student details from MongoDB
details = collection.find_one(
    {"student_id": student_id}
)

print("\n====================================")
print("MONGODB DATA")
print("====================================")

if details:

    print("Skills :", details["skills"])

    print("Projects:")

    for project in details["projects"]:
        print("  Project Name :", project["name"])
        print("  Technology    :", project["technology"])

else:
    print("Student details not found")


# ==========================================
# 3. COMBINE BOTH DATABASES
# ==========================================

print("\n====================================")
print("POLYGLOT PERSISTENCE RESULT")
print("====================================")

if student and details:

    print("Student ID :", student[0])
    print("Name       :", student[1])
    print("Marks      :", student[2])
    print("Skills     :", ", ".join(details["skills"]))

    print("Project    :", details["projects"][0]["name"])
    print("Technology :", details["projects"][0]["technology"])


# ==========================================
# 4. CLOSE DATABASE CONNECTIONS
# ==========================================

pg_cursor.close()
pg_connection.close()
mongo_client.close()

print("\n====================================")
print("DATABASE CONNECTIONS CLOSED")
print("====================================")