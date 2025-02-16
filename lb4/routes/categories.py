from fastapi import APIRouter, Query

from ..dependencies import JwtAuthUserDepN
from ..models import Category
from ..schemas.categories import CategoryResponse, SearchCategoriesQuery, CategoryCreateRequest
from ..schemas.common import PaginationResponse
from ..utils.multiple_errors_exception import MultipleErrorsException

router = APIRouter(prefix="/categories")


@router.get("", response_model=PaginationResponse[CategoryResponse])
async def search_categories(query: SearchCategoriesQuery = Query()):
    query.page -= 1

    db_query_params = {}
    if query.name:
        db_query_params["name__icontains"] = query.name

    db_query = Category.filter(**db_query_params)
    count = await db_query.count()
    categories = await db_query.order_by("id").offset(query.page * query.page_size).limit(query.page_size)

    return {
        "count": count,
        "result": [
            category.to_json()
            for category in categories
        ],
    }


@router.post("", response_model=CategoryResponse, dependencies=[JwtAuthUserDepN])
async def create_category(data: CategoryCreateRequest):
    if await Category.filter(name=data.name).exists():
        raise MultipleErrorsException("Category with this name already exists!")

    category = await Category.create(name=data.name)
    return category.to_json()