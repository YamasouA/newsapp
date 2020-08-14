from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

#テーブル定義を買えたいときはmodels.pyをいじる

#継承しているBaseはdatabase.pyで作るインスタンス
class Rireki(Base):
    __tablename__ = 'rireki'
    #主キー
    title = Column(String(128))
    body = Column(Text)
    date = Column(DateTime, default=datetime.now(), primary_key=True)

    def __init__(self, title=None, body=None, date=None):
        self.title = title
        self.body = body
        self.date = date

    #classのインスタンスを表示するときに__repr__または__str__を表示
    #詳しくは検索してね
    def __repr__(self):
        return '<Title %r' % (self.title)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password

    def __repr__(self):
        return '<Name %r>' % (self.user_name)