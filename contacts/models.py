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

    forename = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    worksat = models.ManyToManyField(Company, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
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
                               ('worksat', 'location'),
                               ]}),
        ('Phones', {'fields': [('phone1', 'phone2')]}),
        ('Emails', {'fields': [('email1', 'email2')]}),
        ('URLs',   {'fields': [('url1', 'url2')]}),
        (None,     {'fields': ['notes']}),
        ]

    list_display = ('name', 'employers_str', 'location', 'phones_str',
                    'emails_str', 'live_opportunities_str')


class Opportunity(models.Model):

    NEW = '00 NEW'
    PENDING = '10 PENDING'
    IN_PROGRESS = '20 IN PROGRESS'
    IN_PROGRESS_AWAITING_CALLBACK = '22 INP WAIT CALLBACK'
    IN_PROGRESS_NEED_TO_CHASE = '22 INP CHASE'
    APPLIED_RECRUITER = '50 APPLIED RECRUITER'
    APPLIED_EMPLOYER = '55 APPLIED EMPLOYER'
    ACCEPTED = '60 ACCEPTED'
    REJECTED = '80 REJECTED'
    WONTAPPLY = '90 WONTAPPLY'
    STATUS_CHOICES = (
        (NEW, 'New'),
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (IN_PROGRESS_AWAITING_CALLBACK, 'In Progress, awaiting callback'),
        (IN_PROGRESS_NEED_TO_CHASE, 'In Progress, need to chase'),
        (APPLIED_RECRUITER, 'Applied, waiting on recruiter'),
        (APPLIED_EMPLOYER, 'Applied, waiting on employer'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (WONTAPPLY, "Won't Apply"),
        )

    STATUS_CLOSED = (
        ACCEPTED,
        REJECTED,
        WONTAPPLY,
        )
    STATUS_NOT_ONGOING = (NEW, ) + STATUS_CLOSED
    STATUS_ONGOING = tuple(
        [x for (x, y) in STATUS_CHOICES if x not in STATUS_NOT_ONGOING])

    offered_by = models.ManyToManyField(Company, blank=True, null=True)
    managed_by = models.ManyToManyField(Person, blank=True, null=True)
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=2000, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    when = models.DateField()
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=NEW)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['status', 'when', 'title']
        verbose_name_plural = "Opportunities"

    def __unicode__(self):
        location = self.location.strip()
        if not location:
            location = 'unknown location'
        return "{0} @ {1}".format(self.title, location)

    @property
    def is_new(self):
        return self.status == Opportunity.NEW

    @property
    def is_ongoing(self):
        return self.status in Opportunity.STATUS_ONGOING

    @property
    def is_closed(self):
        return self.status in Opportunity.STATUS_CLOSED

    def wontapply(self):
        self.status = Opportunity.WONTAPPLY
        self.save()


class OpportunityFilterStatus(admin.SimpleListFilter):

    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('new', 'New'),
            (None, 'Ongoing'),
            ('closed', 'Closed'),
            ('all', 'All')
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == None:
            # Only show ongoing opportunities by default.
            return queryset.filter(status__in=Opportunity.STATUS_ONGOING)
        elif self.value() == 'new':
            # Show only new opportunities if requested.
            return queryset.filter(status__in=[Opportunity.NEW])
        elif self.value() == 'closed':
            # Show only closed opportunities if requested.
            return queryset.filter(status__in=Opportunity.STATUS_CLOSED)
        else:
            # Fallthrough: include whole set.
            return queryset


class OpportunityAdmin(admin.ModelAdmin):

    def offered_by_str(self, obj):
        return ' and '.join([str(person) for person in obj.offered_by.all()])
    offered_by_str.short_description = 'offered by'

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

    list_display = ('status', 'when', 'title', 'location', 'offered_by_str',
                    'managed_by_str')
    list_display_links = ('title',)
    list_filter = (OpportunityFilterStatus,)


class Conversation(models.Model):

    OPEN = '10 OPEN'
    WAITING = '20 WAITING'
    ACTION_NEEDED = '30 ACTION NEEDED'
    CLOSED = '50 CLOSED'
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (WAITING, 'Waiting'),
        (ACTION_NEEDED, 'Action Needed'),
        (CLOSED, 'Closed'),
        )

    involves = models.ManyToManyField(Person)
    regards = models.ManyToManyField(Opportunity, blank=True, null=True)
    when = models.DateTimeField()
    medium = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=OPEN)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['status', 'when']

    def __unicode__(self):
        people = ' and '.join([str(person) for person in self.involves.all()])
        return "{0}, {1} at {2:%H:%M on %A %d %B %Y}".format(people,
                                                             self.medium,
                                                             self.when)


class ConversationFilterOpenness(admin.SimpleListFilter):

    title = 'openness'
    parameter_name = 'openness'

    def lookups(self, request, model_admin):
        return (
            (None, 'Open'),
            ('closed', 'Closed'),
            ('all', 'All')
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == None:
            # Exclude closed conversations by default.
            return queryset.exclude(status__exact=Conversation.CLOSED)
        elif self.value() == 'closed':
            # Show only closed conversations if requested.
            return queryset.filter(status__exact=Conversation.CLOSED)
        else:
            # Fallthrough: include whole set.
            return queryset


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

    list_display = ('when_str', 'status', 'medium', 'involves_str',
                    'regards_str')

    list_filter = (ConversationFilterOpenness,)

    fieldsets = [
        (None, {'fields': [('when', 'medium', 'status'),
                           'involves', 'regards', 'notes']})]
