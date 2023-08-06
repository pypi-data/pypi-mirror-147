from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from simpel_contacts.models import (
    BillingAddress, Country, DeliverableAddress, LinkedAddress, LinkedContact, ShippingAddress,
)

User = get_user_model()


def get_valid_address_data():
    country = Country.objects.get(iso_3166_1_a2="ID")
    data = dict(
        title=LinkedAddress.MR,
        name="Admin",
        line_1="Street name",
        line_2="",
        line_3="",
        city="Bandar Lampung",
        province="Lampung",
        country=country,
        postcode="35223",
    )
    return data


class LinkedContactModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            "demo_user",
            email="demo@email.com",
            password="demo_pass",
        )
        self.contact = LinkedContact(
            linked_object=self.user,
            contact_type=LinkedContact.PHONE,
            contact="+62895605838757",
            is_verified=True,
        )
        self.contact.save()
        self.country = Country.objects.get(iso_3166_1_a2="ID")
        return super().setUp()

    def test_linked_contact_to_dict(self):
        data = self.contact.to_dict()
        self.assertEqual(data["linked_object"], self.user)
        self.assertEqual(data["contact"], "+62895605838757")

    def test_create_linked_contact(self):
        user_ctype = ContentType.objects.get_for_model(User)
        user_contacts = user_ctype.linked_contacts.filter(linked_object_id=self.user.id)
        user_contact = user_contacts.first()
        self.assertEqual(user_contacts.count(), 1)
        self.assertEqual(user_contact.linked_object, self.user)


class LinkedAddressModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            "demo_user",
            email="demo@email.com",
            password="demo_pass",
        )
        address_data = get_valid_address_data()
        address_data.update(
            {
                "linked_object": self.user,
                "address_type": LinkedAddress.HOME,
                "phone_number": "+62895605838757",
                "notes": "Nothing",
                "primary": True,
            }
        )
        self.address = LinkedAddress(**address_data)
        self.address.save()
        return super().setUp()

    def test_linked_address_to_dict(self):
        data = self.address.to_dict()
        self.assertEqual(data["linked_object"], self.user)
        self.assertEqual(data["phone_number"], "+62895605838757")

    def test_create_linked_contact(self):
        user_ctype = ContentType.objects.get_for_model(User)
        user_addresses = user_ctype.linked_addresses.filter(linked_object_id=self.user.id)
        user_address = user_addresses.first()
        self.assertEqual(user_addresses.count(), 1)
        self.assertEqual(user_address.linked_object, self.user)


class BillingAddressTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            "demo_user",
            email="demo@email.com",
            password="demo_pass",
        )
        address_data = get_valid_address_data()
        address_data.update(
            {
                "content": self.user,
                "notes": "Nothing",
                "primary": True,
            }
        )
        self.address = BillingAddress(**address_data)
        self.address.save()
        return super().setUp()

    def test_billing_address_to_dict(self):
        data = self.address.to_dict()
        self.assertEqual(data["content"], self.user)
        self.assertEqual(data["notes"], "Nothing")
        self.assertEqual(data["primary"], True)


class ShippingAddressTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            "demo_user",
            email="demo@email.com",
            password="demo_pass",
        )
        address_data = get_valid_address_data()
        address_data.update(
            {
                "content": self.user,
                "notes": "Nothing",
                "primary": True,
            }
        )
        self.address = ShippingAddress(**address_data)
        self.address.save()
        return super().setUp()

    def test_shipping_address_to_dict(self):
        data = self.address.to_dict()
        self.assertEqual(data["content"], self.user)
        self.assertEqual(data["notes"], "Nothing")
        self.assertEqual(data["primary"], True)


class DeliverableAddressTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            "demo_user",
            email="demo@email.com",
            password="demo_pass",
        )
        address_data = get_valid_address_data()
        address_data.update(
            {
                "content": self.user,
                "notes": "Nothing",
                "primary": True,
            }
        )
        self.address = DeliverableAddress(**address_data)
        self.address.save()
        return super().setUp()

    def test_deliverable_address_to_dict(self):
        data = self.address.to_dict()
        self.assertEqual(data["content"], self.user)
        self.assertEqual(data["notes"], "Nothing")
        self.assertEqual(data["primary"], True)
