from typing import List
from pydantic import BaseModel

class IPList(BaseModel):
    ips: List[str]
