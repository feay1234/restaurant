# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Order_food.table'
        db.add_column('restaurant_order_food', 'table',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['restaurant.Table']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Order_food.table'
        db.delete_column('restaurant_order_food', 'table_id')


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
        'restaurant.businesspost': {
            'Meta': {'object_name': 'BusinessPost'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Restaurant']"}),
            'comment_num': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['restaurant.Comment']", 'symmetrical': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'share': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.UserProfile']"}),
            'who_like': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'Plike'", 'symmetrical': 'False', 'to': "orm['restaurant.UserProfile']"})
        },
        'restaurant.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'restaurant.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment_num': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['restaurant.CommentOfComment']", 'symmetrical': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.UserProfile']"}),
            'who_like': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'Clike'", 'symmetrical': 'False', 'to': "orm['restaurant.UserProfile']"})
        },
        'restaurant.commentofcomment': {
            'Meta': {'object_name': 'CommentOfComment'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.UserProfile']"}),
            'who_like': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'CClike'", 'symmetrical': 'False', 'to': "orm['restaurant.UserProfile']"})
        },
        'restaurant.drink': {
            'Meta': {'object_name': 'Drink'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'foods': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['restaurant.Order_food']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Restaurant']"}),
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
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '16'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Table']"})
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
            'like': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.UserProfile']"})
        },
        'restaurant.product': {
            'Meta': {'object_name': 'Product'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.Shop']"})
        },
        'restaurant.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'follow': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'opening': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'table_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'telephone': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.UserProfile']"}),
            'visiting': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'visitor': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'})
        },
        'restaurant.shop': {
            'Meta': {'object_name': 'Shop'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['restaurant.UserProfile']"})
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