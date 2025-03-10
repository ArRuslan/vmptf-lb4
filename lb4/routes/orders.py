from fastapi import APIRouter, Query

from ..dependencies import JwtAuthUserDepN, JwtAuthUserDep
from ..models import Order, Product
from ..schemas.common import PaginationResponse, PaginationQuery
from ..schemas.orders import OrderResponse, OrderCreateRequest
from ..utils.multiple_errors_exception import MultipleErrorsException

router = APIRouter(prefix="/orders")


@router.get("", response_model=PaginationResponse[OrderResponse])
async def get_orders(user: JwtAuthUserDep, query: PaginationQuery = Query()):
    query.page -= 1

    db_query = Order.filter(user=user)
    count = await db_query.count()
    orders = await db_query.order_by("id").offset(query.page * query.page_size).limit(query.page_size)

    return {
        "count": count,
        "result": [
            await order.to_json()
            for order in orders
        ],
    }


@router.post("", response_model=OrderResponse, dependencies=[JwtAuthUserDepN])
async def create_order(user: JwtAuthUserDep, data: OrderCreateRequest):
    products = await Product.filter(id__in=data.product_ids).select_related("category")
    if not products or len(products) != len(data.product_ids):
        raise MultipleErrorsException("Unknown product!", 404)

    order = await Order.create(user=user)
    await order.products.add(*products)

    return await order.to_json(products)