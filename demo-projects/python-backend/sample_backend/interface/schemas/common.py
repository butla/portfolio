from pydantic import BaseModel, NonNegativeInt


class PaginationParams(BaseModel):
    offset: NonNegativeInt = 0
    limit: NonNegativeInt = 20
