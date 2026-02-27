from fastapi import APIRouter

from . import appointments, customers, services, vehicles, users, session, company, payments

router = APIRouter(prefix="/api")

router.include_router(customers.router, prefix="/customers", tags=["customers"])
router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
router.include_router(services.router, prefix="/services", tags=["services"])
router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(session.router, prefix="/session", tags=["session"])
router.include_router(company.router, prefix="/companies", tags=["companies"])
router.include_router(payments.router, prefix="/payments", tags=["payments"])
