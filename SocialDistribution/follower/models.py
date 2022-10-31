from email.policy import default
from select import select
from sqlite3 import Timestamp
from django.db import models
from django.dispatch import receiver
from authors.models import Author
from django.utils import timezone


# Create your models here.
class Follower(models.Model):
    type = models.CharField(default='followers', max_length=200)
    user = models.OneToOneField(Author, on_delete=models.CASCADE, related_name="user") #related_name = "username")
    friends = models.ManyToManyField(Author, related_name='friends', blank=True)

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Add a new friend
        """

        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def remove_friend(self, account):
        """
        remove a friend
        """

        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        '''
        removee = the person beign un-friend
        '''

        remover_friends_list = self #person terminating the friendship

        # remove friend from remover friend list 
        remover_friends_list.remove_friend(removee)

        # remove friend from removee friend list 
        friends_list = Follower.objects.get(user=removee)
        friends_list.remove_friend(self.user)
    
    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        
        return False


    def to_dict(self):
        return {
            'type': self.type,
            'items': self.items,
        }

class FollowRequest(models.Model):
    '''
    A follow request consists of two main parts:
        1. SENDER:
            - A person sending a follow request
        2. RECIEVER:
            - Person recieving the friend request
    '''
    type = models.CharField(default='Follow', max_length=200)
    summary = models.TextField()
    sender = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='reciever')
    # see https://stackoverflow.com/questions/22538563/django-reverse-accessors-for-foreign-keys-clashing

    is_active = models.BooleanField(blank=True, null=False, default=True)

    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.sender.username

    
    def accept(self):
        '''
        Accept a follow request 
        Update both sender and reciever follow lists
        '''

        receiver_friend_lsit = Follower.objects.get(user=self.reciever)

        if receiver_friend_lsit:
            receiver_friend_lsit.add_friend(self.sender)
            sender_friend_list = Follower.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.reciever)
                self.is_active =False
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
        

    def to_dict(self):
        return {
            'type': self.type,
            'summary': f'{self.actor.displayName} wants to follow {self.object.displayName}',
            'actor': self.actor.username,
            'object': self.object.username,
        }