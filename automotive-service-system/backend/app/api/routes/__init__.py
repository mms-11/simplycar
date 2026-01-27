from fastapi import APIRouter

from . import appointments, customers, materials, services, stock_flow, supplier, vehicles, workers

router = APIRouter(prefix="/api")

router.include_router(customers.router, prefix="/customers", tags=["customers"])
router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
router.include_router(services.router, prefix="/services", tags=["services"])
router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
router.include_router(supplier.router, prefix="/suppliers", tags=["suppliers"])
router.include_router(stock_flow.router, prefix="/stock-flows", tags=["stock-flows"])
router.include_router(materials.router, prefix="/materials", tags=["materials"])
router.include_router(workers.router, prefix="/workers", tags=["workers"])
