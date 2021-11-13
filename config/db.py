from sqlalchemy import create_engine, MetaData


engine = create_engine("mysql+pymysql://root:restapi@localhost:3307/storedb")

meta = MetaData()
conn = engine.connect()
