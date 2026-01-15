from core.config import Settings

if not Settings().ENABLE_DB:
    engine = None

    async def get_db():
        raise RuntimeError("Database disabled in DEV mode")

else:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session


    engine = create_engine(Settings().DATABASE_URL)

    def get_db_session() -> Session:
        with Session(engine) as session:
            yield session
            