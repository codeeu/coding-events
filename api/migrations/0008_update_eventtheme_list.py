# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """
        Update default topics list
        """
        update_theme_title_list = [
            ("Native mobile app development", "Mobile app development"),
            ("Other software development", "Software development"),
            ("Other (see description)", "Other")
        ]

        new_theme_list = [
            "Unplugged activities",
            "Playful coding activities",
            "Art and creativity",
            "Visual/Block programming",
            "Game design",
            "Internet of things and wearable computing",
            "3D printing",
            "Augmented reality",
            "Motivation and awareness raising",
            "Promoting diversity",
        ]

        theme_order_list = [
            ("Hardware", 0),
            ("Robotics", 1),
            ("Data manipulation and visualisation", 2),
            ("Mobile app development", 3),
            ("Web development", 4),
            ("Basic programming concepts", 5),
            ("Unplugged activities", 6),
            ("Playful coding activities", 7),
            ("Art and creativity", 8),
            ("Visual/Block programming", 9),
            ("Software development", 10),
            ("Game design", 11),
            ("Internet of things and wearable computing", 12),
            ("3D printing", 13),
            ("Augmented reality", 14),
            ("Motivation and awareness raising", 15),
            ("Promoting diversity", 16),
            ("Other", 17),
        ]

        for theme in update_theme_title_list:
            # Throw exception, if theme name does not exists
            existing_theme = orm['api.EventTheme'].objects.get(name=theme[0])
            existing_theme.name = theme[1]
            existing_theme.save()

        for theme in new_theme_list:
            new_theme = orm['api.EventTheme'].objects.create(name=theme)
            new_theme.save()

        for theme in theme_order_list:
            # Throw exception, if theme name does not exists
            existing_theme = orm['api.EventTheme'].objects.get(name=theme[0])
            existing_theme.order = theme[1]
            existing_theme.save()

    def backwards(self, orm):
        pass

    models = {
        'api.event': {
            'Meta': {'ordering': "['start_date']", 'object_name': 'Event'},
            'audience': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'event_audience'", 'symmetrical': 'False', 'to': "orm['api.EventAudience']"}),
            'contact_person': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'geoposition': ('geoposition.fields.GeopositionField', [], {'default': "'0,0'", 'max_length': '42'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'organizer': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 8, 0, 0)'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '50'}),
            'theme': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'event_theme'", 'symmetrical': 'False', 'to': "orm['api.EventTheme']"}),
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'api.eventaudience': {
            'Meta': {'object_name': 'EventAudience'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'api.eventtheme': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'EventTheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'api.socialaccountlist': {
            'Meta': {'object_name': 'SocialAccountList'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'api.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']
    symmetrical = True
