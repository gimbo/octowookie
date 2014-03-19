from django.db import models
from django.contrib import admin


class Company(models.Model):

    name = models.CharField(max_length=200)
    phone1 = models.CharField(max_length=100, blank=True, null=True)
    phone2 = models.CharField(max_length=100, blank=True, null=True)
    email1 = models.EmailField(max_length=1000, blank=True, null=True)
    email2 = models.EmailField(max_length=1000, blank=True, null=True)
    url1 = models.URLField(max_length=2000, blank=True, null=True)
    url2 = models.URLField(max_length=2000, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Companies"

    def __unicode__(self):
        return self.name

    def phones(self):
        return [p.strip() for p in [self.phone1, self.phone2] if p.strip()]

    def emails(self):
        return [e.strip() for e in [self.email1, self.email2] if e.strip()]

    def urls(self):
        return [u.strip() for u in [self.url1, self.url2] if u.strip()]

    def employees(self):
        return self.person_set.all()

    def offerings(self):
        return self.opportunity_set.all()


class CompanyAdmin(admin.ModelAdmin):

    def phones_str(self, obj):
        return ', '.join(obj.phones())
    phones_str.short_description = 'phone numbers'

    def emails_str(self, obj):
        return ', '.join(obj.emails())
    emails_str.short_description = 'email addresses'

    def urls_str(self, obj):
        return ', '.join(obj.urls())
    urls_str.short_description = 'URLs'

    def employees_str(self, obj):
        return ' and '.join([str(p) for p in obj.employees()])
    employees_str.short_description = 'employees'

    def offerings_str(self, obj):
        return ' and '.join([str(o) for o in obj.offerings()])
    offerings_str.short_description = 'offerings'

    fieldsets = [
        (None,     {'fields': ['name']}),
        ('Phones', {'fields': [('phone1', 'phone2')]}),
        ('Emails', {'fields': [('email1', 'email2')]}),
        ('URLs',   {'fields': [('url1', 'url2')]}),
        (None,     {'fields': ['notes']}),
        ]

    list_display = ('name', 'phones_str', 'emails_str', 'urls_str',
                    'employees_str', 'offerings_str')


class Person(models.Model):

    worksat = models.ManyToManyField(Company)
    forename = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone1 = models.CharField(max_length=100, blank=True, null=True)
    phone2 = models.CharField(max_length=100, blank=True, null=True)
    email1 = models.EmailField(max_length=1000, blank=True, null=True)
    email2 = models.EmailField(max_length=1000, blank=True, null=True)
    url1 = models.URLField(max_length=2000, blank=True, null=True)
    url2 = models.URLField(max_length=2000, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('surname', 'forename')
        verbose_name_plural = "People"

    def __unicode__(self):
        return self.name()

    def name(self):
        return '{0} {1}'.format(self.forename, self.surname)

    def employers(self):
        return self.worksat.all()

    def phones(self):
        return [p.strip() for p in [self.phone1, self.phone2] if p.strip()]

    def emails(self):
        return [e.strip() for e in [self.email1, self.email2] if e.strip()]

    def opportunities(self):
        return self.opportunity_set.all()

    def live_opportunities(self):
        return [o for o in self.opportunities()
                if o.status not in (Opportunity.WONTAPPLY, Opportunity.REJECTED)]


class PersonAdmin(admin.ModelAdmin):

    def employers_str(self, obj):
        return ', '.join([str(employer) for employer in obj.employers()])
    employers_str.short_description = 'employers'

    def phones_str(self, obj):
        return ', '.join(obj.phones())
    phones_str.short_description = 'phone numbers'

    def emails_str(self, obj):
        return ', '.join(obj.emails())
    emails_str.short_description = 'email addresses'

    def live_opportunities_str(self, obj):
        return '; '.join([str(o) for o in obj.live_opportunities()])
    live_opportunities_str.short_description = 'live opportunities'

    fieldsets = [
        (None,     {'fields': [('forename', 'surname'),
                               'worksat',
                               ]}),
        ('Phones', {'fields': [('phone1', 'phone2')]}),
        ('Emails', {'fields': [('email1', 'email2')]}),
        ('URLs',   {'fields': [('url1', 'url2')]}),
        (None,     {'fields': ['notes']}),
        ]

    list_display = ('name', 'employers_str', 'phones_str', 'emails_str',
                    'live_opportunities_str')


class Opportunity(models.Model):

    PENDING = 'PENDING'
    IN_PROGRESS = 'IN PROGRESS'
    WONTAPPLY = 'WONTAPPLY'
    APPLIED = 'APPLIED'
    REJECTED = 'REJECTED'
    ACCEPTED = 'ACCEPTED'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (APPLIED, 'Applied'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (WONTAPPLY, "Won't Apply"),
        )

    offered_by = models.ManyToManyField(Company, blank=True, null=True)
    managed_by = models.ManyToManyField(Person, blank=True, null=True)
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=2000, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    when = models.DateField()
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=PENDING)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['status', 'when', 'title']
        verbose_name_plural = "Opportunities"

    def __unicode__(self):
        location = self.location.strip()
        if not location:
            location = 'unknown location'
        return "{0} @ {1}".format(self.title, location)


class OpportunityAdmin(admin.ModelAdmin):

    def managed_by_str(self, obj):
        return ' and '.join([str(person) for person in obj.managed_by.all()])
    managed_by_str.short_description = 'managed by'

    fieldsets = [
        (None,     {'fields': [('title', 'url'),
                               ('offered_by', 'managed_by'),
                               'location',
                               'when',
                               'status',
                               'notes'
                               ]}),
        ]

    list_display = ('status', 'when', 'title', 'location', 'managed_by_str')


class Conversation(models.Model):

    involves = models.ManyToManyField(Person)
    regards = models.ManyToManyField(Opportunity, blank=True, null=True)
    when = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['when']

    def __unicode__(self):
        people = ' and '.join([str(person) for person in self.involves.all()])
        return "{0} at {1:%H:%M on %A %d %B %Y}".format(people, self.when)


class ConversationAdmin(admin.ModelAdmin):

    def when_str(self, obj):
        return '{0:%a %d %b %Y at %H:%M}'.format(obj.when)
    when_str.short_description = 'when'

    def involves_str(self, obj):
        return ' and '.join([str(person) for person in obj.involves.all()])
    involves_str.short_description = 'involves'

    def regards_str(self, obj):
        return ' and '.join([str(person) for person in obj.regards.all()])
    regards_str.short_description = 'regards'

    list_display = ('when_str', 'involves_str', 'regards_str')

    fieldsets = [
        (None, {'fields': ['when', 'involves', 'regards', 'notes']})]
