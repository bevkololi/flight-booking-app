from django.db import models


class TimestampsMixin(models.Model):
    """
    The TimestampsMixin has two fields, created_at and updated_at, used to determine
    when the model was created and when it was updated respectively.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Set the model as abstract to prevent migrations from being created
        abstract = True

        # Will be ordered in order of models created first by default
        ordering = ['-created_at', '-updated_at', '-id']