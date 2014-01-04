# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Restaurant.street_address'
        db.delete_column('restaurant_restaurant', 'street_address')

        # Adding field 'Restaurant.address'
        db.add_column('restaurant_restaurant', 'address',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Restaurant.street_address'
        db.add_column('restaurant_restaurant', 'street_address',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True),
                      keep_default=False)

        # Deleting field 'Restaurant.address'
        db.delete_column('restaurant_restaurant', 'address')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'restaurant.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'restaurant.comment': {
            'Meta': {'object_name': 'Comment'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Post']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.UserProfile']"})
        },
        'restaurant.drink': {
            'Meta': {'object_name': 'Drink'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Restaurant']"})
        },
        'restaurant.employee': {
            'Meta': {'object_name': 'Employee'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resturant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Restaurant']"}),
            'salary': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'restaurant.feay': {
            'Meta': {'object_name': 'Feay'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'restaurant.food': {
            'Meta': {'object_name': 'Food'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Restaurant']"})
        },
        'restaurant.food_ingredient': {
            'Ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Ingredient']"}),
            'Meta': {'object_name': 'Food_ingredient'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Food']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'restaurant.friendinvitation': {
            'Meta': {'object_name': 'FriendInvitation'},
            'approve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiverFI'", 'to': "orm['restaurant.UserProfile']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'senderFI'", 'to': "orm['restaurant.UserProfile']"})
        },
        'restaurant.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Restaurant']"})
        },
        'restaurant.message': {
            'Meta': {'object_name': 'Message'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiverM'", 'to': "orm['restaurant.UserProfile']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'senderM'", 'to': "orm['restaurant.UserProfile']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'restaurant.msgnotification': {
            'Meta': {'object_name': 'MsgNotification'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'senderMN'", 'to': "orm['restaurant.UserProfile']"}),
            'unread_num': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'restaurant.myfriend': {
            'Meta': {'unique_together': "[('user', 'friend')]", 'object_name': 'MyFriend'},
            'friend': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friendMF'", 'to': "orm['restaurant.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userMF'", 'to': "orm['restaurant.UserProfile']"})
        },
        'restaurant.order': {
            'Meta': {'object_name': 'Order'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'finish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Table']"})
        },
        'restaurant.order_drink': {
            'Meta': {'object_name': 'Order_drink'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'drink': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Drink']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Order']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '16'})
        },
        'restaurant.order_food': {
            'Meta': {'object_name': 'Order_food'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Food']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Order']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '16'})
        },
        'restaurant.page': {
            'Meta': {'object_name': 'Page'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'views': ('django.db.models.fields.IntegerField', [], {})
        },
        'restaurant.post': {
            'Meta': {'object_name': 'Post'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.UserProfile']"})
        },
        'restaurant.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'table_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'telephone': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.UserProfile']"}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'})
        },
        'restaurant.table': {
            'Meta': {'object_name': 'Table'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Restaurant']"})
        },
        'restaurant.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['restaurant']