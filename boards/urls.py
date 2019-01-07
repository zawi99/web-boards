from django.conf.urls import url

from .views import (
    TopicListView,
    topic_new,
    PostListView,
    topic_reply,
    PostEditView,
    TopicDeleteView
)

urlpatterns = [
    url(r'^(?P<pk>\d+)/$',
        TopicListView.as_view(),
        name='topic-list'),
    url(r'^(?P<pk>\d+)/new/$',
        topic_new,
        name='topic-new'),
    url(r'^(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/$',
        PostListView.as_view(),
        name='topic-posts'),
    url(r'^(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/reply/$',
        topic_reply,
        name='topic-reply'),
    url(r'^(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/post/(?P<post_pk>\d+)/edit/$',
        PostEditView.as_view(),
        name='post-edit'),
    url(r'^(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/delete/$',
        TopicDeleteView.as_view(),
        name='topic-delete'),
]
