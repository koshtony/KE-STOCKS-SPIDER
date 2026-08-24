from app.database.connection import engine
from app.database.models import Base


def init_database():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_database()

    from app.scheduler.jobs import start_scheduler

    start_scheduler()