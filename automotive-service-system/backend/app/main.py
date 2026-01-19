from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import customers, vehicles, services, appointments

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router)
app.include_router(vehicles.router)
app.include_router(services.router)
app.include_router(appointments.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Automotive Service Management System API"}