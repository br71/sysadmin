from sqlalchemy import MetaData, Table, Column, Integer, String, Date, Time,create_engine
from sqlalchemy_utils import IPAddressType

#SQL Alchemy Core
metadata = MetaData()

logtable=Table('logtable', metadata,
          Column('ldate', Date()),
          Column('ltime', Time()),
          Column('s_ip', IPAddressType()),
          Column('cs_method', String(2000)),
          Column('cs_uri_stem', String(2000)),
          Column('cs_uri_query', String(2000)),
          Column('s_port', Integer()),
          Column('cs_username', String(2000)),
          Column('c_ip', IPAddressType()),
          Column('cs_user_agent', String(2000)),
          Column('cs_referer', String(2000)),
          Column('sc_status', Integer()),
          Column('sc_substatus', Integer()),
          Column('sc_win32_status', Integer()),
          Column('time_takens', Integer()),
          Column('realclientips', String(2000)),
)

#Previously DB drivers must be installed
engine = create_engine('postgresql+psycopg2://user1:pass1@hostname/dbnam')
#engine = create_engine('mssql+pyodbc://user1:pass1@hostname:1433/dbname?driver=SQL Server')
#engine = create_engine('mysql+mysqldb://user1:pass1@hostname/dbnam')

#Creating table and columns. Database must be created before that.
#This script have to be excecuted first time, during schema creation.
#Script: G_iisLogDbInsert_SqlAlchemy.py use this cript as model.
#Both scripts must be in same directory.
metadata.create_all(engine)

