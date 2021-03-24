from ORMLayer import session
from DBModel import Contract, Order, OrderPosition, MicrochipType, DeviceType, Base
from datetime import datetime, date
from random import random, choice, choices, randint
import string

microchip_manufacturer_tags_tuple = ('AC701', 'KC705', 'VC707', 'VC709', 'ML605', 'VC7203', 'ZC702', 'ZC706', 'ML605',
                                     'KC705', 'VC707', 'ZC706', 'Atmel', 'TF', 'C')

device_name_tag1_tuple = ('UD', 'UZ', 'UP', 'US')
device_name_tag2_tuple = ('YAS', 'YUS', 'YAPO', 'YAIN', 'YAGY', 'YAZO', 'YAKIDU')

contract_status_tuple = ('Accepted', 'Denied', 'Fulfilled', 'Processed')
manufacturers_tuple = ('Almaz', 'BPSZ', 'YARZ', 'Elektro_Signal')

order_status_tuple = ('Accepted', 'Denied', 'Fulfilled', 'Processed')

tmp_contracts_list = []
tmp_orders_list = []
tmp_orderpos_list = []
tmp_microchip_types_list = []
tmp_device_types_list = []


def random_date(min_year: int = 2016) -> date:
    start = date(min_year, 1, 1)
    end = datetime.today().date()
    return start + (end - start) * random()


def generate_contract() -> Contract:
    tmp_contract_date = random_date()
    tmp_contract_num = '{}/59.{}/{}'.format(''.join(choices(string.digits, k=25)),
                                            ''.join(choices(string.digits, k=3)),
                                            tmp_contract_date.year)
    tmp_contract_status = choice(contract_status_tuple)
    tmp_manufacturer = choice(manufacturers_tuple)
    return Contract(contract_num=tmp_contract_num,
                    contract_date=tmp_contract_date,
                    status=tmp_contract_status,
                    manufacturer=tmp_manufacturer
                    )


def generate_order(some_contract: Contract) -> Order:
    if isinstance(some_contract, Contract):
        return Order(contract_num=some_contract.contract_num,
                     order_num='{}/{}'.format(''.join(choices(string.digits, k=9)), choice(['100', '200'])),
                     status=choice(contract_status_tuple)
                     )
    else:
        print(f"Instance type is not {type(Contract)}")


def generate_order_position(some_order: Order, some_device_type: DeviceType,
                            some_count: int = randint(1, 4000)) -> OrderPosition:
    if isinstance(some_order, Order) and isinstance(some_device_type, DeviceType):
        return OrderPosition(contract_num=some_order.contract_num,
                             order_num=some_order.order_num,
                             device_type_id=some_device_type.id,
                             count=some_count
                             )
    else:
        print(f"ERROR {type(some_order)} is not {Order} OR"
              f" {type(some_device_type)} is not {DeviceType}")


def generate_microchip_type() -> MicrochipType:
    tmp2 = string.ascii_lowercase.join(choices(string.digits, k=4))
    return MicrochipType(id='{}{}{}'.format(choice(microchip_manufacturer_tags_tuple),
                                            ''.join(choices(string.digits, k=4)),
                                            ''.join(choices(tmp2, k=3))
                                            )
                         )


def generate_device_type(some_microchip_type: MicrochipType) -> DeviceType:
    if isinstance(some_microchip_type, MicrochipType):
        return DeviceType(id='BNYZ.{}'.format(''.join(choices(string.digits, k=3))),
                          name='{}{}'.format(choice(device_name_tag1_tuple),
                                             choice(device_name_tag2_tuple)),
                          microchip_type_id=some_microchip_type.id
                          )
    else:
        print(f"ERROR {some_microchip_type} is not {type(MicrochipType)}")


def orm_object_print(object_inst: Base):
    if isinstance(object_inst, Base):
        # Это нужно определить в базовом классе как свойство __repr__ что бы выводить простым print
        print([object_inst.__getattribute__(attr_name) for attr_name in object_inst.__table__.columns.keys()])
    else:
        print("ERROR wrong instance type")


def populate_db() -> None:
    # Создаем случайные типы микросхем и типы устройств
    for _ in range(22):
        tmp_microchip_types_list.append(generate_microchip_type())
    for _ in range(30):
        tmp_device_types_list.append(generate_device_type(choice(tmp_microchip_types_list)))
    # Создаем контракты и заказы
    for _ in range(20):
        tmp_contracts_list.append(generate_contract())
    for _ in range(50):
        tmp_orders_list.append(generate_order(choice(tmp_contracts_list)))
    # Создаем позиции для заказов
    for _ in range(len(tmp_orders_list)):
        target_order = choice(tmp_orders_list)
        for _2 in range(randint(1, 15)):
            tmp_orderpos_list.append(generate_order_position(target_order, choice(tmp_device_types_list),
                                                             randint(1, 4000))
                                     )
    session.add_all(tmp_contracts_list)
    session.commit()
    session.add_all(tmp_orders_list)
    session.commit()
    session.add_all(tmp_microchip_types_list)
    session.commit()
    session.add_all(tmp_device_types_list)
    session.commit()
    session.add_all(tmp_orderpos_list)
    session.commit()

#populate_db()


