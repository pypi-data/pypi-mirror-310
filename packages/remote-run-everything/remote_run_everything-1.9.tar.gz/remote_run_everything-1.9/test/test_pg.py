from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, and_, DateTime
from remote_run_everything.crud.crud import Crud
base = declarative_base()


class Kv(base):
    __tablename__ = "kv"
    id = Column(Integer, primary_key=True)
    k = Column(String(20))
    v = Column(String(20))
    updated = Column(DateTime)


if __name__ == '__main__':
    url = "postgresql://postgres:iamrich@39.96.40.177:5432/projects"
    crude = Crud(url, Kv)
    cond = and_(Kv.k == "aqa")
    crude.delete(cond)
    crude.upsert(cond, {"k": "aqa", "v": "adsf"})
    crude.upsert(cond, {"k": "aqa", "v": "adsf"})
    crude.insert({"k": "aqa", "v": "adsf"})
