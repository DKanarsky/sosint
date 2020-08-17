from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

class Flag(models.Model):
    title = models.CharField(null=True, blank=True, max_length=200)
    task = models.TextField(verbose_name="Task")
    enabled = models.BooleanField(default=True, verbose_name="Enabled")
    comment = models.TextField(null=True, blank=True, verbose_name="Comment")
    key = models.CharField(null=True, blank=True, max_length=100, verbose_name="Secret")
    key_pattern = models.CharField(null=True, blank=True, max_length=100, verbose_name="Secret pattern")
    score = models.IntegerField(null=False, default=1)

    def __str__(self):
        return f"Title: {self.title} | Score:{self.score}"


class FlagChain(models.Model):
    child = models.ForeignKey(
        to="Flag", 
        on_delete=models.CASCADE, 
        related_name="chain",
        verbose_name="Flag identifier"
    )
    parent = models.ForeignKey(
        to="Flag", 
        on_delete=models.SET_NULL, 
        null=True,
        related_name="parents",
        verbose_name="Parent flag identifier"
    )
    enabled = models.BooleanField(
        default=True, 
        verbose_name="Enabled"
    )


class Submit(models.Model):
    flag = models.ForeignKey(
        to="Flag", 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Flag identifier"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True
    )
    value = models.CharField(
        null=False, 
        blank=False, max_length=100, 
        verbose_name="Answer value"
    )
    dt = models.DateTimeField(
        null=False, 
        default=datetime.now, 
        verbose_name="Date and time"
    )
    captured = models.BooleanField(
        null=False, 
        default=False, 
        verbose_name="Captured the Flag"
    )


    def norm_value(self):
        return self.value.lower().strip(" '\"")


    def save(self, *args, **kwargs):
        import re

        if self.pk:
            raise Exception("You can't modify existing submits!")
        try:
            flag = Flag.objects.get(pk=self.flag.pk)
            value = self.norm_value()
            if flag.key_pattern:
                regex = re.compile(flag.key_pattern)
                self.captured = regex.match(value) is not None
            else:
                self.captured = flag.key == value
        except ObjectDoesNotExist:
            return

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user} - {self.value} - {self.captured}"

