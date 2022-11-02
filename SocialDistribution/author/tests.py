from django.test import TestCase
from author.models import Author

from rest_framework.test import APIClient


# Create your tests here.

class AuthorTest(TestCase):
    def test_create_author(self):
        Author.objects.all().delete()
        author = Author.objects.create_user(username="Test", password="testpassword")
        self.assertTrue(Author.objects.filter(username=author.username))

        return


    def test_create_superuser(self):
        Author.objects.all().delete()
        author = Author.objects.create_user(username='Test Author', password='testpassw0rd')
        self.assertFalse(author.is_staff)
        self.assertFalse(author.is_superuser)

    def test_author_str_(self):
            test_username = 'Test'
            Author.objects.all().delete()
            author = Author.objects.create_user(username="Test", password='testauthorpassw0rd')
            self.assertEqual(str(author.username), test_username)


class AuthorAPITest(TestCase):

    user_client = APIClient()

    test_author = {
        "username": "Test",
        "password": "testpassword",
    }

    def test_register(self):
        Author.objects.all().delete()
        request = self.user_client.post('/register/', self.test_author, format='json')
        self.assertTrue(request.status_code == 200)

    def test_login(self):
        Author.objects.all().delete()
        Author.objects.create_user(username="Test", password='testpassword')
        request = self.user_client.post('/login/', self.test_author, format='json')
        self.assertTrue(request.status_code == 200)

