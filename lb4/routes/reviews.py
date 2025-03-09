from fastapi import APIRouter, Query

from ..dependencies import JwtAuthUserDepN, JwtAuthUserDep, ProductDep
from ..models import Order, Review
from ..schemas.common import PaginationResponse, PaginationQuery
from ..schemas.reviews import ReviewResponse, ReviewCreateRequest
from ..utils.multiple_errors_exception import MultipleErrorsException

router = APIRouter(prefix="/reviews")


@router.get("/{product_id}", response_model=PaginationResponse[ReviewResponse], dependencies=[JwtAuthUserDepN])
async def get_product_reviews(product: ProductDep, query: PaginationQuery = Query()):
    query.page -= 1

    db_query = Review.filter(product=product).select_related("user")
    count = await db_query.count()
    reviews = await db_query.order_by("-id").offset(query.page * query.page_size).limit(query.page_size)

    return {
        "count": count,
        "result": [
            await review.to_json()
            for review in reviews
        ],
    }


@router.post("/{product_id}", response_model=ReviewResponse)
async def create_review(product: ProductDep, user: JwtAuthUserDep, data: ReviewCreateRequest):
    if not await Order.filter(user=user, products=product).exists():
        raise MultipleErrorsException("You need to order this product first!", 400)
    if await Review.filter(user=user, product=product).exists():
        raise MultipleErrorsException("You already have reviewed this product!", 400)

    review = await Review.create(
        user=user,
        product=product,
        rating=data.rating,
        text=data.text,
    )

    return await review.to_json()


@router.patch("/{product_id}", response_model=ReviewResponse)
async def edit_review(product: ProductDep, user: JwtAuthUserDep, data: ReviewCreateRequest):
    review = await Review.get_or_none(user=user, product=product).select_related("user")
    if review is None:
        raise MultipleErrorsException("Unknown review.", 404)

    to_update = data.model_dump()
    if not to_update:
        return await review.to_json()

    await review.update_from_dict(to_update).save(update_fields=list(to_update.keys()))
    return await review.to_json()


@router.delete("/{product_id}", status_code=204)
async def delete_review(product: ProductDep, user: JwtAuthUserDep, data: ReviewCreateRequest):
    review = await Review.get_or_none(user=user, product=product).select_related("user")
    if review is None:
        raise MultipleErrorsException("Unknown review.", 404)

    await review.delete()
