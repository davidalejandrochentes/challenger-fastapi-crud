import time
from fastapi import FastAPI, Request
from starlette.status import HTTP_200_OK
from sqlalchemy import event, orm
from sqlalchemy.orm import Session
from models.mixins.db_mixin import SoftDeleteMixin
from routers import auth, users
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url} | Process Time: {process_time:.4f}s")
    return response

@event.listens_for(Session, "do_orm_execute")
def _add_filtering_criteria(execute_state):
    if (
        execute_state.is_select
        and not execute_state.is_column_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/", status_code=HTTP_200_OK)
async def root():
    return "API is running"