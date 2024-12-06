from django.shortcuts import render
from django.views import View
from dcim.models import Device, Module

class WarehouseModulesView(View):
    template_name = 'module_warehouse/warehouse_modules.html'

    def get(self, request, *args, **kwargs):
        # Find the device named "Sklad"
        warehouse_device = Device.objects.filter(name="Sklad").first()

        if warehouse_device:
            # Filter all modules associated with this device
            modules = Module.objects.filter(device=warehouse_device).order_by('module_type')

            context = {
                'warehouse_exists': True,
                'modules': modules
            }
        else:
            # If no warehouse device exists
            context = {
                'warehouse_exists': False
            }

        return render(request, self.template_name, context)
