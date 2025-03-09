from typing import Annotated

from fastapi.params import Header, Depends

from .models import Session, User, Product, Order
from .utils.multiple_errors_exception import MultipleErrorsException


async def jwt_auth_session(
        authorization: str | None = Header(default=None),
        x_token: str | None = Header(default=None),
) -> Session:
    authorization = authorization or x_token
    if not authorization or (session := await Session.from_jwt(authorization)) is None:
        raise MultipleErrorsException("Invalid session.", 401)

    return session


async def jwt_auth_user(session: Session = Depends(jwt_auth_session)) -> User:
    return session.user


JwtAuthUserDepN = Depends(jwt_auth_user)
JwtAuthUserDep = Annotated[User, JwtAuthUserDepN]


async def product_dep(product_id: int) -> Product:
    if (product := await Product.get_or_none(id=product_id)) is None:
        raise MultipleErrorsException("Unknown product.", 404)

    return product


ProductDep = Annotated[Product, Depends(product_dep)]


async def order_dep(order_id: int, user: JwtAuthUserDep) -> Order:
    if (order := await Order.get_or_none(id=order_id, user=user)) is None:
        raise MultipleErrorsException("Unknown order.", 404)

    return order


OrderDep = Annotated[Order, Depends(order_dep)]
