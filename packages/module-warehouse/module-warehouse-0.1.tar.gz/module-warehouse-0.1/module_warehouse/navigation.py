from netbox.plugins import PluginMenuItem

# Definice menu položky
menu_items = (
    PluginMenuItem(
        link='plugins:module_warehouse:warehouse-modules',  # Namespace pluginu + název view
        link_text='Sklad modulů',  # Text odkazu
        permissions=['dcim.view_device'],  # Potřebná oprávnění
    ),
)
