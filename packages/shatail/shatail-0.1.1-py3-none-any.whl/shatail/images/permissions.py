from django.dispatch import receiver
from django.test.signals import setting_changed

from shatail.images import get_image_model
from shatail.images.models import Image
from shatail.permission_policies.collections import CollectionOwnershipPermissionPolicy

permission_policy = None


class ImagesPermissionPolicyGetter:
    """
    A helper to retrieve the current permission policy dynamically.
    Following the descriptor protocol, this should be used as a class attribute::

        class MyImageView(PermissionCheckedMixin, ...):
            permission_policy = ImagesPermissionPolicyGetter()
    """

    def __get__(self, obj, objtype=None):
        return permission_policy


def set_permission_policy():
    """Sets the permission policy for the current image model."""

    global permission_policy
    permission_policy = CollectionOwnershipPermissionPolicy(
        get_image_model(), auth_model=Image, owner_field_name="uploaded_by_user"
    )


@receiver(setting_changed)
def update_permission_policy(signal, sender, setting, **kwargs):
    """
    Updates the permission policy when the `SHATAILIMAGES_IMAGE_MODEL` setting changes.
    This is useful in tests where we override the base image model and expect the
    permission policy to have changed accordingly.
    """

    if setting == "SHATAILIMAGES_IMAGE_MODEL":
        set_permission_policy()


# Set the permission policy for the first time.
set_permission_policy()
