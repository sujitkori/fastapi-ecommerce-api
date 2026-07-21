from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.routers import auth_router, user_router, category_router, product_router, cart_item_router, order_router, payment_router, review_router, product_image_router
from app.exceptions.handlers import (
    http_exception_handler,
    global_exception_handler,
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(product_router)
app.include_router(cart_item_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(review_router)
app.include_router(product_image_router)

app.mount(              # This is to load the image in Browser (StaticFiles)
    "/media",
    StaticFiles(directory="media"),
    name="media"
)

@app.get("/")
def Home():
    return {
        "message":"FastAPI E-Commerce"
    }