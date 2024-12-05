from sqlalchemy import create_engine, select, update, and_, insert, delete


class Crud:
    def __init__(self, url, mod):
        self.engine = create_engine(url, future=True)
        self.mod = mod
        self.mod.__table__.create(self.engine, checkfirst=True)

    def exist_id(self, cond):
        with self.engine.connect() as conn:
            stmt = select(self.mod).where(cond).limit(1)
            id = conn.scalar(stmt)
            if id is not None:
                return id
            return None

    def insert(self, dic):
        with self.engine.connect() as conn:
            stmt = insert(self.mod).values(dic)
            conn.execute(stmt)
            conn.commit()

    def upsert(self, cond, dic):
        with self.engine.connect() as conn:
            # cond = and_(BdhPrice.date == dic['date'], BdhPrice.goodsName == dic['goodsName'])
            stmt = select(self.mod).where(cond).limit(1)
            id = conn.scalar(stmt)
            if id is not None:
                stmt = update(self.mod).where(self.mod.id == id).values(dic)
            else:
                stmt = insert(self.mod).values(dic)
            conn.execute(stmt)
            conn.commit()

    def delete(self, cond):
        with self.engine.connect() as conn:
            while True:
                stmt = select(self.mod).where(cond).limit(1)
                id = conn.scalar(stmt)
                if id is None:
                    return
                stmt = delete(self.mod).where(self.mod.id == id)
                conn.execute(stmt)
                conn.commit()
