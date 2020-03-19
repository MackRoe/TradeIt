import datetime

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from mysite import settings


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, default=True,
        )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # def __str__(self):
    #     return self.username


class Offer(models.Model):
    offer_maker = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    offer_title = models.CharField(max_length=200)
    offer_description = models.TextField()
    tokens_requested = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    slug = models.CharField(max_length=settings.OFFER_PAGE_TITLE_MAX_LENGTH, blank=True, editable=False,
                            help_text="Unique URL path to access this page. Generated by the system.")

    # transaction_location: CharField
    # transaction_complete: BooleanField

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.offer_title

    def get_absolute_url(self):
        """ Returns a fully-qualified path for a page (/droxey/my-new-wiki-page). """
        path_components = {'username': self.username, 'slug': self.slug}
        return reverse('offer-page', kwargs=path_components)

    def save(self, *args, **kwargs):
        """ Creates a URL safe slug automatically when a new a page is created. """

        # STRETCH CHALLENGES:
        #   1. Add time zone support for `created` and `modified` dates if you're receiving the warning below:
        #       RuntimeWarning: DateTimeField received a naive datetime (YYYY-MM-DD HH:MM:SS)
        #       while time zone support is active.
        #   2. Add the ability to update the slug when the Page is edited.
        if not self.pk:  # To detect new objects, check if self.pk exists.
            self.slug = slugify(self.offer_title, allow_unicode=True)

        # Call save on the superclass.
        return super(Offer, self).save(*args, **kwargs)
