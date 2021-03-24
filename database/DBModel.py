from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, DATE, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

Base = declarative_base()


# Абстрактные классы , шаблоны таблиц
class SimplyIdentified:
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)


class Printable:
    pass


# Таблицы типов и вспомогательные таблицы
class MicrochipType(Base, Printable):
    __tablename__ = 'microchip_type'
    id = Column(VARCHAR(255), nullable=False, unique=True, primary_key=True)


class DeviceType(Base, Printable):
    __tablename__ = 'device_type'
    id = Column(VARCHAR(255), nullable=False, unique=True, primary_key=True)
    name = Column(VARCHAR(255), nullable=True)
    microchip_type_id = Column(VARCHAR(255), ForeignKey('microchip_type.id', ondelete='CASCADE'),
                               nullable=False, index=True)


# Таблицы основных сущностей
class Contract(Base, Printable):
    __tablename__ = 'contract'
    contract_num = Column(VARCHAR(255), nullable=False, unique=True, primary_key=True)
    contract_date = Column(DATE, nullable=True)
    status = Column(VARCHAR(255), nullable=True)
    manufacturer = Column(VARCHAR(255), nullable=True)


class Order(Base, Printable):
    __tablename__ = 'order'
    contract_num = Column(VARCHAR(255), ForeignKey('contract.contract_num', ondelete='CASCADE'),
                          nullable=False)
    order_num = Column(VARCHAR(255), nullable=False)
    status = Column(VARCHAR(255), nullable=True)
    __table_args__ = (PrimaryKeyConstraint(contract_num, order_num), {})


class OrderPosition(Base, SimplyIdentified, Printable):
    __tablename__ = 'order_position'
    contract_num = Column(VARCHAR(255), nullable=False)
    order_num = Column(VARCHAR(255), nullable=False)
    device_type_id = Column(VARCHAR(255), ForeignKey('device_type.id', ondelete='CASCADE'), nullable=False)
    count = Column(Integer, nullable=False)
    __table_args__ = (ForeignKeyConstraint([contract_num, order_num],
                                           [Order.contract_num, Order.order_num]),
                      {})


class Bill(Base, SimplyIdentified, Printable):
    __tablename__ = 'bill'
    contract_num = Column(VARCHAR(255), ForeignKey('contract.contract_num', ondelete='CASCADE'), nullable=False,
                          index=True)
    bill_num = Column(VARCHAR(255), nullable=False)
    bill_date = Column(DATE, nullable=False)
    receiving_date = Column(DATE, nullable=False)


class BillPosition(Base, SimplyIdentified, Printable):
    __tablename__ = 'bill_position'
    bill_id = Column(Integer, ForeignKey('bill.id', ondelete='CASCADE'), nullable=False, index=True)
    microchip_type_id = Column(VARCHAR(255), ForeignKey('microchip_type.id', ondelete='CASCADE'), nullable=False,
                               index=True)
    count = Column(Integer, nullable=False)


class Shipment(Base, SimplyIdentified, Printable):
    __tablename__ = 'shipment'
    contract_num = Column(VARCHAR(255), nullable=False, index=True)
    order_num = Column(VARCHAR(255), nullable=False, index=True)
    planing_date = Column(DATE, nullable=True)
    actual_date = Column(DATE, nullable=True)
    status = Column(VARCHAR(255), nullable=False)
    __table_args__ = (ForeignKeyConstraint([contract_num, order_num],
                                           [Order.contract_num, Order.order_num]),
                      {})


class ShipmentPosition(Base, SimplyIdentified, Printable):
    __tablename__ = 'shipment_position'
    shipment_id = Column(Integer, ForeignKey('shipment.id', ondelete='CASCADE'), nullable=False, index=True)
    order_position_id = Column(Integer, ForeignKey('order_position.id', ondelete='CASCADE'), nullable=False, index=True)
    count = Column(Integer, nullable=False)
    technical_deviation_letter = Column(Boolean, nullable=True)


# Должна быть автоматическая проверка совпадения ожидаемого типа устройства у назначенной отгрузки
# и фактического типа устройства которое запрограммированно
class Warehouse(Base, SimplyIdentified, Printable):
    __tablename__ = 'warehouse'
    bill_position_id = Column(Integer, ForeignKey('bill_position.id', ondelete='CASCADE'), nullable=True, index=True)
    shipment_position_id = Column(Integer, ForeignKey('shipment_position.id', ondelete='CASCADE'), nullable=True,
                                  index=True)
    actual_device_type_id = Column(VARCHAR(255), ForeignKey('device_type.id', ondelete='CASCADE'), nullable=True,
                                   index=True)
    count = Column(Integer, nullable=False)
    container_mark = Column(VARCHAR(8), nullable=True)
    package_mark = Column(VARCHAR(8), nullable=False, unique=True)
    microchip_marking = Column(VARCHAR(255))
    technical_deviation_status = Column(Boolean, nullable=True)
