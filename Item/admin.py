from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk','password','username','first_name','last_name','phone','email','is_staff','is_active','date_joined','dob','sex','picture','country','city','district')
    fields= ['first_name','last_name','phone','email','is_staff','is_active','dob','sex','picture','country','city','district']
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk','category','user','title',
    'image',
    'keywords','price','color','condition',
    'brand','status','is_ads')
    fields =[]
    exclude = ()
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk','name','icon','description')
@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display =('pk','name','price','description')
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk','item','advert','user','quantity')
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id','owner','user','item','experience','feedback')
    
# @admin.register(ChatMessage)
# class ChatMessageAdmin(admin.ModelAdmin):
#     list_display = ('id','sender', 'receiver', 'message', 'received_at', 'session', 'is_read')
