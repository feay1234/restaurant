from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q
from django.db.models import Count

# to do, Notification, feed, message, friend,
#change myFriend to friend 
# decide whether delete

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    picture = models.ImageField(upload_to='imgs', blank=True)
    datetime = models.DateTimeField(default=datetime.now, editable=False)
    def __unicode__(self):
            return self.user.username
    def natural_key(self):
		return (self.name)
    def get_instant_message(self, sender):
    	return Message.objects.filter(receiver = self, sender = sender, read=False)
    def get_restaurant(self):
    	return Restaurant.objects.filter(user = self)
    def get_shop(self):
    	return Shop.objects.filter(user = self)
    def find_business(self,name):
    	dict = {}
    	if len(Restaurant.objects.filter(user = self, name = name)) > 0:
    		dict['type'] = "restaurant";
    		dict['business'] = Restaurant.objects.get(user = self, name = name)
    	else:
    		dict['type'] = "shop";
    		dict['business'] = Shop.objects.get(user = self, name = name)
    	return dict
    def to_dict(self):
		dict = {}
		dict['id'] = self.id
		dict['name'] = self.name
		dict['picture'] = self.picture.path.split("/")[-1]
		return dict
    def unnotified_message(self):
    	if len(Message.objects.filter(receiver = self, notify = False)) > 0:
    		return True
    	else:
    		return False
    def get_unread_message(self):
		unnotified_msg = Message.objects.filter(receiver = self, notify = False).values('sender').annotate(msg_count=Count('sender'))
		# Message.objects.filter(receiver = self, notify = False).update(notify = True)
		return unnotified_msg




class Message(models.Model):
	sender = models.ForeignKey(UserProfile,related_name='senderM')
	receiver = models.ForeignKey(UserProfile, related_name='receiverM')
	text = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='imgs', blank=True)
	datetime = models.DateTimeField(default=datetime.now, editable=False)
	read = models.BooleanField(default=False)
	notify = models.BooleanField(default=False)
	def __unicode__(self):
            return self.sender.user.username

class MsgNotification(models.Model):
	sender = models.ForeignKey(UserProfile,related_name='senderMN')
	datetime = models.DateTimeField(default=datetime.now)
	unread_num = models.IntegerField(default=0)
	def __unicode__(self):
		return self.sender.user.username

class CommentOfComment(models.Model):
	user = models.ForeignKey(UserProfile)
	text = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='imgs', blank=True)
	datetime = models.DateTimeField(default=datetime.now)
	like = models.PositiveIntegerField(default=0)
	notification = models.BooleanField(default=False)
	who_like = models.ManyToManyField(UserProfile, related_name="CClike")
	def __unicode__(self):
		return self.text
	def to_dict(self):
		dict = {}
		dict['comment_id'] = self.id
		dict['text'] = self.text
		dict['user_id'] = self.user.id
		dict['name'] = self.user.name
		dict['user_picture'] = self.user.picture.path.split("/")[-1]
		dict['like'] = self.like
		dict['datetime'] = str(self.datetime).split(" ")[1]
		return dict

class Comment(models.Model):
	user = models.ForeignKey(UserProfile)
	title = models.CharField(max_length=128)
	text = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='imgs', blank=True)
	datetime = models.DateTimeField(default=datetime.now)
	like = models.PositiveIntegerField(default=0)
	comment_num = models.PositiveIntegerField(default=0)
	notification = models.BooleanField(default=False)
	comments = models.ManyToManyField(CommentOfComment)
	who_like = models.ManyToManyField(UserProfile, related_name="Clike")
	def __unicode__(self):
		return self.text
	def to_dict(self, userProfile):
		dict = {}
		dict['comment_id'] = self.id
		dict['text'] = self.text
		dict['title'] = self.title
		dict['user_id'] = self.user.id
		dict['name'] = self.user.name
		dict['user_picture'] = self.user.picture.path.split("/")[-1]
		dict['comment_num'] = self.comment_num
		dict['like'] = self.like
		dict['datetime'] = str(self.datetime).split(" ")[1]
		if userProfile in self.who_like.all():
			dict['liked'] = "Unlike"
		else:
			dict['liked'] = "Like"
		return dict


