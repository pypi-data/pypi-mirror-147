from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from simpel_contacts.abstracts import AbstractContact, AbstractCountry, AbstractShippingAddress, AbstractTypedAddress


class Country(AbstractCountry):
    pass


class LinkedContact(AbstractContact):

    linked_object_type = models.ForeignKey(
        ContentType,
        related_name="linked_contacts",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Linked object type"),
    )
    linked_object_id = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Linked instance primary key."),
    )
    linked_object = GenericForeignKey(
        "linked_object_type",
        "linked_object_id",
    )


class LinkedAddress(AbstractTypedAddress):

    phone_number = PhoneNumberField(
        _("Phone number"),
        blank=True,
        help_text=_("In case we need to call you about your order"),
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Note"),
        help_text=_("Tell us anything we should know."),
    )
    linked_object_type = models.ForeignKey(
        ContentType,
        related_name="linked_address",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Linked object type"),
    )
    linked_object_id = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Linked instance primary key."),
    )
    linked_object = GenericForeignKey(
        "linked_object_type",
        "linked_object_id",
    )


class ShippingAddress(AbstractShippingAddress):
    content_type = models.ForeignKey(
        ContentType,
        related_name="shipping_addresses",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Linked order"),
    )
    content_id = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Linked order primary key."),
    )
    content = GenericForeignKey(
        "content_type",
        "content_id",
    )

    class Meta:
        verbose_name = _("Shipping address")
        verbose_name_plural = _("Shipping addresses")


class BillingAddress(AbstractShippingAddress):
    content_type = models.ForeignKey(
        ContentType,
        related_name="billing_addresses",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Linked order"),
    )
    content_id = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Linked order primary key."),
    )
    content = GenericForeignKey(
        "content_type",
        "content_id",
    )

    class Meta:
        verbose_name = _("Billing address")
        verbose_name_plural = _("Billing addresses")


class DeliverableAddress(AbstractShippingAddress):
    content_type = models.ForeignKey(
        ContentType,
        related_name="deliverable_addresses",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Linked order"),
    )
    content_id = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Linked order primary key."),
    )
    content = GenericForeignKey(
        "content_type",
        "content_id",
    )

    class Meta:
        verbose_name = _("Deliverable address")
        verbose_name_plural = _("Deliverable addresses")
