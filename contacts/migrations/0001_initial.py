# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'contacts_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('phone1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('phone2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email1', self.gf('django.db.models.fields.EmailField')(max_length=1000, null=True, blank=True)),
            ('email2', self.gf('django.db.models.fields.EmailField')(max_length=1000, null=True, blank=True)),
            ('url1', self.gf('django.db.models.fields.URLField')(max_length=2000, null=True, blank=True)),
            ('url2', self.gf('django.db.models.fields.URLField')(max_length=2000, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=10000, null=True, blank=True)),
        ))
        db.send_create_signal(u'contacts', ['Company'])

        # Adding model 'Person'
        db.create_table(u'contacts_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('phone1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('phone2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email1', self.gf('django.db.models.fields.EmailField')(max_length=1000, null=True, blank=True)),
            ('email2', self.gf('django.db.models.fields.EmailField')(max_length=1000, null=True, blank=True)),
            ('url1', self.gf('django.db.models.fields.URLField')(max_length=2000, null=True, blank=True)),
            ('url2', self.gf('django.db.models.fields.URLField')(max_length=2000, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=10000, null=True, blank=True)),
        ))
        db.send_create_signal(u'contacts', ['Person'])

        # Adding M2M table for field worksat on 'Person'
        m2m_table_name = db.shorten_name(u'contacts_person_worksat')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'contacts.person'], null=False)),
            ('company', models.ForeignKey(orm[u'contacts.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'company_id'])

        # Adding model 'Opportunity'
        db.create_table(u'contacts_opportunity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=2000, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=10000, null=True, blank=True)),
        ))
        db.send_create_signal(u'contacts', ['Opportunity'])

        # Adding M2M table for field offered_by on 'Opportunity'
        m2m_table_name = db.shorten_name(u'contacts_opportunity_offered_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('opportunity', models.ForeignKey(orm[u'contacts.opportunity'], null=False)),
            ('company', models.ForeignKey(orm[u'contacts.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['opportunity_id', 'company_id'])

        # Adding M2M table for field managed_by on 'Opportunity'
        m2m_table_name = db.shorten_name(u'contacts_opportunity_managed_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('opportunity', models.ForeignKey(orm[u'contacts.opportunity'], null=False)),
            ('person', models.ForeignKey(orm[u'contacts.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['opportunity_id', 'person_id'])

        # Adding model 'Conversation'
        db.create_table(u'contacts_conversation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=10000, null=True, blank=True)),
        ))
        db.send_create_signal(u'contacts', ['Conversation'])

        # Adding M2M table for field involves on 'Conversation'
        m2m_table_name = db.shorten_name(u'contacts_conversation_involves')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conversation', models.ForeignKey(orm[u'contacts.conversation'], null=False)),
            ('person', models.ForeignKey(orm[u'contacts.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['conversation_id', 'person_id'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table(u'contacts_company')

        # Deleting model 'Person'
        db.delete_table(u'contacts_person')

        # Removing M2M table for field worksat on 'Person'
        db.delete_table(db.shorten_name(u'contacts_person_worksat'))

        # Deleting model 'Opportunity'
        db.delete_table(u'contacts_opportunity')

        # Removing M2M table for field offered_by on 'Opportunity'
        db.delete_table(db.shorten_name(u'contacts_opportunity_offered_by'))

        # Removing M2M table for field managed_by on 'Opportunity'
        db.delete_table(db.shorten_name(u'contacts_opportunity_managed_by'))

        # Deleting model 'Conversation'
        db.delete_table(u'contacts_conversation')

        # Removing M2M table for field involves on 'Conversation'
        db.delete_table(db.shorten_name(u'contacts_conversation_involves'))


    models = {
        u'contacts.company': {
            'Meta': {'object_name': 'Company'},
            'email1': ('django.db.models.fields.EmailField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'email2': ('django.db.models.fields.EmailField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'phone1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url1': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'url2': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'})
        },
        u'contacts.conversation': {
            'Meta': {'object_name': 'Conversation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'involves': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contacts.Person']", 'symmetrical': 'False'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'contacts.opportunity': {
            'Meta': {'object_name': 'Opportunity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'managed_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contacts.Person']", 'symmetrical': 'False'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'offered_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contacts.Company']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'contacts.person': {
            'Meta': {'object_name': 'Person'},
            'email1': ('django.db.models.fields.EmailField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'email2': ('django.db.models.fields.EmailField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'phone1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url1': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'url2': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'worksat': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contacts.Company']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['contacts']