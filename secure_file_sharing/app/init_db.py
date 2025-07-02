from .database import engine
from .models import Base

def init():
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    init()