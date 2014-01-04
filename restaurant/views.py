import os.path
ROOT_PATH = os.path.dirname(__file__)
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from django.template import RequestContext, loader
from restaurant.models import *
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from project.settings import MEDIA_ROOT
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime
import time
import json
from django.db.models.fields.files import ImageFieldFile
from django.utils import simplejson
from django import shortcuts
from django.db.models import Q
from django.db.models import F
from django.db.models import Count


@login_required
def index(request):
    template = loader.get_template('restaurant/index.html')
    user = User.objects.get(username = request.user)
    restaurant_list = Restaurant.objects.filter(user = user)
    for res in restaurant_list:
        res.url = encode_category(res.name)    
    userProfile = UserProfile.objects.get(user = user)
    post = BusinessPost.objects.filter(business__in = userProfile.follower.all())
    recommended_restaurant = Restaurant.objects.filter(~Q(user = userProfile))
    print userProfile
    print recommended_restaurant
    context = RequestContext(request, {'restaurant_list':restaurant_list,
                                        'userProfile':userProfile,
                                        'post':post})
    context['form'] = RestaurantForm()

    return HttpResponse(template.render(context))

def change_picture(request):
    user = User.objects.get(username = request.user)
    if request.method == "POST":
        pictureForm = PictureForm(request.FILES)
        if pictureForm.is_valid():
            post = UserProfile.objects.get(user = user)
            post.picture = request.FILES['picture']
            return HttpResponse("yes")
    print request.POST['text']
    print request.FILES['picture']
    return index(request)


@login_required
def profile(request,username):
    template = loader.get_template('restaurant/index.html')
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    if username == userProfile.user.username:
        myFriend = MyFriend.objects.filter(Q(user = userProfile) | Q(friend = userProfile))
        friend_request = FriendInvitation.objects.filter(receiver = userProfile, approve = False)
        context = RequestContext(request, {'userProfile':userProfile, 'myFriend':myFriend, 
                                            'friend_request':friend_request})

    else:
        visited_userProfile = UserProfile.objects.get(user = User.objects.get(username = username))
        visited_friend = MyFriend.objects.filter(user = visited_userProfile)
        context = RequestContext(request, {'visited_userProfile':visited_userProfile, 'visited_friend':visited_friend, 
                                            'userProfile':userProfile})
        if FriendInvitation.objects.filter(Q(sender = visited_userProfile, receiver = userProfile) | Q(sender = userProfile, receiver = visited_userProfile)):
            visited_friend_request = FriendInvitation.objects.get(Q(sender = visited_userProfile, receiver = userProfile) | Q(sender = userProfile, receiver = visited_userProfile))
            context['visited_friend_request'] = visited_friend_request
        

    context['form'] = RestaurantForm()
    return HttpResponse(template.render(context))

@login_required
def feed(request):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    if request.method == 'POST':
        postForm = PostForm(request.POST, request.FILES)
        if postForm.is_valid():
            post = postForm.save(commit = False)
            post.user = userProfile
            post.save()
            return HttpResponseRedirect('/restaurant/feed/')
        else:
            return render_to_response('restaurant/feed.html', {'postForm':postForm}, context)
    else:
        postForm = PostForm()
        post = Post.objects.all().order_by('-datetime')
        myFriend = MyFriend.objects.filter(Q(user = userProfile) | Q(friend = userProfile))
        return render_to_response('restaurant/feed.html', {'postForm':postForm, 'post':post,
                                                            'userProfile':userProfile,
                                                            'myFriend':myFriend}, context)
@login_required
def chat(request):
    template = loader.get_template('restaurant/chat.html')
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    myFriend = MyFriend.objects.filter(Q(user = userProfile) | Q(friend = userProfile))
    context = RequestContext(request, {'userProfile':userProfile, 'myFriend':myFriend})
    return HttpResponse(template.render(context))

@login_required
def business(request):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = Restaurant.objects.filter(user = userProfile)
    return render_to_response('restaurant/business.html', {'userProfile':userProfile,
                                                            'restaurant':restaurant}, context) 

@login_required
def admin(request,restaurant_name):
    context = RequestContext(request)
    restaurant = Restaurant.objects.get(name = restaurant_name)
    food = Food.objects.filter(restaurant = restaurant).order_by('-datetime')
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    post = BusinessPost.objects.filter(business = restaurant).order_by('-datetime')
    return render_to_response('restaurant/admin.html', {'userProfile':userProfile,
                                                        'restaurant':restaurant,
                                                        'food':food,
                                                        'post':post}, context) 

@login_required
def new_business(request,type):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    if request.method == 'POST':
        if(type == 'shop'):
            shopForm = ShopForm(request.POST, request.FILES)
            if shopForm.is_valid():
                shop = shopForm.save(commit = False)
                shop.user = userProfile
                shop.save()
                return HttpResponseRedirect('/restaurant/business')
            else:
                return render_to_response('restaurant/new_business.html', {'shopForm':shopForm}, context)
        else:
            resForm = RestaurantForm(request.POST, request.FILES)
            if resForm.is_valid():
                res = resForm.save(commit = False)
                res.user = userProfile
                res.save()
                return HttpResponseRedirect('/restaurant/business')
            else:
                return render_to_response('restaurant/new_business.html', {'resForm':resForm}, context)
    else:
        if type == 'shop':
            shopForm = ShopForm()
            return render_to_response('restaurant/new_business.html', {'shopForm':shopForm,'userProfile':userProfile}, context) 
        else:
            resForm = RestaurantForm()
            return render_to_response('restaurant/new_business.html', {'resForm':resForm,'userProfile':userProfile}, context) 

