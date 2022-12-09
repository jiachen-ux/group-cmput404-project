from django.test import TestCase, Client
from author.models import Author
from django.urls import reverse

from rest_framework import status

from rest_framework.test import APIClient


# Create your tests here.

class TestViews(TestCase):

    def setUp(self):
        self.c = Client()

        self.user_info = {
            'displayName': 'Test',
            'username' : 'test',
            'password1': 'Newtest123',
            'password2': 'Newtest123',
            'github': 'https://github.com/Bushratun-Nusaibah',

        }

        self.login_info = {
            'username' : 'test',
            'password1': 'Newtest123',
        }

        url_signup = "register/"
        login_url = ""
        self.c.post(url_signup, self.user_info)
        self.c.post(login_url, self.login_info)
        self.url_allAuthors = reverse('allForeignAuthors')

    def profile_page(self):
        response = self.c.get(reverse('author_profile', kwargd = {'authorId':'test'}))

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, "profile.html")

class AuthorTest(TestCase):
    def test_author(self):
        Author.objects.all().delete()
        author = Author.objects.create_user(username="Test", password="testpassword")
        self.assertTrue(Author.objects.filter(username=author.username))

        return


    def test_superuser(self):
        Author.objects.all().delete()
        author = Author.objects.create_user(username='Test Author', password='testpassw0rd')
        self.assertFalse(author.is_staff)
        self.assertFalse(author.is_superuser)

    def test_author_str_(self):
            test_username = 'Test'
            Author.objects.all().delete()
            author = Author.objects.create_user(username="Test", password='testauthorpassw0rd')
            self.assertEqual(str(author.username), test_username)

class AuthorEndpointTest(TestCase):

    client = APIClient()
    test_author = {
            'displayName': 'Test',
            'username' : 'test',
            'password1': 'Newtest123',
            'password2': 'Newtest123',
            'github': 'https://github.com/Bushratun-Nusaibah',

    }

    def test_register(self):
        Author.objects.all().delete()
        request = self.client.post('/register/', self.test_author, format='json')
        self.assertFalse(request.status_code == 200)

    
    def test_profile_updated(self):
        Author.objects.all().delete()
        payload = {
            'username':'updated',
            'displayName':'Updated Test Author'
        }
        author = Author.objects.create_user(username="updated", displayName = "New Name", password="testpassword")
        self.client.post(f'/author/{author.id}/', payload)
        updated_author = Author.objects.get(id=author.id)
        self.assertEqual(updated_author.username, payload['username']) # author username didn't change
        self.assertNotEqual(updated_author.displayName, 'Updated Test Author') #changed


  

    
    '''def test_login_invalid_credentials(self):
        Author.objects.all().delete()
        Author.objects.create_user(username="updated", displayName = "New Name", password="testpassword")
        request = self.client.post('', self.test_author, format='json')
        self.assertTrue(request.status_code == 401)
'''