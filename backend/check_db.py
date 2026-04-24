from sqlalchemy import create_engine, text
from app.core.settings import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname='public';")
    )
    print(list(result))