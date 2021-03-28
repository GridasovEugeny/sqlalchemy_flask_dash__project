from sqlalchemy import create_engine, func, and_, or_, join
from sqlalchemy.orm import sessionmaker
import pandas as pd
from database.DBModel import Contract, Order, OrderPosition
# Create connection object
connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}"
connection_string = connection_string.format("postgres", "Q!w2E#r4", "localhost", "5432", "MicrochipDeviceProduction")
engine = create_engine(connection_string, echo=True)
Session = sessionmaker()
session = Session(bind=engine)
# DBModel.Base.metadata.create_all(engine)


contract_table_columns_names = Contract.__table__.columns.keys()
order_table_columns_names = Order.__table__.columns.keys()
orderpos_table_columns_names = OrderPosition.__table__.columns.keys()


def select_contract_table() -> list(tuple()):
    tmp_q = session.query(Contract.contract_num,
                          Contract.contract_date,
                          Contract.status,
                          Contract.manufacturer,
                          )

    return tmp_q.all()


def select_order_table(target_contract_num: str) -> list(tuple()):
    if target_contract_num is not None:
        tmp_q = session.query(Order.order_num,
                              Order.contract_num,
                              Order.status) \
            .filter(Order.contract_num == target_contract_num)
    else:
        tmp_q = session.query(Order.contract_num, Order.order_num, Order.status)
    return tmp_q.all()


def select_orderpos_table(target_order_num: str) -> list(tuple()):
    if target_order_num is not None:
        tmp_q = session.query(OrderPosition.id,
                              OrderPosition.contract_num,
                              OrderPosition.order_num,
                              OrderPosition.device_type_id,
                              OrderPosition.count)\
            .filter(OrderPosition.order_num == target_order_num)
    else:
        tmp_q = session.query(OrderPosition.id,
                              OrderPosition.contract_num,
                              OrderPosition.order_num,
                              OrderPosition.device_type_id,
                              OrderPosition.count)
    return tmp_q.all()


def select_homepage_analytic() -> pd.DataFrame:
    tmp_filter = and_(or_(Contract.status == 'Accepted', Contract.status == 'Processed'),
                      or_(Order.status == 'Accepted', Order.status == 'Processed'))
    tmp_join = join(join(Contract, Order), OrderPosition)
    tmp_q = session.query(Contract.contract_num,
                          Contract.contract_date,
                          Contract.manufacturer,
                          Contract.status,
                          func.sum(OrderPosition.count)).\
        select_from(tmp_join).\
        group_by(Contract.contract_num).\
        filter(tmp_filter)

    tmp_df = pd.DataFrame(tmp_q.all())
    tmp_df.columns = ['contract_num', 'contract_date', 'manufacturer', 'status', 'count']
    return tmp_df
