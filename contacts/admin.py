from django.contrib import admin
from contacts.models import (Company, Person, Opportunity, Conversation)

# Register your models here.

admin.site.register(Company)
admin.site.register(Person)
admin.site.register(Conversation)
admin.site.register(Opportunity)
