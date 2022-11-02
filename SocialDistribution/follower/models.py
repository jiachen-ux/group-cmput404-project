from email.policy import default
from select import select
from sqlite3 import Timestamp
from django.db import models
from django.dispatch import receiver
from author.models import Author
from django.utils import timezone


# Create your models here.
class Follower(models.Model):
    # type = models.CharField(default='followers', max_length=200)
    user = models.OneToOneField(Author, on_delete=models.CASCADE, related_name="user") #related_name = "username")
    followers = models.ManyToManyField(Author, related_name='followers', blank=True)

    def __str__(self):
        return self.user.username

    def add_follower(self, author):
        """
        Add a new follower
        """

        if not author in self.followers.all():
            self.followers.add(author)
            self.save()
    
    def remove_follower(self, author):
        """
        remove a follower
        """

        if author in self.followers.all():
            self.followers.remove(author)

    def unfollow(self, removee):
        '''
        removee = the person beign un-followed
        '''

        remover_follower_list = self #person terminating the friendship

        # remove follower from remover follower list 
        remover_follower_list.remove_follower(removee)

        # remove follower from removee follower list 
        follower_list = Follower.objects.get(user=removee)
        follower_list.remove_follower(self.user)
    
    def is_mutual_friend(self, friend):
        '''
        Is this is mutal friendship?
        -> true freinds
        '''

        if friend in self.followers.all():
            return True
        
        return False


class FollowRequest(models.Model):
    '''
    A follow request consists of two main parts:
        1. SENDER:
            - A person sending a follow request
        2. RECIEVER:
            - Person recieving the follow request
    '''

    sender = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='reciever')
    # see https://stackoverflow.com/questions/22538563/django-reverse-accessors-for-foreign-keys-clashing

    is_active = models.BooleanField(blank=False, null=False, default=True)

    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.sender.username

    
    def accept(self):
        '''
        Accept a follow request 
        Update both sender and reciever follow lists
        '''

        receiver_follower_lsit = Follower.objects.get(user=self.reciever)

        if receiver_follower_lsit:
            receiver_follower_lsit.add_follower(self.sender)
            sender_follower_list = Follower.objects.get(user=self.sender)
            if sender_follower_list:
                sender_follower_list.add_follower(self.reciever)
                self.is_active = False
                self.save()

    def decline(self):

        '''
        Decline a follow request
        it is decline by setting the 'is_active field to False
        '''

        self.is_active = False
        self.save()

    def cancel(self):
        '''
        the sender cancels the follow request
        '''


        self.is_active = False
        self.save()
        