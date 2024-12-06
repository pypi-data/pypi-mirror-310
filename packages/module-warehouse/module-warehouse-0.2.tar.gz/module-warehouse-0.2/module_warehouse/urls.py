from django.urls import path
from .views import WarehouseModulesView

urlpatterns = [
    path('warehouse-modules/', WarehouseModulesView.as_view(), name='warehouse-modules'),
]
