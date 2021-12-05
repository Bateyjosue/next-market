from django.db import models
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Category, Item, User, Feedback
from django.views.generic import TemplateView, DetailView
from django.contrib import messages
from .forms import ItemForm
from .filters import CategoryFilter

from django.core.paginator import Paginator
# import cv2

# Create your views here.

class Index(View):
    def get(self, request):
        context = {
            'cat' : Category.objects.all(),
            'item' : Item.objects.all(),
        }
        return render(request, 'item/index.html', context)

# class OpenCv(View):
#     def get(self, request):
#         if request.method == 'GET' and request.GET['submit']:
#             img = cv2.imread('Resources/profile.png')
#             cap = cv2.VideoCapture(0)
#             cap.set(3, 640)
#             cap.set(4, 480)
#             cap.set(10, 100)
#             while True:
#                 success, img = cap.read()
#                 cv2.imshow('Video', img)
#                 if cv2.waitKey(50) & 0xFF == ord('n'):
#                     break
#         context = {
#             'cap' : cap
#         }
#         return render(request, 'item/open.html', context)

class Profile(TemplateView):
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            pass
        else:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs) 

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.request.user
        context['item'] = item
        return context

class ItemDetail(View):
    def get(self, request, id):
        context = {
            'feedbacks' : Feedback.objects.all().filter(item = id),
            'item' : Item.objects.all().get(id=id)
        }
        return render(request, 'item/product.html', context)
    def post(self, request, id):
        context = {
            'feedbacks' : Feedback.objects.all().filter(item = id),
            'item' : Item.objects.all().get(id=id)
        }
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            user = self.request.user
            item = Item.objects.all().get(id=id)
            owner = User.objects.all().get(id=request.POST['owner_id'])
            experience = request.POST['experience']
            feedback = request.POST['feedback']
            feedb = Feedback.objects.create(owner = owner, user=user, item = item, experience=experience, feedback=feedback)
            feedb.save()
            messages.success(request, 'Feed Added Successfully!!!')
            # return HttpResponse('')
        return render(request, 'item/product.html', context)    

class itemCategory(View):
    def get(self, request,id):
        search = request.GET.get('search')
        items = Item.objects.all().filter(category = id)
        paginator = Paginator(items, 8)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        if page.has_next():
            next_url = f'?page={page.next_page_number}'
        else:
            next_url = ''
        
        if page.has_previous():
            previous_url = f'?page={page.previous_page_number}'
        else:
            previous_url = ''

        if search is not None:
            search_item = Item.objects.all().filter(title__icontains = search)
            context = {
                'category' : Category.objects.all().get(id = id),
                'categories' : Category.objects.all(),
                'items' :page.object_list,
                'page' : page,
                'search' : search_item,
                'next_page_url' : next_url,
                'previous_page_url' : previous_url,
            }
        else:
            items  = Item.objects.all().filter(category = id),
            context = {
                'category' : Category.objects.all().get(id = id),
                'categories' : Category.objects.all(),
                'items' :page.object_list,
                'page' : page,
            }
        # search = CategoryFilter(request.GET, queryset = items)
        # item = search.qs

        return render(request,'item/product-category.html', context)
    def post(self, request):
        # context = {
        #     'items' : search_category
        # }
        # return render(request,'item/product-category.html',context)
        pass

def searchCategory(self, request):
    if request.method == 'GET':
        category = request.GET['category']
        search_category = Item.objects.all().filter(category = category)
        return render(request,'item/product-category.html',{'data' : search_category})
    else:
        item_details = Item.objects.all()
        return render(request,'item/product-category.html',{'data' : item_details})

# class ItemDetail(DetailView):
#     model = Item
#     template_name = 'product.html'
    # def get(seft,request, id):
    #     user = User.objects.get(pk=id)
    #     item = Item.objects.filter(user=id)
    #     return render(request, 'product.html',{'item':item})

