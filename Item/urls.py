
from typing import ItemsView
from django.urls import path, include
from .views import Index, Profile, ItemDetail, AddItem, AddPhoneView, UserItemView, DeactivateUserView, PersomalDetailsView, UserSettingView, itemCategory, UserMessageView, FeedbackView, searchCategory
# , OpenCv

app_name = 'Item'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('accounts/profile', Profile.as_view(), name='profile'),
    path('accounts/profile/my-ads', UserItemView.as_view(), name='my-ads'),
    path('accounts/profile/setting', UserSettingView.as_view(), name='setting'),
    path('accounts/profile/setting/add-phone',
        AddPhoneView.as_view(), name='add_phone'),
    path('accounts/profile/setting/deactivate-user',
        DeactivateUserView.as_view(), name='deactivate_user'),
    path('accounts/profile/setting/personal-details',
        PersomalDetailsView.as_view(), name='personal_details'),
    path('accounts/profile/feedback', FeedbackView.as_view(), name='feedback'),
    path('product/<int:id>/', ItemDetail.as_view(), name='product-detail'),
    path('add-item', AddItem.as_view(), name='add-item'),
    path('category/<int:id>', itemCategory.as_view(), name='item-category'),
    path('category/', searchCategory, name='search'),
    # path('accounts/profile/message',UserMessageView.as_view(), name='message'),
    # path('accounts/profile/message/<int:id>',UserMessageView.as_view(), name='reply'),
    # path('open', OpenCv.as_view(), name='open')
]
