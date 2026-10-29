from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.customers import router as customers_router
from app.api.v1.vehicles import router as vehicles_router
from app.core.database import Base, engine
from app.models.customer import Customer  # noqa: F401 - registers table metadata
from app.models.vehicle import Vehicle  # noqa: F401 - registers table metadata

app = FastAPI(title='Car & Bike Garage Management System', version='1.0.0')


@app.on_event('startup')
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={'detail': 'Invalid request data', 'errors': exc.errors()})


@app.exception_handler(SQLAlchemyError)
async def database_error(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={'detail': 'Database operation failed'})


@app.get('/health', tags=['Health'])
def health():
    return {'status': 'ok'}


app.include_router(customers_router, prefix='/api/v1')

app.include_router(vehicles_router, prefix='/api/v1')
