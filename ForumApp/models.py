from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    title = models.CharField('Tag',max_length=45)
    subscribers = models.ManyToManyField(User,related_name='subscribes',blank=True)

    def __repr__(self):
        return self.title

    def __str__(self):
        return repr(self)

class Idea(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE
                             ,related_name='ideas')
    title = models.CharField('Title',max_length=90)
    tags = models.ManyToManyField(Tag,related_name='ideas')
    descr = models.TextField('Description')
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField('last comment', auto_now_add=True)

    def __repr__(self):
        return f'{self.title}'

    def __str__(self):
        return repr(self)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE
                             ,related_name='comms')
    idea = models.ForeignKey(Idea,on_delete=models.CASCADE
                             ,related_name='comms')
    content = models.TextField('Content')
    date = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)
    parent = models.ForeignKey('self',on_delete=models.CASCADE
                                ,null=True,blank=True,related_name='replies')
    main_parent= models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,
                                   related_name='all_replies')

    def __repr__(self):
        return self.content+f' ({self.idea.pk})'+f' ({self.date.date()})'

    def __str__(self):
        return repr(self)
