from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.

class Company(models.Model):
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
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    worksat = models.ManyToManyField(Company)
    name = models.CharField(max_length=200)
    phone1 = models.CharField(max_length=100, blank=True, null=True)
    phone2 = models.CharField(max_length=100, blank=True, null=True)
    email1 = models.EmailField(max_length=1000, blank=True, null=True)
    email2 = models.EmailField(max_length=1000, blank=True, null=True)
    url1 = models.URLField(max_length=2000, blank=True, null=True)
    url2 = models.URLField(max_length=2000, blank=True, null=True)
    notes = models.CharField(max_length=10000, blank=True, null=True)

class Opportunity(models.Model):
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
    def __unicode__(self):
        return unicode(self.when)
    involves = models.ManyToManyField(Person)
    regards = models.ForeignKey(Opportunity, blank=True, null=True)
    when = models.DateTimeField()
    notes = models.CharField(max_length=10000, blank=True, null=True)