class Restaurant(models.Model):
	user = models.ForeignKey(UserProfile)
	name = models.CharField(max_length=16, unique=True) 
	address = models.CharField(max_length=32, blank=True)
	description = models.CharField(max_length=32)
	city = models.CharField(max_length=32, blank=True)
	zip_code = models.CharField(max_length=8, blank=True)
	country = models.CharField(max_length=32, blank=True)
	telephone = models.IntegerField(blank=True)
	datetime = models.DateTimeField(default=datetime.now, editable=False)
	picture = models.ImageField(upload_to='imgs', blank=True)
	table_number = models.PositiveIntegerField(default=0)
	opening = models.CharField(max_length=32, blank=True)
	like = models.IntegerField(default=0)
	visiting = models.PositiveIntegerField(default=0)
	visitor = models.PositiveIntegerField(default=0)
	follow = models.PositiveIntegerField(default=0)
	follower = models.ManyToManyField(UserProfile, related_name='follower')
	website = models.CharField(max_length=32, blank=True)
	#add many fields website
	
	def __unicode__(self):
		return self.name
	def to_dict(self):
		dict = {}
		dict['name'] = self.name
		dict['description'] = self.description
		dict['id'] = self.id
		dict['address'] = self.address
		dict['city'] = self.city
		dict['country'] = self.country
		dict['zip_code'] = self.zip_code
		dict['telephone'] = self.telephone
		dict['picture'] = self.picture.path.split("/")[-1]
		dict['like'] = self.like
		dict['table_number'] = self.table_number
		dict['datetime'] = str(self.datetime).split(" ")[0]
		return dict
	def get_menu(self):
		return Food.objects.filter(restaurant = self)
	def get_post(self):
		return BusinessPost.objects.filter(business = self).order_by('-datetime')

class RestaurantReview(models.Model):
	user = models.ForeignKey(UserProfile)
	restaurant = models.ForeignKey(Restaurant)
	title = models.CharField(max_length=128)
	text = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='imgs', blank=True)
	datetime = models.DateTimeField(default=datetime.now)
	like = models.PositiveIntegerField(default=0)
	comment_num = models.PositiveIntegerField(default=0)
	notification = models.BooleanField(default=False)
	who_like = models.ManyToManyField(UserProfile, related_name="rr_who_like")
	def __unicode__(self):
		return self.text
	def to_dict(self, userProfile):
		dict = {}
		dict['id'] = self.id
		dict['text'] = self.text
		dict['title'] = self.title
		dict['user_id'] = self.user.id
		dict['name'] = self.user.name
		dict['user_picture'] = self.user.picture.path.split("/")[-1]
		dict['comment_num'] = self.comment_num
		dict['like'] = self.like
		dict['datetime'] = str(self.datetime).split(" ")[1]
		if userProfile in self.who_like.all():
			dict['liked'] = "Unlike"
		else:
			dict['liked'] = "Like"
		return dict

class BusinessPost(models.Model):
	user = models.ForeignKey(UserProfile)
	business = models.ForeignKey(Restaurant)
	text = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='imgs', blank=True)
	datetime = models.DateTimeField(default=datetime.now)
	like = models.PositiveIntegerField(default=0)
	comment_num = models.PositiveIntegerField(default=0)
	share = models.PositiveIntegerField(default=0)
	notification = models.BooleanField(default=False)
	who_like = models.ManyToManyField(UserProfile, related_name="Plike")
	def __unicode__(self):
		return self.business.name
	def get_comment(self):
		return Comment.objects.filter(post = self)
	def to_dict(self):
		dict = {}
		dict['id'] = self.id
		dict['text'] = self.text
		if self.picture:
			dict['picture'] = self.picture.path.split("/")[-1]
		dict['like'] = self.like
		dict['datetime'] = str(self.datetime).split(" ")[0]
		dict['comment_num'] = self.comment_num
		return dict

class BusinessPostComment(models.Model):
	user = models.ForeignKey(UserProfile)
	post = models.ForeignKey(BusinessPost)
	text = models.CharField(max_length=128)
	datetime = models.DateTimeField(default=datetime.now)
	like = models.PositiveIntegerField(default=0)
	notification = models.BooleanField(default=False)
	who_like = models.ManyToManyField(UserProfile, related_name="rrc_who_like")
	def __unicode__(self):
		return self.text
	def to_dict(self, userProfile):
		dict = {}
		dict['id'] = self.id
		dict['text'] = self.text
		dict['user_id'] = self.user.id
		dict['name'] = self.user.name
		dict['user_picture'] = self.user.picture.path.split("/")[-1]
		dict['like'] = self.like
		dict['datetime'] = str(self.datetime).split(" ")[1]
		if userProfile in self.who_like.all():
			dict['liked'] = "Unlike"
		else:
			dict['liked'] = "Like"
		return dict

