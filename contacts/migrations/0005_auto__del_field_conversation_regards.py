# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Conversation.regards'
        db.delete_column(u'contacts_conversation', 'regards_id')

        # Adding M2M table for field regards on 'Conversation'
        m2m_table_name = db.shorten_name(u'contacts_conversation_regards')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conversation', models.ForeignKey(orm[u'contacts.conversation'], null=False)),
            ('opportunity', models.ForeignKey(orm[u'contacts.opportunity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['conversation_id', 'opportunity_id'])


    def backwards(self, orm):
        # Adding field 'Conversation.regards'
        db.add_column(u'contacts_conversation', 'regards',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contacts.Opportunity'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field regards on 'Conversation'
        db.delete_table(db.shorten_name(u'contacts_conversation_regards'))


    models = {
        u'contacts.company': {
            'Meta': {'ordering': "['name']", 'object_name': 'Company'},
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
            'Meta': {'ordering': "['when']", 'object_name': 'Conversation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'involves': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contacts.Person']", 'symmetrical': 'False'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'regards': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['contacts.Opportunity']", 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'contacts.opportunity': {
            'Meta': {'ordering': "['status', 'when', 'title']", 'object_name': 'Opportunity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'managed_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['contacts.Person']", 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'offered_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['contacts.Company']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'contacts.person': {
            'Meta': {'ordering': "['surname', 'forename']", 'object_name': 'Person'},
            'email1': ('django.db.models.fields.EmailField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'email2': ('django.db.models.fields.EmailField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'forename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'phone1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url1': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'url2': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'worksat': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contacts.Company']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['contacts']