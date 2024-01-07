from django.dispatch import receiver
from django.core.mail import send_mail
from MyBB import settings
from .models import Comment
from django.db.models.signals import post_save


@receiver
def notify_about_new_comment(sender, instance, created, **kwargs):
    if created:
        author = instance.post.author
        post = instance.post
        text = instance.text
        subject = 'new comment'
        message = f'hello /{author.username}/, here is a comment:: /{text}/ for your post:: /{post}/'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [author.email])


@receiver(post_save, sender=Comment)
def notify_about_comment(sender, instance, created, **kwargs):
    old_status = Comment.objects.get(pk=instance.pk).status
    if not old_status and instance.status == False:
        return
    sender = settings.DEFAULT_FROM_EMAIL
    recipient = instance.author.email
    send_notification(sender, [recipient], instance)


def send_notification(sender, recipient, comment):
    email_subject = 'comment accepted'
    email_message = f'your comment of the post {comment.comment_text} has been accepted'
    send_mail(email_subject, email_message, sender, [recipient])