class Post(models.Model):
	user = models.ForeignKey(UserProfile)
	text = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='imgs', blank=True)
	datetime = models.DateTimeField(default=datetime.now)
	like = models.PositiveIntegerField(default=0)
	notification = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.user.username
	def get_comment(self):
		return Comment.objects.filter(post = self)

class MyFriend(models.Model):
	user = models.ForeignKey(UserProfile, related_name="userMF")
	friend = models.ForeignKey(UserProfile, related_name="friendMF")
	def __unicode__(self):
		return self.user.user.username
	class Meta:
		unique_together = [("user", "friend")]

class FriendInvitation(models.Model):
	sender = models.ForeignKey(UserProfile,related_name='senderFI')
	receiver = models.ForeignKey(UserProfile, related_name='receiverFI')
	approve = models.BooleanField(default=False)
	notification = models.BooleanField(default=False)
	def __unicode__(self):
		return self.sender.user.username







class Shop(models.Model):
	user = models.ForeignKey(UserProfile)
	name = models.CharField(max_length=16, unique=True)
	description = models.CharField(max_length=128)
	telephone = models.IntegerField(blank=True)
	datetime = models.DateTimeField(default=datetime.now, editable=False)
	picture = models.ImageField(upload_to='imgs', blank=True)
	like = models.PositiveIntegerField(default=0)
	
	def __unicode__(self):
		return self.name
	def get_product(self):
		return Product.objects.filter(shop = self)
	def to_dict(self):
		dict = {}
		dict['name'] = self.name
		dict['id'] = self.id
		dict['telephone'] = self.telephone
		dict['picture'] = self.picture.path.split("/")[-1]
		dict['like'] = self.like
		dict['datetime'] = str(self.datetime).split(" ")[0]
		return dict

class Product(models.Model):
	shop = models.ForeignKey(Shop)
	name = models.CharField(max_length=32, unique=True)
	description = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='imgs', blank=True)
	price = models.IntegerField(default=0)
	datetime = models.DateTimeField(default=datetime.now, editable=False)
	like = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.name
	def to_dict(self):
		dict = {}
		dict['id'] = self.id
		dict['name'] = self.name
		dict['description'] = self.description
		dict['price'] = self.price
		dict['picture'] = self.picture.path.split("/")[-1]
		dict['like'] = self.like
		return dict

class Table(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	number = models.IntegerField()
	available = models.BooleanField(default=True)
	def natural_key(self):
		return self.number,
	def __unicode(self):
		return self.number



class Food(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	name = models.CharField(max_length=32)
	description = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='imgs', blank=True)
	price = models.IntegerField(default=0)
	datetime = models.DateTimeField(default=datetime.now, editable=False)
	like = models.PositiveIntegerField(default=0)
	def natural_key(self):
		return (self.name, self.price)
	def __unicode__(self):
		return self.name
	def to_dict(self):
		dict = {}
		dict['id'] = self.id
		dict['name'] = self.name
		dict['description'] = self.description
		dict['price'] = self.price
		dict['picture'] = self.picture.path.split("/")[-1]
		dict['like'] = self.like
		return dict
	
class FoodReview(models.Model):
	user = models.ForeignKey(UserProfile)
	food = models.ForeignKey(Food)
	title = models.CharField(max_length=128)
	text = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='imgs', blank=True)
	datetime = models.DateTimeField(default=datetime.now)
	like = models.PositiveIntegerField(default=0)
	comment_num = models.PositiveIntegerField(default=0)
	notification = models.BooleanField(default=False)
	who_like = models.ManyToManyField(UserProfile, related_name="fr_who_like")
	def __unicode__(self):
		return self.text
	def to_dict(self, userProfile):
		dict = {}
		dict['id'] = self.id
		dict['text'] = self.text
		dict['title'] = self.title
		dict['user_id'] = self.user.id
		dict['name'] = self.user.name
		dict['user_picture'] = self.user.picture.path.split("/")[-1]
		dict['comment_num'] = self.comment_num
		dict['like'] = self.like
		dict['datetime'] = str(self.datetime).split(" ")[1]
		if userProfile in self.who_like.all():
			dict['liked'] = "Unlike"
		else:
			dict['liked'] = "Like"
		return dict



