from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import UpdateView

from .forms import NewTopicForm, NewPostForm
from .models import (
    Board,
    Topic,
    Post
)


def home(request):
    boards = Board.objects.all()
    post_count = Post.objects.count()
    topic_count = Topic.objects.count()
    # last_post = Post.objects.filter(topic__board=board)
    context = {
        'boards': boards
    }
    return render(request, 'home.html', context)


def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = Topic.objects.order_by('-last_update').annotate(
        replies=Count('posts') - 1)
    context = {
        'board': board,
        'topics': topics
    }
    return render(request, 'boards/topics.html', context)


@login_required
def topic_new(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            user = request.user
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            message = form.cleaned_data.get('message')
            Post.objects.create(
                message=message,
                topic=topic,
                created_by=user,
            )
            return redirect('topic-posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()

    context = {
        'board': board,
        'form': form
    }
    return render(request, 'boards/topic_new.html', context)


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    context = {
        'topic': topic
    }
    return render(request, 'boards/topic_posts.html', context)


@login_required
def topic_reply(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            user = request.user
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = user
            post.save()
            return redirect('topic-posts', pk=pk, topic_pk=topic_pk)
    else:
        form = NewPostForm()

    context = {
        'form': form,
        'topic': topic
    }
    return render(request, 'boards/topic_reply.html', context)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'boards/post_edit.html'
    pk_url_kwarg = 'post_pk'

    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic-posts', pk=post.topic.board.pk,
                        topic_pk=post.topic.pk)
