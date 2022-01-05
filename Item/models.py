from typing import KeysView
from django.db.models import Max
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.shortcuts import reverse

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.contrib.sessions.models import Session
from django.conf import settings



# Create your models here.
class User(AbstractUser):
    gender = (
        ('O', 'Others'),
        ('M', 'Male'),
        ('F', 'Female')
    )
    dob         = models.DateTimeField(null=True)
    sex         = models.CharField(max_length=10, choices =gender, default='O')
    picture     = models.ImageField(upload_to='media', null=False, blank=False)
    phone        = models.CharField(max_length=255, default='(000) 000 000 000')
    country     = CountryField()
    city        = models.CharField(max_length=255)
    district    = models.CharField(max_length=255, default='Kicukiro')

    def __str__(self):
        return self.username

class Category(models.Model):
    name        = models.CharField(max_length=100, help_text='Choose a specific composite names',unique=True,editable=True)
    icon        = models.ImageField(upload_to='category', null=False)
    description = models.TextField()
    createdAt   = models.DateTimeField(auto_now_add = True)
    updatedAT   = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize >= megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

class Item(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title       = models.CharField(max_length = 100, null = False, blank = False, default = 'product name')
    image       = models.ImageField(upload_to = 'item', null=False,validators=[validate_image] , help_text='Maximum file size allowed is 2Mb', default ='default/default-product.png')
    keywords    = models.CharField(max_length = 255, null = False, blank = False, default = 'keywords')
    description = models.TextField(null = False, blank = False, default = 'product description')
    disc        = models.IntegerField(null = False, blank = True, default=0)
    price       = models.FloatField(null = False, blank = False, default = 0.0000)
    brand       = models.CharField(max_length = 100, null = False, blank = False)
    model       = models.CharField(max_length = 100, null = False, blank = False)
    color       = models.CharField(max_length = 100, null = False, blank = False)
    conditions  = (
        ('Brand New', 'Brand New'),
        ('Used ', 'Used'),
    )
    condition   = models.CharField(max_length = 100, null = False, blank = False, choices=conditions,default='Used')
    status      = models.BooleanField(default=True) #In Checking Process
    is_ads      = models.BooleanField(default=False, blank=True) # Is advertize
    createdAt   = models.DateTimeField(auto_now_add = True)
    updatedAT   = models.DateTimeField(auto_now = True)
    # slug        = models.SlugField()
    class Meta:
        ordering = ['is_ads', '-updatedAT']

    def __str__(self):
        return self.title
    def clean(self):
        if not self.image:
            raise ValidationError('No Image!!!')
        else:
            w,h = get_image_dimensions(self.image)
            if w < 600:
                raise ValidationError("The image is %i pixel wide. It's supposed to be >600px" % w)
            if h < 600: 
                raise ValidationError("The image is %i pixel high. It's supposed to be >600px" % h)
    # def get_absolute_url(self):
    #     return reverse('Item:product-detail', Kwargs = {
    #         'slug' : self.slug
    #     })
    def deleteItem(self):
        pass
    
    def get_absolute_url(self):
        return reverse('Item:my-ads')
class Advert(models.Model):
    prom        = (
                    ('No Promote','Not Promote'),
                    ('P','premium'),
                    ('P+','Premium+'),
                    ('P++','Premium++'),
                )
    name            = models.CharField(max_length = 50, blank = True,choices = prom)
    price           = models.IntegerField(null = False, blank = False)
    description     = models.TextField(null = False, blank = False)
    createdAt       = models.DateTimeField(auto_now_add = True)
    updatedAT       = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.name

class Payment(models.Model):
    item        = models.ForeignKey(Item, on_delete=models.CASCADE)
    advert      = models.ForeignKey(Advert, on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    quantity    = models.IntegerField(null = False, blank = False)
    createdAt   = models.DateTimeField(auto_now_add = True)
    updatedAT   = models.DateTimeField(auto_now = True)
    def __str__(self):
        return str(self.advert) 

class Feedback(models.Model):
    EXP = (
                ('positive', 'positive'),
                ('neutral', 'neutral'),
                ('negative', 'negative')
            )
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    item        = models.ForeignKey(Item, on_delete = models.CASCADE)
    experience  = models.CharField(max_length=255, choices=EXP)
    feedback    = models.TextField()
    createdAt   = models.DateTimeField(auto_now_add = True)
    updatedAT   = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.feedback
    
# class Message(models.Model):
#     id_sender   = models.ForeignKey(User, on_delete = models.CASCADE)
#     id_receiver = models.ForeignKey(User, on_delete = models.CASCADE)
#     message    = models.TextField()
#     createdAt   = models.DateTimeField(auto_now_add = True)
#     updatedAT   = models.DateTimeField(auto_now = True)
    
#     def __str__(self):
#         return str(self.id_sender)
# class ChatMessage(models.Model):
#     sender      = models.ForeignKey(User, related_name = 'sender_user', on_delete=models.CASCADE)
#     receiver    = models.ForeignKey(User, related_name = 'receiver_user', on_delete=models.CASCADE)
#     message     = models.CharField(max_length = 200)
#     received_at = models.DateTimeField(auto_now_add = True)
#     # updated_at   = models.DateTimeField(auto_now = True)
#     session     = models.ForeignKey(Session,on_delete=models.CASCADE, default=Session.pk)
#     is_read     = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.message
    
#     def send_message(sender_user, receiver_user, body):
#         sender_message = ChatMessage(
#             sender = sender_user, 
#             receiver = receiver_user, 
#             message = body, 
#             is_read = False
#             )
#         sender_message.save()

#         receiver_message = ChatMessage(
#             sender = receiver_user, 
#             receiver = sender_user,  
#             message = body, 
#             is_read = True
#             )
#         receiver_message.save()
#         return sender_message
    
#     def get_messages(sender):
#         messages = ChatMessage.objects.filter(user=sender).values('receiver').annotate(last=Max('received_at')).order_by('-last')
#         users = []
#         for message in messages :
#             users.append({
#                 'user' : User.objects.get(pk = message['receiver']),
#                 'last' : message['last'],
#                 'unread' : ChatMessage.objects.filter(sender = sender, receiver__pk=message['receiver'], is_read=False).count()
#             })
#         return users 