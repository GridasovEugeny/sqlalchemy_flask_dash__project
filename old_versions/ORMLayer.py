from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from database import DBModel

# Create connection object
connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}"
connection_string = connection_string.format("postgres", "Q!w2E#r4", "localhost", "5432", "MicrochipDeviceProduction")
engine = create_engine(connection_string, echo=True)
Session = sessionmaker()
session = Session(bind=engine)
# DBModel.Base.metadata.create_all(engine)


contract_table_columns_names = DBModel.Contract.__table__.columns.keys()
order_table_columns_names = DBModel.Order.__table__.columns.keys()
orderpos_table_columns_names = DBModel.OrderPosition.__table__.columns.keys()

contract_table_df = pd.DataFrame(columns=contract_table_columns_names)
# Если результат запроса будет пустой то произойдет ошибка при присвоении имен стобцов
def get_contract_table_df():
    tmp_q = session.query(DBModel.Contract.contract_num,
                          DBModel.Contract.contract_date,
                          DBModel.Contract.status,
                          DBModel.Contract.manufacturer,
                          )
    tmp_df = pd.DataFrame(tmp_q.all())
    tmp_df.columns = [description_dict["name"] for description_dict in tmp_q.column_descriptions]

    return tmp_df


def get_order_table_df(target_contract_num):
    if target_contract_num is not None:
        tmp_q = session.query(DBModel.Order.order_num,
                              DBModel.Order.contract_num,
                              DBModel.Order.status) \
            .filter(DBModel.Order.contract_num == target_contract_num)
        tmp_df = pd.DataFrame(tmp_q.all())
        tmp_df.columns = [description_dict["name"] for description_dict in tmp_q.column_descriptions]

    else:
        tmp_q = session.query(DBModel.Order.contract_num, DBModel.Order.order_num, DBModel.Order.status)
        tmp_df = pd.DataFrame(tmp_q.all())
        tmp_df.columns = [description_dict["name"] for description_dict in tmp_q.column_descriptions]
    return tmp_df


def get_orderpos_table_df(target_order_num):
    if target_order_num is not None:
        tmp_q = session.query(DBModel.OrderPosition.id,
                              DBModel.OrderPosition.contract_num,
                              DBModel.OrderPosition.order_num,
                              DBModel.OrderPosition.device_type_id,
                              DBModel.OrderPosition.count)\
            .filter(DBModel.OrderPosition.order_num == target_order_num)
        tmp_df = pd.DataFrame(tmp_q.all())
        tmp_df.columns = [description_dict["name"] for description_dict in tmp_q.column_descriptions]

    else:
        tmp_q = session.query(DBModel.OrderPosition.id,
                              DBModel.OrderPosition.contract_num,
                              DBModel.OrderPosition.order_num,
                              DBModel.OrderPosition.device_type_id,
                              DBModel.OrderPosition.count)
        tmp_df = pd.DataFrame(tmp_q.all())
        tmp_df.columns = [description_dict["name"] for description_dict in tmp_q.column_descriptions]
    return tmp_df
