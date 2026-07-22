from django.contrib import admin
from .models import Customer, PhoneNumber, Address, Document

admin.site.register(Customer)
admin.site.register(PhoneNumber)
admin.site.register(Address)
admin.site.register(Document)