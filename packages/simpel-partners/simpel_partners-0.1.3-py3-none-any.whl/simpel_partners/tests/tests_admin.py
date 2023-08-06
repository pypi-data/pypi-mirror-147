from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..admin import PartnerAdmin
from ..models import Partner

User = get_user_model()


class DummyRequest:
    def __init__(self, user):
        self.user = user


class PartnerAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            "staff",
            email="staff@email.com",
            password="demo_pass",
            is_staff=True,
        )
        cls.superuser = User.objects.create_superuser(
            "super",
            email="super@email.com",
            password="demo_pass",
        )

    def setUp(self):
        self.admin = PartnerAdmin(Partner, admin.site)
        self.partner = Partner(
            user=self.staff,
            name="Staff Partner",
            partner_type=Partner.ORGANIZATION,
        )
        self.partner_2 = Partner(
            user=self.superuser,
            name="Superuser Partner",
            partner_type=Partner.ORGANIZATION,
        )
        self.partner.save()
        self.partner_2.save()
        self.factory = RequestFactory()
        self.change_url = reverse(admin_urlname(self.admin.opts, "changelist"))

        staff_request = self.factory.get(self.change_url)
        staff_request.user = self.staff
        setattr(staff_request, "session", "session")
        self.staff_messages = FallbackStorage(staff_request)
        setattr(staff_request, "_messages", self.staff_messages)
        self.staff_request = staff_request

        superuser_request = self.factory.get(self.change_url)
        superuser_request.user = self.superuser
        setattr(superuser_request, "session", "session")
        self.superuser_messages = FallbackStorage(superuser_request)
        setattr(staff_request, "_messages", self.superuser_messages)
        self.superuer_request = superuser_request

        return super().setUp()

    def test_partner_admin_permissions(self):
        # Staff
        request = DummyRequest(self.staff)
        view_perm = self.admin.has_view_permission(request)
        self.assertEqual(view_perm, True)
        activate_perm = self.admin.has_activate_permission(request)
        self.assertEqual(activate_perm, False)
        verify_perm = self.admin.has_verify_permission(request)
        self.assertEqual(verify_perm, False)

        # Super User
        request = DummyRequest(self.superuser)
        view_perm = self.admin.has_view_permission(request)
        self.assertEqual(view_perm, True)
        activate_perm = self.admin.has_activate_permission(request)
        self.assertEqual(activate_perm, True)
        verify_perm = self.admin.has_verify_permission(request)
        self.assertEqual(verify_perm, True)

    def test_partner_name_method(self):
        name = self.admin.partner_name(self.partner)
        self.assertLessEqual(len(name), 60)

    def test_partner_readonly_fields(self):
        # Staff has user in readonly_fields
        request = DummyRequest(self.staff)
        readonly_fields = self.admin.get_readonly_fields(request)
        self.assertIn("user", readonly_fields)
        # Superuser has empty readonly_fields
        request = DummyRequest(self.superuser)
        readonly_fields = self.admin.get_readonly_fields(request)
        self.assertEqual(len(readonly_fields), 0)

    def test_activate_partner_action(self):
        queryset = self.admin.model.objects.all()
        queryset.update(is_active=False)

        inactive_partners = queryset.filter(is_active=False)
        self.assertEqual(inactive_partners.count(), 2)

        self.admin.activate_partner(self.staff_request, queryset)
        active_partners = self.admin.model.objects.filter(is_active=True)
        self.assertEqual(active_partners.count(), 2)

    def test_deactivate_partner_action(self):
        queryset = self.admin.model.objects.all()
        queryset.update(is_active=True)

        active_partners = queryset.filter(is_active=True)
        self.assertEqual(active_partners.count(), 2)

        self.admin.deactivate_partner(self.staff_request, queryset)
        inactive_partners = self.admin.model.objects.filter(is_active=False)
        self.assertEqual(inactive_partners.count(), 2)

    def test_verify_partner_action(self):
        queryset = self.admin.model.objects.all()
        queryset.update(is_active=True, is_verified=False)

        unverified_partners = queryset.filter(is_verified=False)
        self.assertEqual(unverified_partners.count(), 2)

        self.admin.verify_partner(self.staff_request, queryset)
        verified_partners = self.admin.model.objects.filter(is_verified=True)
        self.assertEqual(verified_partners.count(), 2)

    def test_verify_inactive_partner_action(self):
        queryset = self.admin.model.objects.all()
        queryset.update(is_active=False, is_verified=False)

        unverified_partners = queryset.filter(is_verified=False)
        self.assertEqual(unverified_partners.count(), 2)

        self.admin.verify_partner(self.staff_request, queryset)
        verified_partners = self.admin.model.objects.filter(is_verified=True)
        self.assertEqual(verified_partners.count(), 0)

    def test_deverify_partner_action(self):
        queryset = self.admin.model.objects.all()
        queryset.update(is_active=True, is_verified=True)

        verified_partners = queryset.filter(is_verified=True)
        self.assertEqual(verified_partners.count(), 2)

        self.admin.deverify_partner(self.staff_request, queryset)
        unverified_partners = self.admin.model.objects.filter(is_verified=False)
        self.assertEqual(unverified_partners.count(), 2)

    def test_activate_partner_action_view(self):
        queryset = self.admin.model.objects.all()
        queryset.update(is_active=False)
        data = {"action": "activate_partner", "_selected_action": [obj.id for obj in queryset.all()]}
        change_url = reverse(admin_urlname(self.admin.opts, "changelist"))

        self.client.login(username=self.staff.username, password="demo_pass")
        response = self.client.post(change_url, data, follow=True)
        self.client.logout()

        active_partners = self.admin.model.objects.filter(is_active=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(active_partners.count(), 0)

    def test_deactivate_partner_action_view(self):
        queryset = self.admin.model.objects.all()
        queryset.update(is_active=False)
        data = {"action": "deactivate_partner", "_selected_action": [obj.id for obj in queryset.all()]}
        change_url = reverse(admin_urlname(self.admin.opts, "changelist"))

        self.client.login(username=self.staff.username, password="demo_pass")
        response = self.client.post(change_url, data, follow=True)
        self.client.logout()

        active_partners = self.admin.model.objects.filter(is_active=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(active_partners.count(), 0)
