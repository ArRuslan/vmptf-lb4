from pydantic import EmailStr, BaseModel


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    token: str
    expires_at: int


class LoginResponse(RegisterResponse):
    ...