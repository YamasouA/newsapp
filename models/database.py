from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
#DBの接続情報(接続先のDB等）を変えたいときはここをいじる

#__file__:実行中のスクリプトの場所を取得、abspathを指定しているから絶対パスで帰ってくる
database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'rireki.db')
#DBAPI接続を確立するPoolオブジェクトを作成
engine = create_engine('sqlite:///' + database_file, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    #初期化対象のテーブル定義指定
    import models.models
    #テーブル作成
    Base.metadata.create_all(bind=engine)