class Ingredient(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	name = models.CharField(max_length=128, unique=True)
	amount = models.PositiveIntegerField(default=0)
	category = models.CharField(max_length=16)
	# alarm when the amount reach at provided amount, peak_amount, unit
	def natural_key(self):
		return self.name,self.amount


	def __unicode__(self):
		return self.name

class Food_ingredient(models.Model):
	food = models.ForeignKey(Food)
	Ingredient = models.ForeignKey(Ingredient)
	amount = models.IntegerField()
	def __unicode__(self):
		return self.food+self.Ingredient

class Drink(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	name = models.CharField(max_length=128, unique=True)
	like = models.PositiveIntegerField(default=0)
	amount = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.name


class Order_food(models.Model):
	table = models.ForeignKey(Table)
	food = models.ForeignKey(Food)
	amount = models.PositiveIntegerField(default=1)
	status = models.CharField(max_length=16, default="pending")
	def natural_key(self):
		return self.food.name,self.food.price,self.amount,self.status,str(self.food.picture),self.id
	def __unicode__(self):
		return self.status

class Order(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	table = models.ForeignKey(Table)
	datetime = models.DateTimeField(default=datetime.now)
	pay = models.BooleanField(default=False)
	finish = models.BooleanField(default=False)
	send = models.BooleanField(default=False)
	foods = models.ManyToManyField(Order_food)
	def natural_key(self):
		return self.table.number,self.datetime,self.finish,self.pk
	def __unicode__(self):
		return str(self.id)



class Order_drink(models.Model):
	order = models.ForeignKey(Order)
	drink = models.ForeignKey(Drink)
	amount = models.PositiveIntegerField(default=1)
	status = models.CharField(max_length=16, default="pending")
	def __unicode__(self):
		return self.status

class Employee(models.Model):
	resturant = models.ForeignKey(Restaurant)
	user = models.ForeignKey(User)
	salary = models.IntegerField()
	def __unicode__(self):
		return self.user

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	like = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField()

	def __unicode__(self):
		return self.title

# Modal form
class CategoryForm(forms.ModelForm):
        name = forms.CharField(max_length=50,
                help_text='Please enter the name of the category.')
        class Meta:
                # associate the model, Category, with the ModelForm
                model = Category
        fields = ('name',)
class PageForm(forms.ModelForm):
        title = forms.CharField(max_length=100,
                help_text='Please enter the title of the page.')
        url = forms.CharField(max_length=200,
                help_text='Please enter the URL of the page.')
        class Meta:
                model = Page
                # select which fields will be present on the form
                # (i.e. we are hiding the foreign key and views fields)
                fields = ('title','url')
	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')
		if not url.startswith('http://'):
			url = 'http://' + url
		cleaned_data['url'] = url
		return cleaned_data

class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=16)
	password = forms.CharField(widget=forms.PasswordInput)
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ["username","password","email",]

class UserProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	class Meta:
		model = UserProfile
		fields = [ 'picture',]

class PostForm(forms.ModelForm):
	text = forms.CharField(max_length=128)
	picture = forms.ImageField(required=False)
	class Meta:
		model = Post
		fields = ['text','picture',]

class BusinessPostForm(forms.ModelForm):
	text = forms.CharField(max_length=128,widget=forms.Textarea(attrs={'class': 'input-block-level','rows': 4}))
	picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'input-block-level',}))
	class Meta:
		model = BusinessPost
		fields = ['text','picture',]


class RestaurantForm(forms.ModelForm):
	name = forms.CharField(max_length=32)
	description = forms.CharField(max_length=128)
	address = forms.CharField(max_length=32)
	city = models.CharField(max_length=32, blank=True)
	zip_code = models.CharField(max_length=8, blank=True)
	country = models.CharField(max_length=32, blank=True)
	telephone = models.IntegerField(blank=True)
	picture = forms.ImageField(required=False)
	class Meta:
		model = Restaurant
		fields = ['name', 'description','address','city','country', 'zip_code','telephone','picture',]

class ShopForm(forms.ModelForm):
	name = forms.CharField(max_length=32)
	description = forms.CharField(max_length=128)
	telephone = models.IntegerField(blank=True)
	picture = forms.ImageField(required=False)
	class Meta:
		model = Shop
		fields = ['name', 'description','telephone','picture',]

class MenuForm(forms.ModelForm):
	name = forms.CharField(max_length=32)
	description = forms.CharField(max_length=128)
	price = models.IntegerField()
	picture = forms.ImageField()
	class Meta:
		model = Food
		fields = ['name', 'description', 'price', 'picture',]

class ProductForm(forms.ModelForm):
	name = forms.CharField(max_length=32)
	description = forms.CharField(max_length=128)
	price = models.IntegerField()
	picture = forms.ImageField()
	class Meta:
		model = Product
		fields = ['name', 'description', 'price', 'picture',]

	