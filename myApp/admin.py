from django.contrib import admin
from myApp.models import customer,agricultureBasics,agricultureSchemes,subscribers,products,orders,feedback,applications,cart,grassCutters

# Register your models here.
admin.site.register(customer)
admin.site.register(agricultureBasics)
admin.site.register(agricultureSchemes)
admin.site.register(subscribers)
admin.site.register(products)
admin.site.register(orders)
admin.site.register(feedback)
admin.site.register(applications)
admin.site.register(cart)
admin.site.register(grassCutters)
