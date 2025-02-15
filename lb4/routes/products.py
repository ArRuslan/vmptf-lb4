from fastapi import APIRouter, Query

from ..models import Category, Product
from ..schemas.common import PaginationResponse
from ..schemas.products import ProductResponse, ProductCreateRequest, SearchProductsQuery
from ..utils.multiple_errors_exception import MultipleErrorsException

router = APIRouter(prefix="/products")


@router.get("", response_model=PaginationResponse[ProductResponse])
async def search_products(query: SearchProductsQuery = Query()):
    query.page -= 1

    db_query_params = {}
    if query.name:
        db_query_params["name__icontains"] = query.name
    if query.category_id:
        db_query_params["category__id"] = query.category_id
    if query.price_min:
        db_query_params["price__gte"] = query.price_min
    if query.price_max:
        db_query_params["price__lte"] = query.price_max

    db_query = Product.filter(**db_query_params)
    count = await db_query.count()
    products = await db_query.order_by("id").select_related("category")\
        .offset(query.page * query.page_size).limit(query.page_size)

    return {
        "count": count,
        "result": [
            product.to_json()
            for product in products
        ],
    }


# TODO: add jwt auth
@router.post("", response_model=ProductResponse)
async def create_product(data: ProductCreateRequest):
    if (category := await Category.get_or_none(id=data.category_id)) is None:
        raise MultipleErrorsException("Category with this name does not exist!")

    product = await Product.create(name=data.name, description=data.description, price=data.price, caegory=category)
    return product.to_json()
