from pydantic import BaseModel, field_validator


class ReviewUserModel(BaseModel):
    id: int
    first_name: str
    last_name: str


class ReviewResponse(BaseModel):
    id: int
    user: ReviewUserModel
    product_id: int
    rating: float
    text: str
    created_at: int


class ReviewCreateRequest(BaseModel):
    rating: float
    text: str

    @field_validator("rating")
    def validate_page(cls, value: float) -> float:
        if value < 1:
            return 1
        if value > 5:
            return 5
        return value


class ReviewEditRequest(BaseModel):
    rating: float | None = None
    text: str | None = None

    @field_validator("rating")
    def validate_page(cls, value: float | None) -> float | None:
        if value is None:
            return value
        if value < 1:
            return 1
        if value > 5:
            return 5
        return value

