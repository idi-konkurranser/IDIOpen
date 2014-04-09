# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CompilerProfile.flags'
        db.delete_column(u'execution_compilerprofile', 'flags')

        # Adding field 'CompilerProfile.name'
        db.add_column(u'execution_compilerprofile', 'name',
                      self.gf('django.db.models.fields.CharField')(default='name', max_length=100),
                      keep_default=False)

        # Adding field 'CompilerProfile.compiler_flags'
        db.add_column(u'execution_compilerprofile', 'compiler_flags',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CompilerProfile.run_cmd'
        db.add_column(u'execution_compilerprofile', 'run_cmd',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10),
                      keep_default=False)

        # Adding field 'CompilerProfile.run_flags'
        db.add_column(u'execution_compilerprofile', 'run_flags',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)


        # Changing field 'CompilerProfile.compiler_name_cmd'
        db.alter_column(u'execution_compilerprofile', 'compiler_name_cmd', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'Problem.date_uploaded'
        db.alter_column(u'execution_problem', 'date_uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):
        # Adding field 'CompilerProfile.flags'
        db.add_column(u'execution_compilerprofile', 'flags',
                      self.gf('django.db.models.fields.CharField')(default='name', max_length=100),
                      keep_default=False)

        # Deleting field 'CompilerProfile.name'
        db.delete_column(u'execution_compilerprofile', 'name')

        # Deleting field 'CompilerProfile.compiler_flags'
        db.delete_column(u'execution_compilerprofile', 'compiler_flags')

        # Deleting field 'CompilerProfile.run_cmd'
        db.delete_column(u'execution_compilerprofile', 'run_cmd')

        # Deleting field 'CompilerProfile.run_flags'
        db.delete_column(u'execution_compilerprofile', 'run_flags')


        # Changing field 'CompilerProfile.compiler_name_cmd'
        db.alter_column(u'execution_compilerprofile', 'compiler_name_cmd', self.gf('django.db.models.fields.CharField')(default='', max_length=10))

        # Changing field 'Problem.date_uploaded'
        db.alter_column(u'execution_problem', 'date_uploaded', self.gf('django.db.models.fields.DateTimeField')())

    models = {
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'contest.contactinformation': {
            'Meta': {'object_name': 'ContactInformation'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'contest.contest': {
            'Meta': {'object_name': 'Contest'},
            'contact_infos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contest.ContactInformation']", 'null': 'True', 'symmetrical': 'False'}),
            'css': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('sortedm2m.fields.SortedManyToManyField', [], {'to': u"orm['contest.Link']", 'symmetrical': 'False'}),
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contest.Sponsor']", 'symmetrical': 'False', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'teamreg_end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'contest.link': {
            'Meta': {'object_name': 'Link'},
            'contestUrl': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'separator': ('django.db.models.fields.BooleanField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contest.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Logo'", 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'execution.compilerprofile': {
            'Meta': {'object_name': 'CompilerProfile'},
            'compiler_flags': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'compiler_name_cmd': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'extensions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['execution.FileExtension']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'run_cmd': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'run_flags': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'execution.fileextension': {
            'Meta': {'object_name': 'FileExtension'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'execution.problem': {
            'Meta': {'object_name': 'Problem'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userregistration.CustomUser']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contest.Contest']"}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'textFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'execution.testcase': {
            'Meta': {'object_name': 'TestCase'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userregistration.CustomUser']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inputDescription': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'inputFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'outputDescription': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'outputFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['execution.Problem']"}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'userregistration.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'email_activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '1'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skill_level': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '4'}),
            'temp_email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['execution']