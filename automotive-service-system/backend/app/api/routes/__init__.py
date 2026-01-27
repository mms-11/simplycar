from fastapi import APIRouter

from . import appointments, customers, services, vehicles

router = APIRouter(prefix="/api")

router.include_router(customers.router, prefix="/customers", tags=["customers"])
router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
router.include_router(services.router, prefix="/services", tags=["services"])
router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
