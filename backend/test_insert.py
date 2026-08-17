from app.db.base import Base
from app.db.session import SessionLocal
from app.db.models.user import User

db = SessionLocal()

user = User(
    name="Suprit",
    email="suprit@test.com",
    password_hash="password123",
)

db.add(user)
db.commit()

print("User inserted successfully")

db.close()