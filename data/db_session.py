import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy.pool import QueuePool

# Base class for models to inherit from
SqlAlchemyBase = dec.declarative_base()

# Factory for creating sessions
__factory = None

def global_init(db_file: str):
    """Initialize the global database connection and session factory.
    
    Args:
        db_file (str): The path to the database file.
    
    Raises:
        Exception: If the database file is not specified.
    """
    global __factory

    # Check if the factory is already initialized
    if __factory:
        return

    # Validate the database file path
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    # Create the connection string
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    # Create the database engine with a QueuePool for connection pooling
    engine = sa.create_engine(conn_str, echo=False, poolclass=QueuePool, pool_size=10, max_overflow=20)
    __factory = orm.sessionmaker(bind=engine)

    # Import all models to ensure they are registered with SQLAlchemy
    from . import __all_models

    # Create tables for all models
    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    """Create a new session for interacting with the database.
    
    Returns:
        Session: A new SQLAlchemy session.
    """
    global __factory
    if __factory is None:
        raise Exception("Database not initialized. Call global_init() first.")
    return __factory()