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
    notes = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Companies"

    def __unicode__(self):
        return self.name

    def phones(self):
        return [p.strip() for p in [self.phone1, self.phone2] if p.strip()]

    def phones_str(self):
        return ', '.join(self.phones())

    def emails(self):
        return [e.strip() for e in [self.email1, self.email2] if e.strip()]

    def emails_str(self):
        return ', '.join(self.emails())

    def employees(self):
        return self.person_set.all()

    def offerings(self):
        return self.opportunity_set.all()


class CompanyAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,     {'fields': ['name']}),
        ('Phones', {'fields': [('phone1', 'phone2')]}),
        ('Emails', {'fields': [('email1', 'email2')]}),
        ('URLs',   {'fields': [('url1', 'url2')]}),
        (None,     {'fields': ['notes']}),
        ]

    list_display = ('name', 'phones_str', 'emails_str', 'employees',
                    'offerings')


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
    notes = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        ordering = ('surname', 'forename')
        verbose_name_plural = "People"

    def __unicode__(self):
        return self.name()

    def name(self):
        return '{0} {1}'.format(self.forename, self.surname)

    def employers(self):
        return self.worksat.all()

    def employers_string(self):
        return ', '.join([str(employer) for employer in self.employers()])

    def phones(self):
        return [p.strip() for p in [self.phone1, self.phone2] if p.strip()]

    def phones_str(self):
        return ', '.join(self.phones())

    def emails(self):
        return [e.strip() for e in [self.email1, self.email2] if e.strip()]

    def emails_str(self):
        return ', '.join(self.emails())


class PersonAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,     {'fields': [('forename', 'surname'),
                               'worksat',
                               ]}),
        ('Phones', {'fields': [('phone1', 'phone2')]}),
        ('Emails', {'fields': [('email1', 'email2')]}),
        ('URLs',   {'fields': [('url1', 'url2')]}),
        (None,     {'fields': ['notes']}),
        ]

    list_display = ('name', 'employers_string', 'phones_str', 'emails_str')


class Opportunity(models.Model):

    PENDING = 'PENDING'
    WONTAPPLY = 'WONTAPPLY'
    APPLIED = 'APPLIED'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPLIED, 'Applied'),
        (REJECTED, 'Rejected'),
        (WONTAPPLY, "Won't Apply"),
        )

    offered_by = models.ManyToManyField(Company, blank=True, null=True)
    managed_by = models.ManyToManyField(Person, blank=True, null=True)
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=2000, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    when = models.DateTimeField()
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=PENDING)
    notes = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        ordering = ['status', 'when', 'title']
        verbose_name_plural = "Opportunities"

    def __unicode__(self):
        location = self.location.strip()
        if not location:
            location = 'unknown location'
        return "{0} (at {1})".format(self.title, location)

    def managed_by_str(self):
        return ' and '.join([str(person) for person in self.managed_by.all()])


class OpportunityAdmin(admin.ModelAdmin):

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
    notes = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        ordering = ['when']

    def __unicode__(self):
        people = ' and '.join([str(person) for person in self.involves.all()])
        return "{0} at {1:%H:%M on %A %d %B %Y}".format(people, self.when)

    def involves_str(self):
        return ' and '.join([str(person) for person in self.involves.all()])

    def regards_str(self):
        return ' and '.join([str(person) for person in self.regards.all()])

    def when_str(self):
        return '{0:%a %d %b %Y at %H:%M}'.format(self.when)


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('when_str', 'involves_str', 'regards_str')
