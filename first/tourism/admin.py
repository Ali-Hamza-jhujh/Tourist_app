from django.contrib import admin
from tourism.models import Register,TouristSpot,Text,City,Hotel,Booking,Payment
# Register your models here.
admin.site.register(Register)
admin.site.register(Text)
admin.site.register(TouristSpot)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Booking)
admin.site.register(Payment)