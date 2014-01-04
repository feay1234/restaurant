# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('restaurant_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('restaurant', ['UserProfile'])

        # Adding model 'Feay'
        db.create_table('restaurant_feay', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('restaurant', ['Feay'])

        # Adding model 'Message'
        db.create_table('restaurant_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='senderM', to=orm['restaurant.UserProfile'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiverM', to=orm['restaurant.UserProfile'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('restaurant', ['Message'])

        # Adding model 'MsgNotification'
        db.create_table('restaurant_msgnotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='senderMN', to=orm['restaurant.UserProfile'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('unread_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('restaurant', ['MsgNotification'])

        # Adding model 'Post'
        db.create_table('restaurant_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.UserProfile'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('likes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('notification', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('restaurant', ['Post'])

        # Adding model 'MyFriend'
        db.create_table('restaurant_myfriend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='userMF', to=orm['restaurant.UserProfile'])),
            ('friend', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friendMF', to=orm['restaurant.UserProfile'])),
        ))
        db.send_create_signal('restaurant', ['MyFriend'])

        # Adding unique constraint on 'MyFriend', fields ['user', 'friend']
        db.create_unique('restaurant_myfriend', ['user_id', 'friend_id'])

        # Adding model 'FriendInvitation'
        db.create_table('restaurant_friendinvitation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='senderFI', to=orm['restaurant.UserProfile'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiverFI', to=orm['restaurant.UserProfile'])),
            ('approve', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notification', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('restaurant', ['FriendInvitation'])

        # Adding model 'Comment'
        db.create_table('restaurant_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.UserProfile'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Post'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('likes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('notification', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('restaurant', ['Comment'])

        # Adding model 'Restaurant'
        db.create_table('restaurant_restaurant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('telephone', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('table_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('likes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('restaurant', ['Restaurant'])

        # Adding model 'Table'
        db.create_table('restaurant_table', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Restaurant'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('restaurant', ['Table'])

        # Adding model 'Food'
        db.create_table('restaurant_food', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Restaurant'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('likes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('restaurant', ['Food'])

        # Adding model 'Ingredient'
        db.create_table('restaurant_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Restaurant'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('restaurant', ['Ingredient'])

        # Adding model 'Food_ingredient'
        db.create_table('restaurant_food_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Food'])),
            ('Ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Ingredient'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('restaurant', ['Food_ingredient'])

        # Adding model 'Drink'
        db.create_table('restaurant_drink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Restaurant'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('likes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('restaurant', ['Drink'])

        # Adding model 'Order'
        db.create_table('restaurant_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Table'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('pay', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('finish', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('restaurant', ['Order'])

        # Adding model 'Order_food'
        db.create_table('restaurant_order_food', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Order'])),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Food'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=16)),
        ))
        db.send_create_signal('restaurant', ['Order_food'])

        # Adding model 'Order_drink'
        db.create_table('restaurant_order_drink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Order'])),
            ('drink', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Drink'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=16)),
        ))
        db.send_create_signal('restaurant', ['Order_drink'])

        # Adding model 'Employee'
        db.create_table('restaurant_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resturant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Restaurant'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('salary', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('restaurant', ['Employee'])

        # Adding model 'Category'
        db.create_table('restaurant_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('likes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('restaurant', ['Category'])

        # Adding model 'Page'
        db.create_table('restaurant_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['restaurant.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('views', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('restaurant', ['Page'])


    def backwards(self, orm):
        # Removing unique constraint on 'MyFriend', fields ['user', 'friend']
        db.delete_unique('restaurant_myfriend', ['user_id', 'friend_id'])

        # Deleting model 'UserProfile'
        db.delete_table('restaurant_userprofile')

        # Deleting model 'Feay'
        db.delete_table('restaurant_feay')

        # Deleting model 'Message'
        db.delete_table('restaurant_message')

        # Deleting model 'MsgNotification'
        db.delete_table('restaurant_msgnotification')

        # Deleting model 'Post'
        db.delete_table('restaurant_post')

        # Deleting model 'MyFriend'
        db.delete_table('restaurant_myfriend')

        # Deleting model 'FriendInvitation'
        db.delete_table('restaurant_friendinvitation')

        # Deleting model 'Comment'
        db.delete_table('restaurant_comment')

        # Deleting model 'Restaurant'
        db.delete_table('restaurant_restaurant')

        # Deleting model 'Table'
        db.delete_table('restaurant_table')

        # Deleting model 'Food'
        db.delete_table('restaurant_food')

        # Deleting model 'Ingredient'
        db.delete_table('restaurant_ingredient')

        # Deleting model 'Food_ingredient'
        db.delete_table('restaurant_food_ingredient')

        # Deleting model 'Drink'
        db.delete_table('restaurant_drink')

        # Deleting model 'Order'
        db.delete_table('restaurant_order')

        # Deleting model 'Order_food'
        db.delete_table('restaurant_order_food')

        # Deleting model 'Order_drink'
        db.delete_table('restaurant_order_drink')

        # Deleting model 'Employee'
        db.delete_table('restaurant_employee')

        # Deleting model 'Category'
        db.delete_table('restaurant_category')

        # Deleting model 'Page'
        db.delete_table('restaurant_page')


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
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'table_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'telephone': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
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