@login_required
def hangout(request):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    return render_to_response('restaurant/hangout.html', {'userProfile':userProfile}, context) 

def business_home(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = Restaurant.objects.get(name = name)
    restaurantReview = RestaurantReview.objects.filter(restaurant = restaurant)
    food = Food.objects.filter(restaurant = restaurant).order_by('-datetime')[:6]
    post = restaurant.get_post()
    return render_to_response('restaurant/business_home.html', {'userProfile':userProfile,
                                                                'restaurant':restaurant,
                                                                'restaurantReview':restaurantReview,
                                                                'post':post,
                                                                'food':food}, context) 

def business_menu(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = Restaurant.objects.get(name = name)
    food = Food.objects.filter(restaurant = restaurant).order_by('-datetime')
    post = restaurant.get_post()
    return render_to_response('restaurant/business_menu.html', {'userProfile':userProfile,
                                                                'restaurant':restaurant,
                                                                'post':post,
                                                                'food':food}, context) 
def business_about(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = Restaurant.objects.get(name = name)
    food = Food.objects.filter(restaurant = restaurant).order_by('-datetime')[:6]
    post = restaurant.get_post()
    return render_to_response('restaurant/business_about.html', {'userProfile':userProfile,
                                                                'restaurant':restaurant,
                                                                'post':post,
                                                                'food':food}, context) 

def business_follower(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = Restaurant.objects.get(name = name)
    food = Food.objects.filter(restaurant = restaurant).order_by('-datetime')[:6]
    post = restaurant.get_post()
    return render_to_response('restaurant/business_follower.html', {'userProfile':userProfile,
                                                                'restaurant':restaurant,
                                                                'post':post,
                                                                'food':food}, context) 
def business_hungry(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = Restaurant.objects.get(name = name)
    food = Food.objects.filter(restaurant = restaurant).order_by('-datetime')[:6]
    post = restaurant.get_post()
    return render_to_response('restaurant/business_hungry.html', {'userProfile':userProfile,
                                                                'restaurant':restaurant,
                                                                'post':post,
                                                                'food':food}, context) 
def business_checkin(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = Restaurant.objects.get(name = name)
    food = Food.objects.filter(restaurant = restaurant).order_by('-datetime')[:6]
    post = restaurant.get_post()
    return render_to_response('restaurant/business_checkin.html', {'userProfile':userProfile,
                                                                'restaurant':restaurant,
                                                                'post':post,
                                                                'food':food}, context) 


def upload(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    business = userProfile.find_business(name)
    if business['type'] == "restaurant" :
        menuForm = MenuForm()
        if request.method == 'POST':
            menuForm = MenuForm(request.POST, request.FILES)
            if menuForm.is_valid():
                menu = menuForm.save(commit = False)
                menu.restaurant = business['business']
                menu.save()
                template = loader.get_template('restaurant/upload.html')
                context['business'] = business['business']
                context['menuForm'] = menuForm
                context['success'] = "yes"
                return HttpResponse(template.render(context))

        return render_to_response('restaurant/upload.html', {'business':business['business'],
                                                                      'menuForm':menuForm}, context)
    else:
        productForm = MenuForm()
        if request.method == 'POST':
            productForm = ProductForm(request.POST, request.FILES)
            if productForm.is_valid():
                product = productForm.save(commit = False)
                product.shop = business['business']
                product.save()
                return render_to_response('restaurant/upload.html', {'business':business['business'],
                                                                      'productForm':productForm,
                                                                      'success':"yes"}, context)

        return render_to_response('restaurant/upload.html', {'business':business['business'],
                                                                      'productForm':productForm}, context)

def upload_post(request,name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    business = userProfile.find_business(name)
    businessPForm = BusinessPostForm()
    if request.method == 'POST':
        businessPForm = BusinessPostForm(request.POST, request.FILES)
        if businessPForm.is_valid():
            post = businessPForm.save(commit = False)
            post.user = userProfile
            post.business = business['business']
            post.save()
            return render_to_response('restaurant/upload.html', {'business':business['business'],
                                                                      'businessPForm':businessPForm,
                                                                      'post_success':"yes"}, context)

    return render_to_response('restaurant/upload.html', {'business':business['business'],
                                                                      'businessPForm':businessPForm}, context)

def get_business_post(request):
    business_id = request.GET["business_id"]
    restaurant = Restaurant.objects.get(id = business_id)
    result = []
    for i in restaurant.get_post():
        result.append(i.to_dict())
    print result
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def get_new_business_post(request):
    business_id = request.GET["business_id"]
    restaurant = Restaurant.objects.get(id = business_id)
    result = []
    post = BusinessPost.objects.filter(business=restaurant)
    result.append(post[len(post)-1].to_dict())
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def first(request):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    return render_to_response('restaurant/first.html', {'userProfile':userProfile}, context) 

def hangout_home(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = userProfile.find_business(name)
    post = restaurant['business'].get_post().order_by('-datetime')
    postForm = BusinessPostForm()
    # need average price limit length of information
    return render_to_response('restaurant/hangout_home.html', {'userProfile':userProfile,
                                                                'business':restaurant['business'],
                                                                'post':post,
                                                                'postForm':postForm}, context) 
def kitchen(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = userProfile.find_business(name)
    orders = Order.objects.filter(restaurant = restaurant['business'], finish = False)
    orders.update(send=True)
    return render_to_response('restaurant/kitchen.html', {'userProfile':userProfile,
                                                            'restaurant':restaurant['business'],
                                                            'orders':orders},context)
def set_cooking(request):
    order_food = Order_food.objects.get(id = request.GET['order_food_id'])
    order_food.status = "cooking"
    order_food.save()
    return  HttpResponse("yes")

def set_finish(request):
    order_food = Order_food.objects.get(id = request.GET['order_food_id'])
    order_food.status = "finish"
    order_food.save()
    return  HttpResponse("yes")

def set_order_finish(request):
    order = Order.objects.get(id = request.GET['order_id'])
    order.finish = True
    order.save()
    return  HttpResponse("yes")

def service(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = userProfile.find_business(name)
    tables = Table.objects.filter(restaurant = restaurant['business']).order_by('number')
    menu = Food.objects.filter(restaurant = restaurant['business'])
    # need average price limit length of information
    return render_to_response('restaurant/service.html', {'userProfile':userProfile,
                                                            'restaurant':restaurant['business'],
                                                            'tables':tables,
                                                            'menu':menu}, context)

def get_order(request):
    table = Table.objects.get(id = request.GET['table_id'])
    order = Order.objects.filter(table = table, pay = False)
    data = serializers.serialize('json', order,use_natural_keys=True)
    return HttpResponse(data, mimetype="application/json")

def pay(request):
    table = Table.objects.get(id = request.GET['table_id'])
    order = Order.objects.filter(table = table, pay = False)
    order.update(pay = True)
    table.available = True;
    table.save()
    return HttpResponse("yes")
def pending_foods(request):
    table = Table.objects.get(id = request.GET['table_id'])
    pending_foods = Order_food.objects.filter(table = table, status = 'pending')
    if len(pending_foods) == 0:
        order = Order.objects.filter(table = table, pay = False)
        data = serializers.serialize('json', order,use_natural_keys=True)
        return HttpResponse(data, mimetype="application/json")
    else:
        data = serializers.serialize('json', [],use_natural_keys=True)
        return HttpResponse(data, mimetype="application/json")

def send_order(request):
    restaurant_id = request.GET['restaurant_id']
    restaurant = Restaurant.objects.get(id = restaurant_id)
    food_list = json.loads(request.GET['food_list'])
    table = Table.objects.get(id = request.GET['table_id'])
    order = Order(restaurant = restaurant, table = table)
    order.save()
    for i in food_list:
        food = Food.objects.get(id = i['food_id'])
        order_food = Order_food(table = table, food = food, amount = i['food_amount'])
        order_food.save()
        order.foods.add(order_food)
    if table.available == True:
        table.available = False;
        table.save()
    return HttpResponse("yes")
    # context = RequestContext(request)
    # user_name = User.objects.get(username = request.user)
    # restaurant_selected = Restaurant.objects.get(user = user_name, name = decode_category(restaurant_url_selected))
    # table_number = request.GET.get('table_number')
    # table = Table.objects.get(restaurant=restaurant_selected, number=table_number)
    # if table.available:
    #     table.available = False
    #     table.save()

    # food_order_list = request.GET.getlist('food_order_list')
    # order = Order(table=table,send=False)
    # order.save()
    # for food_name in food_order_list[0].split(","):
    #     food = Food.objects.get(restaurant=restaurant_selected,name=food_name)
    #     Order_food(order=order,food=food,amount=1).save()

    
    # print restaurant_selected
    # print table_number
    # print food_order_list
    # return HttpResponseRedirect('/restaurant/'+restaurant_url_selected+'/restaurant_services')



def hangout_menu(request, name):
    context = RequestContext(request)
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = userProfile.find_business(name)
    post = restaurant['business'].get_post().order_by('-datetime')
    postForm = BusinessPostForm()
    # need average price limit length of information
    return render_to_response('restaurant/hangout_menu.html', {'userProfile':userProfile,
                                                                'business':restaurant['business'],
                                                                'post':post,
                                                                'postForm':postForm}, context)
def commentRestaurantPost(request):
    user = UserProfile.objects.get(user = User.objects.get(username = request.user))
    text = request.GET["text"]
    post = BusinessPost.objects.get(id = request.GET['post_id'])
    comment = BusinessPostComment(user = user, post = post, text = text)
    comment.save()
    post.comment_num = F('comment_num')+1
    post.save()
    return HttpResponse(simplejson.dumps(comment.to_dict(user)), mimetype="application/json")

def get_restaurant_post_comment(request):
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    post = BusinessPost.objects.get(id = request.GET['post_id'])
    comment = BusinessPostComment.objects.filter(post = post)
    result = []
    for i in comment:
        result.append(i.to_dict(userProfile))
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def comment(request):
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    text = request.GET["text"]
    if request.GET["mode"] == "post":
        post = BusinessPost.objects.get(id = request.GET["post_id"])
        comment = Comment(user = userProfile, text = text)
        comment.save()
        post.comments.add(comment)
        post.comment_num = F('comment_num')+1
        post.save()
        return HttpResponse(simplejson.dumps(comment.to_dict(userProfile)), mimetype="application/json")
    elif request.GET["mode"] == "food":
        food = Food.objects.get(id = request.GET["food_id"])
        foodReview = FoodReview(user = userProfile, food = food, text = text)
        foodReview.save()
        return HttpResponse(simplejson.dumps(foodReview.to_dict(userProfile)), mimetype="application/json")
    elif request.GET["mode"] == "restaurant":
        restaurant = Restaurant.objects.get(id = request.GET["restaurant_id"])
        title = request.GET["title"]
        restaurantReview = RestaurantReview(user = userProfile,restaurant = restaurant, title = title, text = text)
        restaurantReview.save()
        return HttpResponse(simplejson.dumps(restaurantReview.to_dict(userProfile)), mimetype="application/json")
    else:
        comment = Comment.objects.get(id = request.GET["comment_id"])
        cc = CommentOfComment(user = userProfile, text = text)
        cc.save()
        comment.comments.add(cc)
        comment.comment_num = F('comment_num')+1
        comment.save()
        return HttpResponse(simplejson.dumps(cc.to_dict(userProfile)), mimetype="application/json")

def follow(request):
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    restaurant = Restaurant.objects.get(id = request.GET['restaurant_id'])
    if restaurant.follower.filter(id = userProfile.id).exists():
        restaurant.follower.remove(userProfile)
        restaurant.follow = F('follow')-1
        restaurant.save()
        return HttpResponse("Follow")
    else:
        restaurant.follower.add(userProfile)
        restaurant.follow = F('follow')+1
        restaurant.save()
        return HttpResponse("Following")
    
def like(request):
    user_id = request.GET["user_id"]
    userProfile = UserProfile.objects.get(id = user_id)
    mode = request.GET['mode']
    object_id = request.GET['id']
    if mode == "post":
        temp = BusinessPost.objects.get(id = object_id)
    elif mode == "comment":
        temp = BusinessPostComment.objects.get(id = object_id)
    elif mode == "commentOf":
        temp = CommentOfComment.objects.get(id = object_id)
    elif mode == "restaurantReview":
        temp = RestaurantReview.objects.get(id = object_id)
    elif mode == "foodReview":
        temp = FoodReview.objects.get(id = object_id)
    if temp.who_like.filter(id = user_id).exists():
        temp.like = F('like')-1
        temp.save()
        temp.who_like.remove(userProfile)
        return HttpResponse("Like")
    else:
        temp.who_like.add(userProfile)
        temp.like = F('like')+1
        temp.save()
        return HttpResponse("Unlike")
        


    return HttpResponse("bad")

def get_restaurant_table(request):
    restaurant_id = request.GET["restaurant_id"]
    restaurant = Restaurant.objects.get(id = restaurant_id)
    tables = Table.objects.filter(restaurant = restaurant).order_by('number')
    data = serializers.serialize('json', tables)
    return HttpResponse(data, mimetype="application/json")



def create_restaurant_table(request):
    restaurant_id = request.GET["restaurant_id"]
    table_number = request.GET["table_number"]
    restaurant = Restaurant.objects.get(id = restaurant_id)
    for i in range(int(table_number)):
            Table(restaurant = restaurant, number = i+1 ).save()
    restaurant.table_number = restaurant.table_number+int(table_number)
    restaurant.save()
    return HttpResponse("yes")
           
def get_menu(request):
    business_id = request.GET["restaurant_id"]
    restaurant = Restaurant.objects.get(id = business_id)
    result = []
    for i in restaurant.get_menu():
        result.append(i.to_dict())
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


def get_new_menu(request):
    business_id = request.GET["business_id"]
    restaurant = Restaurant.objects.get(id = business_id)
    result = []
    food = Food.objects.filter(restaurant=restaurant)
    result.append(food[len(food)-1].to_dict())
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def get_new_product(request):
    business_id = request.GET["business_id"]
    shop = Shop.objects.get(id = business_id)
    result = []
    product = Product.objects.filter(shop=shop)
    result.append(product[len(product)-1].to_dict())
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def get_product(request):
    business_id = request.GET["business_id"]
    shop = Shop.objects.get(id = business_id)
    result = []
    for i in shop.get_product():
        result.append(i.to_dict())
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


def get_msg_notification(request):
    first_time = request.GET["first_time"]
    user = UserProfile.objects.get(user = User.objects.get(username = request.user))
    if first_time == "0":
        msg = Message.objects.filter(receiver = user, read = False)
    else:
        patient = 0;
        while True:
            # check new message
            msg = Message.objects.filter(receiver = user, notify = False)
            if( len(msg)==0 and patient<3):
                print "server"
                time.sleep(5)
                patient+=1
            else:
                break
    msgNotification = []
    if len(msg) > 0:
        if first_time != 0:
            print "=================================="
            msg = Message.objects.filter(receiver = user, read = False)         
        for i in msg.values('sender').annotate(msg_count=Count('sender')):
            sender = UserProfile.objects.get(user = User.objects.get(username = str(i['sender'])))
            msn = MsgNotification(sender = sender, unread_num=i['msg_count'])
            msgNotification.append(msn)
        data = serializers.serialize('json', msgNotification)
        msg.update(notify = True) 
        return HttpResponse(data, mimetype="application/json")
    else:
        return HttpResponse("")
    

def get_new_message(request):
    user = UserProfile.objects.get(user = User.objects.get(username = request.user))
    sender = UserProfile.objects.get(user = User.objects.get(username = request.GET['sender']))

    msg = Message.objects.filter(sender = sender, receiver = user, read=False)
    data = serializers.serialize('json', msg,use_natural_keys=True)
    msg.update(read = True)
    return HttpResponse(data, mimetype="application/json") 

def get_old_message(request):
    sender = UserProfile.objects.get(user = User.objects.get(username = request.user))
    receiver = UserProfile.objects.get(user = User.objects.get(username = request.GET['receiver']))
    message = Message.objects.filter(Q(sender = sender, receiver = receiver) | Q(sender = receiver, receiver = sender))
    if len(message) == 0:
        return HttpResponse("No")
    else:
        message.update(read = True)
        data = serializers.serialize('json', message,use_natural_keys=True)
        return HttpResponse(data, mimetype="application/json")       

def get_old_comment(request):
    post = Post.objects.get(id = request.GET['post_id'])
    comment = post.get_comment()
    list = []
    if len(comment) == 0:
        return HttpResponse(list)
    else:
        for i in comment:
            list.append(i.to_dict())
        return HttpResponse(simplejson.dumps(list), mimetype="application/json")

def get_food_comment(request):
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    food = Food.objects.get(id = request.GET['food_id'])
    foodReview = FoodReview.objects.filter(food = food)
    list = []
    if len(foodReview) == 0:
        return HttpResponse(list)
    else:
        for i in foodReview:
            list.append(i.to_dict(userProfile))
        return HttpResponse(simplejson.dumps(list), mimetype="application/json")

def get_userprofile(request):
    user = UserProfile.objects.get(id = request.GET['user_id'])
    return HttpResponse(simplejson.dumps(user.to_dict()), mimetype="application/json")

def get_friends(request):
    user = UserProfile.objects.get(id = request.GET['user_id'])
    myFriend  =  MyFriend.objects.filter(Q(user = user) | Q(friend = user))
    result = []
    for i in myFriend:
        if i.user != user:
            result.append(i.user.to_dict())
        else:
            result.append(i.friend.to_dict())
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def get_business(request):
    user = UserProfile.objects.get(user = User.objects.get(username = request.user))
    result = []
    for i in user.get_restaurant():
        result.append(i.to_dict())
    for i in user.get_shop():
        result.append(i.to_dict())
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def get_restaurant(request):
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    result = []
    for i in Restaurant.objects.filter(~Q(user = userProfile)):
        if i not in userProfile.follower.all():
            result.append(i.to_dict())
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def get_following_restaurant(request):
    userProfile = UserProfile.objects.get(user = User.objects.get(username = request.user))
    result = []
    for i in userProfile.follower.all():
        result.append(i.to_dict())
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def get_order_kitchen2(request):
    restaurant = Restaurant.objects.get(id = request.GET['restaurant_id'])
    patient = 0
    while True:
        order = Order.objects.filter(send = False, restaurant = restaurant, finish = False)
        if(len(order)==0 and patient<5):
            print "server"
            time.sleep(3)
            patient+=1
        else:
            print "ready to send"
            break
    data = serializers.serialize('json', order,use_natural_keys=True)
    order.update(send=True)
    return HttpResponse(data, mimetype="application/json") 

def get_order_kitchen(request):
    # a = datetime.now()
    # restaurant_selected = Restaurant.objects.get( name = "1234")
    # table = Table.objects.filter(restaurant = restaurant_selected, available=False)
    # order = []
    # for t in table:
    #     order.append(Order.objects.filter(table=t))
    # food_order = []
    # for o in order:
    #     for fo in o:
    #         f = Order_food.objects.filter(order = fo)
    #         for i in f:
    #             food_order.append(i)

    # b = datetime.now()
    c = datetime.now()
    first_time = request.GET["first_time"]

    table = Table.objects.filter(restaurant__name = "1234",available=False)
    if first_time=="0":
        order = Order.objects.filter(finish = False, table__in = table)
        
    else:
        patient = 0
        while True:
            order = Order.objects.filter(send = False, table__in = table)
            if(len(order)==0 and patient<1000000000):
                print "server"
                time.sleep(5)
                patient+=1
            else:
                print "ready to send"
                break
        # order = Order.objects.filter(send = False, table__in = table)
      

    food_order2 = Order_food.objects.filter(order__in=order)
    d = datetime.now()

    data = serializers.serialize('json', food_order2,use_natural_keys=True)
    order.update(send=True)



    return HttpResponse(data, mimetype="application/json") 
def add_friend(request):
    sender = UserProfile.objects.get(user = User.objects.get(username = request.user))
    receiver = UserProfile.objects.get(user = User.objects.get(username = request.GET['friend']))
    FriendInvitation(sender = sender, receiver = receiver).save()
    return HttpResponse("yes")

def send_message(request):
    sender = UserProfile.objects.get(user = User.objects.get(username = request.user))
    receiver = UserProfile.objects.get(user = User.objects.get(username = request.GET['receiver']))
    Message(sender = sender, receiver = receiver, text = request.GET['text']).save()
    return HttpResponse("yes")    

def send_comment(request):
    user = UserProfile.objects.get(user = User.objects.get(username = request.user))
    post = Post.objects.get(id = request.GET['post_id'])
    comment = Comment(user = user, post = post, text = request.GET['text'])
    comment.save()
    return HttpResponse(simplejson.dumps(comment.to_dict(user)), mimetype="application/json")

def accept_friend(request):
    receiver = UserProfile.objects.get(user = User.objects.get(username = request.user))
    sender = UserProfile.objects.get(user = User.objects.get(username = request.GET['sender']))     
    friendInvitation = FriendInvitation.objects.filter(sender = sender, receiver = receiver)
    friendInvitation.update(approve = True)
    MyFriend(user = receiver, friend = sender).save()
    return HttpResponse("yes")
    
def user_test(request):
    template = loader.get_template('restaurant/g.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def free(request):
    template = loader.get_template('restaurant/free.html')
    # r= Restaurant.objects.get(name='1234')
    # table_list = Table.objects.filter(restaurant=r)
    context = RequestContext(request, {})

    return HttpResponse(template.render(context))


def restaurant_home(request,restaurant_url_selected):
    template = loader.get_template('restaurant/restaurant_home.html')
    user_name = User.objects.get(username =request.user)
    restaurant_list = Restaurant.objects.filter(user = user_name)
    restaurant = Restaurant.objects.get(name = restaurant_url_selected)
    restaurant.url = restaurant_url_selected
    food_list = Food.objects.filter(restaurant = restaurant)
    context = RequestContext(request, {'restaurant_list':restaurant_list,
                                        'restaurant_selected':restaurant,'food_list':food_list})
    context['loop_food'] = [int(i+1) for i in range(len(food_list))]
    form = RestaurantForm()
    context['form'] = form
    return HttpResponse(template.render(context))


            

def restaurant_kitchen(request,restaurant_url_selected):
    template = loader.get_template('restaurant/restaurant_kitchen.html')
    user_name = User.objects.get(username =request.user)
    restaurant_list = Restaurant.objects.filter(user = user_name)
    for res in restaurant_list:
            res.url = encode_category(res.name)
            # this loop is checked every time so it should stop when the condition satisfied once
            if res.url == restaurant_url_selected:
                restaurant_selected = res
            
    context = RequestContext(request, {'restaurant_list':restaurant_list, 'restaurant_selected':restaurant_selected})
    return HttpResponse(template.render(context))

def restaurant_stock(request,restaurant_url_selected):
    template = loader.get_template('restaurant/restaurant_stock.html')
    user_name = User.objects.get(username =request.user)
    restaurant_list = Restaurant.objects.filter(user = user_name)
    for res in restaurant_list:
            res.url = encode_category(res.name)
            # this loop is checked every time so it should stop when the condition satisfied once
            if res.url == restaurant_url_selected:
                restaurant_selected = res

    protein = Ingredient.objects.filter(restaurant=restaurant_selected, category="protein")
    carbohydrate = Ingredient.objects.filter(restaurant=restaurant_selected, category="carbohydrate")
    vegetable = Ingredient.objects.filter(restaurant=restaurant_selected, category="vegetable")
    fruit = Ingredient.objects.filter(restaurant=restaurant_selected, category="fruit")
    other = Ingredient.objects.filter(restaurant=restaurant_selected, category="other")
    drink = Drink.objects.filter(restaurant=restaurant_selected)        


    context = RequestContext(request, {'restaurant_list':restaurant_list, 'restaurant_selected':restaurant_selected,
        'protein':protein,'carbohydrate':carbohydrate,'vegetable':vegetable,'fruit':fruit,'other':other,'drink':drink})
    
    context['loop_protein'] = [int(i+1) for i in range(len(protein))]
    context['loop_carbohydrate'] = [int(i+1) for i in range(len(carbohydrate))]
    context['loop_vegetable'] = [int(i+1) for i in range(len(vegetable))]
    context['loop_fruit'] = [int(i+1) for i in range(len(fruit))]
    context['loop_other'] = [int(i+1) for i in range(len(other))]
    context['loop_drink'] = [int(i+1) for i in range(len(drink))]
    
    return HttpResponse(template.render(context))

def restaurant_employee(request,restaurant_url_selected):
    template = loader.get_template('restaurant/restaurant_employee.html')
    user_name = User.objects.get(username =request.user)
    restaurant_list = Restaurant.objects.filter(user = user_name)
    for res in restaurant_list:
            res.url = encode_category(res.name)
            # this loop is checked every time so it should stop when the condition satisfied once
            if res.url == restaurant_url_selected:
                restaurant_selected = res
            
    context = RequestContext(request, {'restaurant_list':restaurant_list, 'restaurant_selected':restaurant_selected})
    return HttpResponse(template.render(context))

def restaurant_statistic(request,restaurant_url_selected):
    template = loader.get_template('restaurant/restaurant_statistic.html')
    user_name = User.objects.get(username =request.user)
    restaurant_list = Restaurant.objects.filter(user = user_name)
    for res in restaurant_list:
            res.url = encode_category(res.name)
            # this loop is checked every time so it should stop when the condition satisfied once
            if res.url == restaurant_url_selected:
                restaurant_selected = res
            
    context = RequestContext(request, {'restaurant_list':restaurant_list, 'restaurant_selected':restaurant_selected})
    return HttpResponse(template.render(context))

def restaurant_services(request,restaurant_url_selected):
    template = loader.get_template('restaurant/restaurant_services.html')
    user_name = User.objects.get(username =request.user)

    restaurant_list = Restaurant.objects.filter(user = user_name)
    restaurant = Restaurant.objects.get(name = restaurant_url_selected)
    restaurant.url = restaurant_url_selected

    table_list = Table.objects.filter(restaurant=restaurant)
    food_list = Food.objects.filter(restaurant = restaurant)
    context = RequestContext(request, {'restaurant_list':restaurant_list, 'restaurant_selected':restaurant,
        'table_list':table_list, 'food_list':food_list})
    context['loop_food'] = [int(i+1) for i in range(len(food_list))]
    return HttpResponse(template.render(context))

def user_store(request):
    template = loader.get_template('restaurant/store.html')
    user_name = User.objects.get(username =request.user)
    restaurant_list = Restaurant.objects.filter(user = user_name)
    for res in restaurant_list:
            res.url = encode_category(res.name)
            
    context = RequestContext(request, {'restaurant_url_selected':restaurant_url_selected, 
        'restaurant_list':restaurant_list})
    return HttpResponse(template.render(context))
def category(request, category_name_url):
	if(request.session.test_cookie_worked()):
		print "the test cookie worked"
		request.session.delete_test_cookie()
	else:
		print "the test cookie is not worked "
        template = loader.get_template('restaurant/category.html')
        cat_list = get_category_list()
        category_name = decode_category(category_name_url)
        cat = Category.objects.get(name=category_name)

        if cat:
                # selects all the pages associated with the selected category
                pages = Page.objects.filter(category=cat)
                category_id = cat.id
                likes = cat.likes
        context_dict = {'cat_list': cat_list, 'category_name_url': category_name_url, 'category_name': category_name, 'category_id': category_id, 'likes': likes, 'pages':pages }
        context = RequestContext(request, context_dict)
        return HttpResponse(template.render(context))




@login_required
def like_category(request):
    context = RequestContext(request)
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    else:
        cat_id = request.POST['category_id']


    likes = 0
    if cat_id:
        c = Category.objects.get(id=int(cat_id))
        if c:
            likes = c.likes + 1
            c.likes = likes
            c.save()
    print "I like it"
    return HttpResponse(likes)

def get_food_menu(request,restaurant_url_selected):
    context = RequestContext(request)
    user_name = User.objects.get(username = request.user)
    restaurant_selected = Restaurant.objects.get(user = user_name, name = decode_category(restaurant_url_selected))
    table = request.GET['table_number']
    food_list = Food.objects.filter(restaurant = restaurant_selected)
    

    return HttpResponse({food_list:food_list})



def cook_food(request):
    context = RequestContext(request)
    food_id = request.GET['food_id']
    print Order_food.objects.get(pk=food_id)
    #set status of food to be cooking, customer cannot this ordered food.

    return HttpResponse("yes")

    

    # print food_order_list

   #  some_data = {
   # '1': 'foo',
   # '2': 'bar',
   #  }
   #  print simplejson.dumps(some_data)
   #  return HttpResponse(simplejson.dumps(some_data), 'application/json')
   #  print some_data
    # data = simplejson.dumps(data)





def update_ingredient_amount(request):
    category = request.GET['category']
    name = request.GET['name']
    amount = request.GET['amount']
    if category!="drink":
        ing = Ingredient.objects.filter(name = name)
        ing.update(amount=amount)
    else:
        dri = Drink.objects.filter(name=name)
        dri.update(amount=amount)
    return HttpResponse("success")





    


@login_required
def create_new_menu(request):
    context = RequestContext(request)

    food_name = request.GET['food_name']
    description = request.GET['food_description']
    price = request.GET['price']
    restaurant_url_selected = request.GET['restaurant_selected']
    user_name = User.objects.get(username = request.user)
    restaurant = Restaurant.objects.get(user = user_name, name = decode_category(restaurant_url_selected))
    Food(restaurant=restaurant, name=food_name, description=description, price=price).save()
     
    return HttpResponse("yes")

def delete_food(request):
    food = Food.objects.get(id = request.GET['food_id'])
    food.delete()
    return HttpResponse("yes")

def delete_post(request):
    post = BusinessPost.objects.get(id = request.GET['post_id'])
    post.delete()
    return HttpResponse("yes")

@login_required
def create_restaurant(request):
    context = RequestContext(request)
    success = False
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        print request.FILES
        if form.is_valid():
            return HttpResponse(simplejson.dumps(request.POST), mimetype="application/json")

        else:
            print "failf"
            errors = form.errors
            return HttpResponse(simplejson.dumps(errors), mimetype="application/json")


    return HttpResponse("WTF")




def register(request):
    context = RequestContext(request)
    if request.method == 'POST':      
        uform = UserForm(data = request.POST)
        pform = UserProfileForm(request.POST,request.FILES)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            pw = user.password
            user.set_password(pw)
            user.save()
            profile = pform.save(commit = False)
            profile.user = user
            profile.save()

            
            return HttpResponseRedirect('/restaurant/')
        else:
            return render_to_response('restaurant/register.html', {'uform': uform,'pform':pform}, context)          
    else:
        uform = UserForm()
        pform = UserProfileForm()
        return render_to_response('restaurant/register.html', {'uform': uform,'pform':pform}, context)

def encode_category(category_name):
        # returns the name converted for insert into url
        return category_name.replace(' ','_')

def decode_category(category_url):
        # returns the category name given the category url portion
        return category_url.replace('_',' ')

def add_category(request):
        # immediately get the context - as it may contain posting data
        context = RequestContext(request)
        if request.method == 'POST':
                # data has been entered into the form via Post
                form = CategoryForm(request.POST)
                if form.is_valid():
                        # the form has been correctly filled in,
                        # so lets save the data to the model
                        cat = form.save(commit=True)
                        # show the index page with the list of categories
                        return index(request)
                else:
                        # the form contains errors,
                        # show the form again, with error messages
                        pass
        else:
                # a GET request was made, so we simply show a blank/empty form.
                form = CategoryForm()

        # pass on the context, and the form data.
        return render_to_response('restaurant/add_category.html',
                {'form': form }, context)

def add_page(request, category_name_url):
        context = RequestContext(request)

        category_name = decode_category(category_name_url)
        if request.method == 'POST':
                form = PageForm(request.POST)
                if form.is_valid():
                        # this time we cant commit straight away
                        # because not all fields are populated
                        page = form.save(commit=False)
                        # retrieve and assign the category object to the new page
                        cat = Category.objects.get(name=category_name)
                        page.category = cat
                        # also plug in a default value for the no. of page views
                        page.views = 0
                        page.save()
                        # Now that the page is saved, display the category instead.
                        return category(request, category_name)
                else:
                        print form.errors
        else:
                form = PageForm()

        return render_to_response( 'restaurant/add_page.html',
                        {'category_name_url': category_name_url,
                                'category_name': category_name, 'form': form },
                        context)






@login_required
def delete_restaurant(request, restaurant_url_selected):
    context = RequestContext(request)
    user_name = User.objects.get(username = request.user)
    Restaurant.objects.get(user = user_name, name = decode_category(restaurant_url_selected)).delete()

    return HttpResponseRedirect('/restaurant/')



def add_ingredient(request):

    restaurant_selected = Restaurant.objects.get(name = decode_category(request.GET['restaurant_url_selected']))
    category = request.GET['category']
    ingredient_list = request.GET.getlist('ingredient_list[]')

    if category!="drink":
        for i in range(0, len(ingredient_list), 4):
            Ingredient(restaurant=restaurant_selected,name=ingredient_list[i], category=category).save()
       
    else:
        for i in range(0, len(ingredient_list), 4):
            Drink(restaurant=restaurant_selected,name=ingredient_list[i]).save()
        
    return HttpResponse("yes")

def get_ingredient(request):
    restaurant_selected = Restaurant.objects.get(name = decode_category(request.GET['restaurant_url_selected']))
    category = request.GET['category']
    ingredient = Ingredient.objects.filter(restaurant=restaurant_selected, category=category);
    data = serializers.serialize('json', ingredient,use_natural_keys=True)
    return HttpResponse(data, mimetype="application/json") 





def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return HttpResponseRedirect("/restaurant/")
                  # return render_to_response('restaurant/feed.html', {}, context)

		 # return render_to_response('restaurant/index.html', {}, context)
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              print  "invalid login details " + username + " " + password
              return render_to_response('restaurant/login.html', {}, context)
    else:
        # the login is a  GET request, so just show the user the login form.
        return render_to_response('restaurant/login.html', {}, context)

def some_view(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('restaurant/login/')
	else:
		return HttpResponseRedirect('restaurant/')

@login_required
def restricted(request):
	return HttpResponse('authenticated user , you can view this restriced page.')

@login_required
def user_logout(request):
	context = RequestContext(request)
        logout(request)
        return HttpResponseRedirect('/restaurant/')

class EnhancedJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode Django "ImageFieldFile"s.
    """

    def default(self, o):
        if isinstance(o, ImageFieldFile):
            # Treat ImageFieldFile as a unicode string
            return super(EnhancedJSONEncoder, self).default(unicode(o))
        else:

            return super(EnhancedJSONEncoder, self).default(o)