# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Word'
        db.create_table(u'bay_word', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'bay', ['Word'])


    def backwards(self, orm):
        # Deleting model 'Word'
        db.delete_table(u'bay_word')


    models = {
        u'bay.file': {
            'Meta': {'object_name': 'File'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'torrent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bay.Torrent']"}),
            'wanted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'bay.torrent': {
            'Meta': {'object_name': 'Torrent'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infohash': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'leechers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'seeders': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'uploader': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'bay.word': {
            'Meta': {'object_name': 'Word'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['bay']