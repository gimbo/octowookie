from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.

class Company(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Companies"
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=200)
    phone1 = models.CharField(max_length=100, blank=True, null=True)
    phone2 = models.CharField(max_length=100, blank=True, null=True)
    email1 = models.EmailField(max_length=1000, blank=True, null=True)
    email2 = models.EmailField(max_length=1000, blank=True, null=True)
    url1 = models.URLField(max_length=2000, blank=True, null=True)
    url2 = models.URLField(max_length=2000, blank=True, null=True)
    notes = models.CharField(max_length=10000, blank=True, null=True)

class Person(models.Model):
    class Meta:
        ordering = ['surname', 'forename']
        verbose_name_plural = "People"
    def __unicode__(self):
        return self.name()
    def name(self):
        return '{0} {1}'.format(self.forename, self.surname)
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

class Opportunity(models.Model):
    class Meta:
        ordering = ['when', 'title']
        verbose_name_plural = "Opportunities"
    def __unicode__(self):
        return self.title
    offered_by = models.ManyToManyField(Company, blank=True, null=True)
    managed_by = models.ManyToManyField(Person, blank=True, null=True)
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=2000, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    when = models.DateTimeField()
    notes = models.CharField(max_length=10000, blank=True, null=True)

class Conversation(models.Model):
    class Meta:
        ordering = ['when', 'regards']
    def __unicode__(self):
        people = ' and '.join([str(person) for person in self.involves.all()])
        return "{0} at {1:%H:%M on %A %d %B %Y}".format(people, self.when)
    involves = models.ManyToManyField(Person)
    regards = models.ForeignKey(Opportunity, blank=True, null=True)
    when = models.DateTimeField()
    notes = models.CharField(max_length=10000, blank=True, null=True)
