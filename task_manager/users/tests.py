from django.test import TestCase
from .factories import UserFactory, PASSWORD
from django.utils.translation import gettext as _
from django.urls import reverse


class UserTest(TestCase):

    def setUp(self):
        self.users = UserFactory.create_batch(2)
        self.user = UserFactory.create_fake_user()
        self.user_incorrect_pw = UserFactory.create_fake_user(
            password='pw'
        )
        self.user_incorrect_un = UserFactory.create_fake_user(
            username=''
        )
        self.login_data = {
            'username': self.users[0].username,
            'password': PASSWORD
        }
        self.id = self.users[0].id
        self.wrong_id = self.users[1].id

    # testing users view
    def test_users_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        for user in self.users:
            self.assertContains(response, user.first_name)
            self.assertContains(response, user.last_name)
            self.assertContains(response, user.username)

    def test_users_view_links(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/users/create/')
        self.assertContains(response, '/users/login/')
        self.assertNotContains(response, '/users/logout/')
        self.assertNotContains(response, '/labels/')

    # testing user create view
    def test_user_create_get(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)

    def test_user_create_post_correct(self):
        response = self.client.post(reverse('user_create'), data=self.user)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('user_create'), data=self.user, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('User created successfully!'))

    def test_user_create_post_incorrect(self):
        for case in [self.user_incorrect_pw, self.user_incorrect_un]:
            response = self.client.post(reverse('user_create'), data=case)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, _('Something went wrong. Please check the entered data'))
            self.assertContains(response, _('Create'))

    # testing user login and logout
    def test_user_login_code(self):
        response = self.client.post(reverse('user_login'), data=self.login_data)
        self.assertEqual(response.status_code, 302)

    def test_user_login_content(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Logged in successfully!'))

    def test_users_view_links_logged_in(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        self.assertNotContains(response, '/users/create/')
        self.assertNotContains(response, '/users/login/')
        self.assertContains(response, '/users/logout/')
        self.assertContains(response, 'Labels')

    def test_user_logout(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.post(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.post(reverse('user_logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/users/login/')

    # testing user update view
    def test_user_update_post_not_logged_in(self):
        response = self.client.get(reverse('user_update', args=[self.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('You must login to be able to update your profile'))

    def test_user_update_get(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.get(reverse('user_update', args=[self.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Update'))

    def test_user_update_get_wrong_user(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.get(reverse('user_update', args=[self.wrong_id]))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.get(reverse('user_update', args=[self.wrong_id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Sorry, you don&#x27;t have permissions to update other users&#x27; data"))

    def test_user_update_post_wrong_user(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.post(reverse('user_update', args=[self.wrong_id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Sorry, you don&#x27;t have permissions to update other users&#x27; data"))

    def test_user_update_post_correct_code(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.post(reverse('user_update', args=[self.id]), data=self.user)
        self.assertEqual(response.status_code, 302)

    def test_user_update_post_correct_content(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.post(reverse('user_update', args=[self.id]), data=self.user, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User updated successfully!')
        self.assertContains(response, self.user['username'])

    def test_user_update_post_incorrect(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.post(reverse('user_update', args=[self.id]), data=self.user_incorrect_un)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Something went wrong. Please check the entered data")
        self.assertContains(response, _('Update'))

    # testing user delete view
    def test_user_delete_post_not_logged_in(self):
        response = self.client.get(reverse('user_delete', args=[self.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('You must login to be able to delete your profile'))

    def test_user_delete_get(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.get(reverse('user_delete', args=[self.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('delete'))

    def test_user_delete_get_wrong_user(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.get(reverse('user_delete', args=[self.wrong_id]))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.get(reverse('user_delete', args=[self.wrong_id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Sorry, you don&#x27;t have permissions to delete other users&#x27; data"))

    def test_user_delete_post_wrong_user(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.post(reverse('user_delete', args=[self.wrong_id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Sorry, you don&#x27;t have permissions to delete other users&#x27; data"))

    def test_user_delete_post_correct_code(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.post(reverse('user_delete', args=[self.id]))
        self.assertEqual(response.status_code, 302)

    def test_user_delete_post_correct_content(self):
        response = self.client.post(reverse('user_login'), data=self.login_data, follow=True)
        response = self.client.post(reverse('user_delete', args=[self.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('User deleted successfully!'))
        self.assertNotContains(response, self.user['username'])
