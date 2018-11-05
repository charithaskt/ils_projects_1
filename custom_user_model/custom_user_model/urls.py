from django.contrib import admin
from django.urls import path,re_path, include
from accounts import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('catalog/', include('opac.urls')),
    path('', RedirectView.as_view(url='/catalog/',permanent=True)), 
    #url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'), 
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    #url(r'^accounts/update/(?P<pk>[\-\w]+)/$', views.edit_user, name='account_update'),
    #re_path(r'^accounts/update/(?P<pk>[\-\w]+)/$', views.edit_user, name='account_update'),
    path('accounts/update/', views.edit_user, name='account_update'),
    path('accounts/profiles/', views.profiles_list, name='account_profiles'),
    path('accounts/profile/', views.profile_detail, name='profile_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

