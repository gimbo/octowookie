from django.contrib import admin
from contacts.models import (Company, CompanyAdmin, Person, PersonAdmin,
                             Opportunity, OpportunityAdmin, Conversation,
                             ConversationAdmin)

# Register your models here.

admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Opportunity, OpportunityAdmin)
