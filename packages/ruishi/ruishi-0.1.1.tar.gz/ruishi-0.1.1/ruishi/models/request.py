from pydantic import BaseModel, Field, validator

import time
from typing import List, Optional, Any, Iterable
from uuid import UUID, uuid4
from datetime import datetime

import ruishi


class Request(BaseModel):
    version: str = ruishi.api_version
    productSign: str = ruishi.api_product
    appSign: str = ruishi.__name__
    requestId: UUID = Field(default_factory=uuid4)
    applyTime: datetime = Field(default_factory=lambda: int(round(time.time() * 1000)))

    @staticmethod
    def format_dict(func):
        def convert(data: Any):
            if type(data) == str:
                return data
            elif type(data) == UUID:
                return data.hex
            elif isinstance(data, Iterable):
                data_type = type(data)
                if data_type == tuple:
                    new_tuple = []
                    for i in data:
                        new_tuple.append(convert(i))
                    return tuple(new_tuple)
                elif data_type == list:
                    new_list = []
                    for i in data:
                        new_list.append(convert(i))
                    return new_list
                elif data_type == dict:
                    new_dict = {}
                    for i, v in data.items():
                        new_dict.update({i: convert(v)})
                    return new_dict
                else:
                    print(data)
                    raise ValueError('不知道什么类型')
            else:
                return data

        def inner(*args, **kwargs):
            data = func(*args, **kwargs)
            return convert(data)

        return inner

    @format_dict
    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs)


class LoginRequest(Request):
    account: str
    password: str


class RoomListRequest(Request):
    pass


class DeviceListRequest(Request):
    nodeUuids: List[UUID]


class DeviceControlRequest(Request):
    timestamp: datetime = Field(default_factory=lambda: datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
    useruuid: Optional[UUID]
    transactionNo: Optional[str]
    deviceCode: UUID

    class Config:
        fields = {'timestamp': {'exclude': True},
                  'useruuid': {'exclude': True}}

    @validator('transactionNo', pre=True, always=True)
    def transactionno_verify(cls, v, values):
        if values['useruuid'] and v:
            raise ValueError('useruuid和transactionNo只能传一个')
        if v:
            if len(v) != 50 or v[0:1] != 'a':
                raise ValueError('transactionNo的格式是 a+时间戳+user的uuid')
            s = v[1:18]
            if f'{s}000' != datetime.strptime(s, '%Y%m%d%H%M%S%f').strftime("%Y%m%d%H%M%S%f"):
                raise ValueError('transactionNo的格式是 a+时间戳+user的uuid')
            s = v[18:50]
            if UUID(s).version != 4:
                raise ValueError('transactionNo的格式是 a+时间戳+user的uuid')
            return v
        elif values['useruuid']:
            return f"a{values['timestamp']}{str(values['useruuid']).replace('-', '')}"
        else:
            raise ValueError('useruuid和transactionNo必须传一个')


if __name__ == '__main__':
    a = RoomListRequest()
    print(a.dict())
