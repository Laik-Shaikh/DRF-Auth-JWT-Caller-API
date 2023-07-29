from django.contrib import admin
from . models import RegisterUser, ContactList, SpamNumber

# Register your models here.
admin.site.register(RegisterUser)
admin.site.register(ContactList)
admin.site.register(SpamNumber)
