from django.test import TestCase
from .factories import StatusFactory
from django.utils.translation import gettext as _
from django.urls import reverse


class StatusTest(TestCase):

    def setUp(self):
        self.statuses = StatusFactory.create_batch(2)
        self.status = {
            'name': 'sample_text'
        }
        self.id = self.statuses[0].id
        self.user = {
            'password1': 'PswrdNmrc1',
            'password2': 'PswrdNmrc1',
            'first_name': 'John',
            'last_name': 'Cena',
            'username': 'bingchilling'
        }
        self.login_data = {
            'password': self.user['password1'],
            'username': self.user['username']
        }
        self.client.post(reverse('user_create'), data=self.user)
        self.client.post(reverse('user_login'), data=self.login_data)

    # testing statuses view
    def test_statuses_view(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Delete'))
        self.assertContains(response, _('Update'))
        for status in self.statuses:
            self.assertContains(response, status.name)

    def test_statuses_view_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('statuses'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    # testing status create view
    def test_status_create_get_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('status_create'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_status_create_post_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.post(reverse('status_create'), data=self.status, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_status_create_get(self):
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Create'))

    def test_status_create_post_correct_code(self):
        response = self.client.post(reverse('status_create'), data=self.status)
        self.assertEqual(response.status_code, 302)

    def test_status_create_post_correct_content(self):
        response = self.client.post(reverse('status_create'), data=self.status, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Status created successfully!'))

    def test_status_create_post_incorrect(self):
        response = self.client.post(reverse('status_create'), data=self.status)
        response = self.client.post(reverse('status_create'), data=self.status, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('exists'))

        response = self.client.post(reverse('status_create'), data={'name': 'a'*500}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Create'))


    # testing status update view
    def test_status_update_get_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('status_update', args=[self.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_status_update_post_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.post(reverse('status_update', args=[self.id]), data=self.status, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_status_update_get(self):
        response = self.client.get(reverse('status_update', args=[self.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'/statuses/{self.id}/update/')

    def test_status_update_get_in_progress(self):  # TODO
        assert True

    def test_status_update_post_correct_code(self):
        response = self.client.post(reverse('status_update', args=[self.id]), data=self.status)
        self.assertEqual(response.status_code, 302)

    def test_status_update_post_correct_content(self):
        response = self.client.post(reverse('status_update', args=[self.id]), data=self.status, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Status updated successfully!'))

    def test_status_update_post_incorrect(self):
        self.client.post(reverse('status_create'), data=self.status, follow=True)
        response = self.client.post(reverse('status_update', args=[self.id]), data=self.status, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('exists'))

        response = self.client.post(reverse('status_update', args=[self.id]), data={'name': 'a'*500}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('update'))

    # testing status delete view
    def test_status_delete_post_not_logged_in(self):
        self.client.post(reverse('user_logout'))
        response = self.client.get(reverse('status_delete', args=[self.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Password'))

    def test_status_delete_get(self):
        response = self.client.get(reverse('status_delete', args=[self.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('delete'))
        self.assertContains(response, f'/statuses/{self.id}/delete/')

    def test_status_delete_get_in_progress(self):  # TODO
        assert True

    def test_status_delete_post_correct_code(self):
        response = self.client.post(reverse('status_delete', args=[self.id]))
        self.assertEqual(response.status_code, 302)

    def test_status_delete_post_correct_content(self):
        response = self.client.post(reverse('status_delete', args=[self.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Status deleted successfully!'))
        self.assertNotContains(response, self.statuses[0].name)
