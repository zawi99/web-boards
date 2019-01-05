from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin

from accounts.views import (signup,
                            UserAccountView,
                            UserUpdateView)
from boards.views import (TopicListView,
                          topic_new,
                          PostListView,
                          topic_reply,
                          BoardListView,
                          PostEditView,
                          TopicDeleteView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # accounts
    url(r'^account/$', UserAccountView.as_view(), name='account-detail'),
    url(r'^account/update/$', UserUpdateView.as_view(), name='account-update'),

    # boards
    url(r'^$', BoardListView.as_view(), name='home'),
    url(r'^boards/(?P<pk>\d+)/$', TopicListView.as_view(), name='topic-list'),
    url(r'^boards/(?P<pk>\d+)/new/$', topic_new, name='topic-new'),
    url(r'^boards/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/$',
        PostListView.as_view(),
        name='topic-posts'),
    url(r'^boards/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/reply/$', topic_reply,
        name='topic-reply'),
    url(
        r'^boards/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/post/(?P<post_pk>\d+)/edit/$',
        PostEditView.as_view(),
        name='post-edit'),
    url(r'^boards/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/delete/$',
        TopicDeleteView.as_view(),
        name='topic-delete'),

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
    url(
        r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]
