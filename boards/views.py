from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView, ListView, DeleteView

from .forms import NewTopicForm, NewPostForm
from .models import (
    Board,
    Topic,
    Post
)


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_update').annotate(
            replies=Count('posts') - 1)
        return queryset


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


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = f'viewed_topic_{self.topic.id}'
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic,
                                       board__pk=self.kwargs.get('pk'),
                                       pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


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

            topic.last_update = timezone.now()
            topic.save()
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
        post.save()
        return redirect('topic-posts', pk=post.topic.board.pk,
                        topic_pk=post.topic.pk)


class TopicDeleteView(DeleteView):
    def get_object(self, queryset=None):
        user = self.request.user
        board_pk = self.kwargs.get('pk')
        topic_pk = self.kwargs.get('topic_pk')
        topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
        if not topic.starter == user and not user.is_staff:
            raise Http404
        return topic

    def get_success_url(self):
        board_pk = self.kwargs.get('pk')
        return reverse_lazy('topic-list', kwargs={'pk': board_pk})
