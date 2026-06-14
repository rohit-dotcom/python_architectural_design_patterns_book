from sqlalchemy import create_engine, text
from config import get_postgres_url
import orm
from sqlalchemy.orm import sessionmaker
import repository
import config


url = get_postgres_url()
print(url)

orm.start_mapper()
get_session=sessionmaker(bind=create_engine(config.get_postgres_url()))

engine = create_engine(url)
with engine.connect() as conn:
    session=get_session()
    batches=repository.SQLAlchemyRepository(session).list()
    print(batches)

    # result = conn.execute(text("SELECT * from batches"))
    # print(result.all())