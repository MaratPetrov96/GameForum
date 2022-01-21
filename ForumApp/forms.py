from django.forms import *
from .models import *

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets={
            'content':Textarea(attrs={'rows':'3','cols':'25'})
            }

class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets={
            'content':Textarea(attrs={'rows':'3','cols':'25'})
            }

class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ['title','descr']
