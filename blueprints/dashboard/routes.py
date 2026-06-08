import logging
from typing import Any
from apiflask import APIBlueprint

from blueprints.dashboard.schemas import DashboardUnionResponseSchema
from blueprints.dashboard.services import get_all_dashboard

logger = logging.getLogger(__name__)

dashboard_bp = APIBlueprint("dashboard", 
                         __name__,
                         url_prefix='/api/dashboard') 

@dashboard_bp.get("/")
@dashboard_bp.output(DashboardUnionResponseSchema, status_code=200)
# Al usar Any, APIFlask permite cualquier JSON plano de salida sin validar de forma rígida
# @dashboard_bp.output(
#     Any, 
#     status_code=200, 
#     description="Retorna DashboardAdminResponseSchema si el rol es ADMIN, o DashboardEmployeeResponseSchema si es EMPLOYEE."
# )
def get_dashboard():
    dashboard_data =  get_all_dashboard()
    return dashboard_data

