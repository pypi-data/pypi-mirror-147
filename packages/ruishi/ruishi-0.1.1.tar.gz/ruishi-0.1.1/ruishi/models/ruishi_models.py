from pydantic import BaseModel, validator

from uuid import UUID
from typing import Optional


class RuishiUser(BaseModel):
    username: str
    password: str
    token: Optional[str]
    useruuid: Optional[UUID]

    @validator('useruuid', pre=True, always=True)
    def check(cls, v, values):
        if v and values['token']:
            return v
        elif v or values['token']:
            raise ValueError('token和useruuid必须都传或者都不传')
        else:
            return v
