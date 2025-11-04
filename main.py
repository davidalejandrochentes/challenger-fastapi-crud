from fastapi import FastAPI
from starlette.status import HTTP_200_OK
from starlette.staticfiles import StaticFiles
from sqlalchemy import event, orm
from sqlalchemy.orm import Session
from models.mixins.db_mixin import SoftDeleteMixin

app = FastAPI()

@event.listens_for(Session, "do_orm_execute")
def _add_filtering_criteria(execute_state):
    """
    Intercept all ORM queries and add a filtering criterion for all SELECT statements
    to exclude entities that have been soft-deleted.
    """
    if (
        execute_state.is_select
        and not execute_state.is_column_select
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )

@app.get("/", status_code=HTTP_200_OK)
async def root():
    return "API is running"