from django.contrib.auth import get_user_model
from django.test import TestCase

from simpel_contacts.models import Country

from ..models import Partner, PartnerAddress

User = get_user_model()


class PartnerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_superuser(
            "demo_user_1",
            email="demo1@email.com",
            password="demo_pass",
        )
        cls.user_2 = User.objects.create_superuser(
            "demo_user_2",
            email="demo2@email.com",
            password="demo_pass",
        )
        cls.organization = Partner(
            user=cls.user_1,
            name="Organization Partner",
            partner_type=Partner.ORGANIZATION,
        )
        cls.organization.save()
        cls.personal = Partner(
            name="Personal Partner",
            partner_type=Partner.PERSONAL,
        )
        cls.personal.save()
        cls.partners = Partner.objects.all()

        # Partner Address
        country = Country.objects.get(iso_3166_1_a2="ID")
        address_data = dict(
            partner=cls.organization,
            title=PartnerAddress.MR,
            line_1="Street name",
            line_2="",
            line_3="",
            city="Bandar Lampung",
            province="Lampung",
            country=country,
            postcode="35223",
        )

        cls.partner_address_1 = PartnerAddress(
            address_type=PartnerAddress.SHIPPING,
            name="Partner 1",
            **address_data,
        )
        cls.partner_address_1.save()

        cls.partner_address_2 = PartnerAddress(
            address_type=PartnerAddress.BILLING,
            name="Partner 2",
            **address_data,
        )
        cls.partner_address_2.save()

        cls.partner_address_3 = PartnerAddress(
            address_type=PartnerAddress.DELIVERABLE,
            name="Partner 3",
            **address_data,
        )
        cls.partner_address_3.save()

    def tests_create_partners(self):
        self.assertEqual(str(self.organization), "Organization Partner")
        self.assertEqual(self.partners.count(), 2)
        self.assertEqual(self.partners.filter(partner_type=Partner.ORGANIZATION).count(), 1)
        self.assertEqual(self.partners.filter(partner_type=Partner.PERSONAL).count(), 1)

    def test_activate_partner(self):
        self.organization.is_active = False
        self.organization.save()
        self.organization.activate()
        self.assertEqual(self.organization.is_active, True)

    def test_deactivate_partner(self):
        self.organization.is_active = True
        self.organization.save()
        self.organization.deactivate()
        self.assertEqual(self.organization.is_active, False)

    def test_verify_active_partner(self):
        self.organization.is_active = True
        self.organization.is_verified = False
        self.organization.save()
        self.organization.verify()
        self.assertEqual(self.organization.is_verified, True)

    def test_verify_inactive_partner(self):
        self.organization.is_active = False
        self.organization.is_verified = False
        self.organization.save()
        with self.assertRaises(PermissionError):
            self.organization.verify()

    def test_deverify_verified_partner(self):
        self.organization.is_verified = True
        self.organization.save()
        self.organization.deverify()
        self.assertEqual(self.organization.is_verified, False)

    def test_deverify_unverified_partner(self):
        self.organization.is_verified = False
        self.organization.save()
        self.organization.deverify()
        self.assertEqual(self.organization.is_verified, False)

    def test_get_partner_for_user(self):
        partner_1 = Partner.get_for_user(self.user_1)
        partner_2 = Partner.get_for_user(self.user_2)
        self.assertEqual(partner_1.name, "Organization Partner")
        self.assertEqual(partner_2.user, self.user_2)
        self.assertEqual(partner_2.name, "demo_user_2")

    def test_partner_get_address(self):
        address = self.organization.get_address(address_type=PartnerAddress.HOME)
        self.assertEqual(address.name, "Partner 1")

    def test_get_partner_address_get_primary(self):
        organization_1_primary = PartnerAddress.objects.get_primary(partner=self.organization)
        personal_2_primary = PartnerAddress.objects.get_primary(partner=self.personal)
        self.assertEqual(organization_1_primary.name, "Partner 1")
        self.assertEqual(personal_2_primary, None)

    def test_get_partner_address_set_as_primary(self):
        self.partner_address_2.set_as_primary()
        primary = PartnerAddress.objects.get_primary(partner=self.organization)
        self.assertEqual(primary.id, self.partner_address_2.id)
        # Double Check
        self.partner_address_1.set_as_primary()
        primary = PartnerAddress.objects.get_primary(partner=self.organization)
        self.assertEqual(primary.id, self.partner_address_1.id)
        # make sure primary only 1 primary
        primaries = PartnerAddress.objects.filter(partner=self.organization, primary=True)
        self.assertEqual(primaries.count(), 1)

    def test_partner_address_property(self):
        address = self.organization.address
        shipping = self.organization.shipping_address
        billing = self.organization.billing_address
        deliverable = self.organization.deliverable_address
        self.assertEqual(address, self.organization.get_address())
        self.assertEqual(shipping.name, "Partner 1")
        self.assertEqual(billing.name, "Partner 2")
        self.assertEqual(deliverable.name, "Partner 3")

    def test_get_deliverable_info(self):
        deliverable = self.organization.deliverable_address
        deliverable_info = self.organization.get_deliverable_info()
        self.assertEqual(deliverable.to_dict(), deliverable_info)
        deliverable_info = self.personal.get_deliverable_info()
        self.assertEqual(dict(), deliverable_info)
