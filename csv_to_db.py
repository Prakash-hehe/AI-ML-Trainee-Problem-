import csv
import sqlite3

# ─────────────────────────────────────────────
# STEP 1: Connect & Create Table
# ─────────────────────────────────────────────
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
''')
conn.commit()
print("✅ Table created (or already exists)\n")


# ─────────────────────────────────────────────
# STEP 2: Import CSV → Database
# ─────────────────────────────────────────────
with open('users.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            cursor.execute(
                'INSERT INTO users (name, email) VALUES (?, ?)',
                (row['name'], row['email'])
            )
        except sqlite3.IntegrityError:
            print(f"⚠️  Skipped duplicate: {row['email']}")

conn.commit()
print("✅ CSV data imported successfully!\n")


# ─────────────────────────────────────────────
# STEP 3: Read All Records
# ─────────────────────────────────────────────
print("📋 All Users in Database:")
print(f"{'ID':<5} {'Name':<20} {'Email'}")
print("-" * 50)
cursor.execute('SELECT * FROM users')
for row in cursor.fetchall():
    print(f"{row[0]:<5} {row[1]:<20} {row[2]}")


# ─────────────────────────────────────────────
# STEP 4: Search a User by Name
# ─────────────────────────────────────────────
print("\n🔍 Search Result for 'Priya':")
cursor.execute("SELECT * FROM users WHERE name LIKE ?", ('%Priya%',))
result = cursor.fetchall()
if result:
    for row in result:
        print(f"  ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
else:
    print("  No user found.")


# ─────────────────────────────────────────────
# STEP 5: Update a User's Email
# ─────────────────────────────────────────────
cursor.execute(
    "UPDATE users SET email = ? WHERE name = ?",
    ('aarav.new@example.com', 'Aarav Sharma')
)
conn.commit()
print("\n✏️  Updated Aarav Sharma's email.")


# ─────────────────────────────────────────────
# STEP 6: Delete a User
# ─────────────────────────────────────────────
cursor.execute("DELETE FROM users WHERE name = ?", ('Pooja Joshi',))
conn.commit()
print("🗑️  Deleted Pooja Joshi from database.")


# ─────────────────────────────────────────────
# STEP 7: Show Final Record Count
# ─────────────────────────────────────────────
cursor.execute("SELECT COUNT(*) FROM users")
count = cursor.fetchone()[0]
print(f"\n📊 Total users in database: {count}")


# ─────────────────────────────────────────────
# STEP 8: Close Connection
# ─────────────────────────────────────────────
conn.close()
print("\n🔒 Database connection closed.")
