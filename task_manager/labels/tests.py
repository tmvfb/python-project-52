from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .factories import LabelFactory
from django import test


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class LabelTest(TestCase):
    def setUp(self):
        self.labels = LabelFactory.create_batch(2)
        self.label = {"name": "sample_text"}
        self.id = self.labels[0].id

        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='JohnCena',
            password='bingchilling'
        )
        self.client.force_login(self.user)

    # testing labels view
    def test_labels_view(self):
        response = self.client.get(reverse("labels"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Delete"))
        self.assertContains(response, _("Update"))
        for label in self.labels:
            self.assertContains(response, label.name)

    def test_labels_view_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.get(reverse("labels"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    # testing label create view
    def test_label_create_get_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.get(reverse("label_create"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_label_create_post_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.post(
            reverse("label_create"), data=self.label, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_label_create_get(self):
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Create"))

    def test_label_create_post_correct_code(self):
        response = self.client.post(reverse("label_create"), data=self.label)
        self.assertEqual(response.status_code, 302)

    def test_label_create_post_correct_content(self):
        response = self.client.post(
            reverse("label_create"), data=self.label, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Label created successfully!"))

    def test_label_create_post_incorrect(self):
        response = self.client.post(reverse("label_create"), data=self.label)
        response = self.client.post(
            reverse("label_create"), data=self.label, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("exists"))

        response = self.client.post(
            reverse("label_create"), data={"name": "a" * 500}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Create"))

    # testing label update view
    def test_label_update_get_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.get(
            reverse("label_update", args=[self.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_label_update_post_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.post(
            reverse("label_update", args=[self.id]),
            data=self.label,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_label_update_get(self):
        response = self.client.get(reverse("label_update", args=[self.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"/labels/{self.id}/update/")

    def test_label_update_get_in_progress(self):  # TODO
        assert True

    def test_label_update_post_correct_code(self):
        response = self.client.post(
            reverse("label_update", args=[self.id]), data=self.label
        )
        self.assertEqual(response.status_code, 302)

    def test_label_update_post_correct_content(self):
        response = self.client.post(
            reverse("label_update", args=[self.id]),
            data=self.label,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Label updated successfully!"))

    def test_label_update_post_incorrect(self):
        self.client.post(reverse("label_create"), data=self.label, follow=True)
        response = self.client.post(
            reverse("label_update", args=[self.id]),
            data=self.label,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("exists"))

        response = self.client.post(
            reverse("label_update", args=[self.id]),
            data={"name": "a" * 500},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("update"))

    # testing label delete view
    def test_label_delete_post_not_logged_in(self):
        self.client.post(reverse("user_logout"))
        response = self.client.get(
            reverse("label_delete", args=[self.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Password"))

    def test_label_delete_get(self):
        response = self.client.get(
            reverse("label_delete", args=[self.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("delete"))
        self.assertContains(response, f"/labels/{self.id}/delete/")

    def test_label_delete_get_in_progress(self):  # TODO
        assert True

    def test_label_delete_post_correct_code(self):
        response = self.client.post(reverse("label_delete", args=[self.id]))
        self.assertEqual(response.status_code, 302)

    def test_label_delete_post_correct_content(self):
        response = self.client.post(
            reverse("label_delete", args=[self.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Label deleted successfully!"))
        self.assertNotContains(response, self.labels[0].name)

    # test permissions
    # TODO
