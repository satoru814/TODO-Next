import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

def get_tables(Base):
    class Oldtask(Base):
        __tablename__ = "old_task"  # テーブル名を指定
        id = Column(Integer, primary_key=True)
        # done_time = Column(String(255))
        # push_time = Column(String(255))
        task_title = Column(String(255))
        comment = Column(String(255))
        start_time = DateTime()
        done_time = DateTime()

    tables = {Oldtask.__tablename__: Oldtask}
    return tables

class DB:
    def __init__(self, engine=None):
        if engine:
            self.engine = engine
        else:
            self.engine = create_engine("sqlite:///old_task.db")

        self.Base = declarative_base()
        self.tables = get_tables(self.Base)
        self.Base.metadata.create_all(self.engine)
        SessionClass = sessionmaker(self.engine)  # セッションを作るクラスを作成
        self.session = SessionClass()

    @classmethod
    def load_local(cls, filepath="sqlite:///old_task.db"):
        cls(create_engine(filepath))
        
    def add(self, task_to_json, table_name="old_task"):
        table = self.tables[table_name]
        self.session.add(table(**task_to_json))
        self.session.commit()
    
    def to_langchain_db(self):
        return SQLDatabase(engine=self.engine)
    
    # def select_with_condition(self, table_name: str, condition: dict) -> str:
    #     table = self.tables[table_name]
    #     for column, value in condition.items():
    #         condition = (getattr(table, column) == value)
    #     state = select(table_name).where(condition)
    #     res = self.session.execute(state)[0]
    #     return res