from typing import List

from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str = None
    services: List[str]
    price: int
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)