class AddItem(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {
                'form' : ItemForm(),
                'cat' : Category.objects.all(),
                'item': Item.objects.all()
            }
        else:
            return redirect('account_login')

        return render(request, 'item/add-item.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            item  = Item.objects.all()
            cat = Category.objects.all()
            if request.method == 'POST':
                user = request.user
                cats = request.POST['category']
                cat_id = Category.objects.get(name = cats)
                category = cat_id
                title = request.POST['title']
                image = request.FILES.get('image')
                keywords = request.POST['keyword']
                description = request.POST['description']
                discount = request.POST['discount']
                price = request.POST['price']
                brand = request.POST['brand']
                model = request.POST['model']
                color = request.POST['color']
                condition = request.POST['condition']
                item = Item.objects.create(category=category,user=user,title=title,image=image,keywords=keywords,description=description,disc=discount,price=price,brand=brand,model=model,color=color,condition=condition)
                # if not Item.clean(self):
                #     messages.error(request, 'Image Dont safisfy condition')
                # else:
                item.save()
                messages.success(request, 'Post Added Successfully!!!')
                # redirect('/')
            else:
                messages.error(request,'Ooops, there is an error occuring in your process please contact the Admin!!!')
        else:
            return redirect('account_login')
        return render(request, 'item/add-item.html', {'cat' : cat}) 

        #     form = ItemForm(request.POST)
        #     if form.is_valid():
        #         item = form.save(commit=False)
        #         item.user= request.user
        #         item.save()
        #         messages.success(request, 'Post Added Successfully!!!')
        #         redirect('profile')
        #         return HttpResponseRedirect('/thanks/')
        # else:
        #     messages.error(request,'Ooops, there is an error occuring in your process please contact the Admin!!!')
        #     context = {
        #         'form' : ItemForm()
        #     }
        #     form = ItemForm()
        # return render(request, 'item/add-item.html') 

class UserItemView(View):
    def get(self, request):
        id = request.user.pk
        context ={
            'item' : Item.objects.filter(user=id)
        }
        return render(request, 'item/user-product.html', context)

    def post(self, request):
        product_id = request.POST.get('product_id')
        product_state = request.POST.get('state')
        if product_state == 'Activate':
            Item.objects.all().filter(pk = product_id).update(status=False)
            messages.success(request, 'Deactivated!!!')
        elif product_state == 'Deactivate':
            Item.objects.all().filter(pk = product_id).update(status=True)
            messages.success(request, 'Activated!!!')
        id = request.user.pk
        context ={
            'item' : Item.objects.filter(user=id)
        }
        return render(request, 'item/user-product.html', context)




class UserSettingView(View):
    def get(self, request):
        id = request.user.pk
        user = User.objects.filter(pk = id)
        return render(request, 'accounts/setting.html', {'user':user})

    def post(self, request):
        pass

class EmailForm(View):
    def get(self, request):
        return render(request, 'account/email.html')
    def post(self, request):
        pass

class UserMessageView(View):
    def get(self, request):
        context = {
            'chat' : ChatMessage.objects.all()
        }
        return render(request, 'accounts/message.html', context)
    def post(self, request):
        context = {
            'chat' : ChatMessage.objects.all()
        }
        if request.method == 'POST':
            sender = request.user
            receiver = request.POST.get('receiver')
            message = request.POST.get('message')
            send_chat = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
            send_chat.save()
            messages.success(request, 'Post Added Successfully!!!')
        else:
            messages.error(request,'Ooops, there is an error occuring in your process please contact the Admin!!!')
        return render(request, 'accounts/message.html', context)

class FeedbackView(View):
    def get(self, request):
        prod = request.GET.get('prod-ID')
        context = {
            'feedbacks' : Feedback.objects.all().filter(item=prod)
        }
        return render(request, 'item/feedback.html', context)

class AddPhoneView(View):
    def get(self, request):
        context ={
            'number' : User.objects.all().filter(username=request.user),
        }
        return render(request, 'accounts/add-phone.html',context)
    def post(self, request):
        number = request.POST.get('new_number')
        User.objects.all().filter(pk=request.user.pk).update(phone=number)
        messages.success(request, 'Number Added successfully!!!')
        context ={
            'number' : User.objects.all().filter(username=request.user),
        }
        return render(request, 'accounts/add-phone.html',context)

class PersomalDetailsView(View):
    def get(self, request):
        context ={
            'user' : User.objects.all().filter(username=request.user)
        }
        return render(request, 'accounts/personal-details.html',context)
    def post(self, request):
        id = request.POST.get('id_user')
        picture = request.POST.get('picture')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone-number')
        email = request.POST.get('email-address')
        country = request.POST.get('country')
        city = request.POST.get('city')
        district = request.POST.get('district')
        User.objects.all().filter(pk = id).update(picture= picture, first_name = first_name, last_name = last_name,
        sex=gender, dob = dob, phone = phone, email = email,country=country, city=city, district=district)
        messages.success(request, 'Saved')
        context ={
            'user' : User.objects.all().filter(username=request.user)
        }
        return render(request, 'accounts/personal-details.html',context)

class DeactivateUserView(View):
    def get(self, request):
        context = {
            'user' : User.objects.all().filter(username=request.user)
        }
        return render(request, 'accounts/deactivate-user.html',context)
    def post(self, request):
        btn_action = request.GET.get('deactivate')
        if btn_action == 'deactivate':
            User.objects.all().filter(pk = request.user.pk).update(active = False)