from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin

from accounts.views import signup
from boards.views import (home,
                          board_detail,
                          topic_new,
                          topic_posts,
                          topic_reply)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', home, name='home'),
    url(r'^boards/(?P<pk>\d+)/$', board_detail, name='board-detail'),
    url(r'^boards/(?P<pk>\d+)/new/$', topic_new, name='topic-new'),
    url(r'^boards/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/$', topic_posts,
        name='topic-posts'),
    url(r'^boards/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/reply/$', topic_reply,
        name='topic-reply'),

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
    url(
        r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]
