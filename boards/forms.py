from django import forms

from .models import (Topic, Post)


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(),
        help_text='The max length of the text is 4000.',
        max_length=4000,
    )

    class Meta:
        model = Topic
        fields = ('subject', 'message')


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('message',)
