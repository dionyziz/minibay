# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Torrent'
        db.create_table(u'bay_torrent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('seeders', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('leechers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('uploaded', self.gf('django.db.models.fields.DateTimeField')()),
            ('uploader', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('magnet', self.gf('django.db.models.fields.CharField')(max_length=2048)),
        ))
        db.send_create_signal(u'bay', ['Torrent'])

        # Adding model 'File'
        db.create_table(u'bay_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('torrent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bay.Torrent'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'bay', ['File'])


    def backwards(self, orm):
        # Deleting model 'Torrent'
        db.delete_table(u'bay_torrent')

        # Deleting model 'File'
        db.delete_table(u'bay_file')


    models = {
        u'bay.file': {
            'Meta': {'object_name': 'File'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'torrent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bay.Torrent']"})
        },
        u'bay.torrent': {
            'Meta': {'object_name': 'Torrent'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leechers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'magnet': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'seeders': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'uploader': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['bay']