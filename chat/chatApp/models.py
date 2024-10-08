from django.db import models

# Create your models here.


class Conversation(models.Model):
    room_name = models.TextField(default="")
    created_at = models.DateTimeField(auto_now=True)
    block_conversation = models.BooleanField(default=False)
    user_bloking = models.IntegerField(null=True, blank=True, default=-1)

    def __str__(self):
        return self.room_name

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(max_length=200,null=True, blank=True,default="")
    sender_name = models.IntegerField(null=True, blank=True)
    time_added = models.DateTimeField(auto_now_add=True)
    read_msg = models.BooleanField(default=False)
    class Meta:
        ordering = ['time_added']
    def __str__(self):
        return "messageFrom_" + str(self.sender_name)
