from netbox.plugins import PluginConfig
from django.urls import path, include

class ModuleWarehouseConfig(PluginConfig):
    name = 'module_warehouse'
    verbose_name = 'Module warehouse'
    description = 'Plugin which displays modules that are currently stored in warehouse.'
    version = '1.0.0'
    author = 'Viktor Kubec'
    author_email = 'Viktor.Kubec@gmail.com'
    base_url = 'module-warehouse'
    required_settings = []
    default_settings = {}

config = ModuleWarehouseConfig
