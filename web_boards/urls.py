from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

from accounts.views import (signup,
                            UserAccountView,
                            UserUpdateView)
from boards.views import BoardListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # accounts
    url(r'^account/$', UserAccountView.as_view(), name='account-detail'),
    url(r'^account/update/$', UserUpdateView.as_view(), name='account-update'),

    # boards
    url(r'^$', BoardListView.as_view(), name='home'),
    url(r'^boards/', include('boards.urls', namespace='boards')),

    # auth
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^password/change/$',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),

    url(r'^password/reset/$',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password/reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]
