from uuid import UUID

from db.models import OrderModel
from di import provide_orders_repo
from litestar import Controller, delete, get, post
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.plugins.sqlalchemy import filters
from pydantic import TypeAdapter
from repositories import OrderRepository
from schemas import Order, OrderCreate


class OrderController(Controller):
    """Order CRUD"""

    dependencies = {"orders_repo": Provide(provide_orders_repo)}
    tags = ["Orders"]

    @get(path="/orders")
    async def list_orders(
        self,
        orders_repo: OrderRepository,
        limit_offset: filters.LimitOffset,
    ) -> OffsetPagination[Order]:
        results, total = await orders_repo.list_and_count(limit_offset)
        type_adapter = TypeAdapter(list[Order])
        return OffsetPagination[Order](
            items=type_adapter.validate_python(results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post(path="/orders")
    async def create_order(
        self,
        orders_repo: OrderRepository,
        data: OrderCreate,
    ) -> Order:
        obj = await orders_repo.add(
            OrderModel(**data.model_dump(exclude_unset=True, exclude_none=True)),
        )
        await orders_repo.session.commit()
        return Order.model_validate(obj)

    @delete(path="/orders/{order_id:uuid}")
    async def delete_order(
        self,
        orders_repo: OrderRepository,
        order_id: UUID,
    ) -> None:
        _ = await orders_repo.delete(order_id)
        await orders_repo.session.commit()
