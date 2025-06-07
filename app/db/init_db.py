from app.db.base import Base
from app.db.session import engine

def init_db():
    print("Initializing database...")
    print(f"Database URL: {engine.url}")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 