from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from views import Student





# Create your tests here.
class ReviewIndexViewTests(TestCase):

    def setUp(self):
        Student.objects.create(major="12", pronoun="1", year="2018", phone_number="9196272390", netid="su26", id="11111", username='sarp', name="Sarp Uner")
        self.user = User.objects.create_user(username='sarp', email='sarpim@gmail.com', password='top_secret')

    def test_no_reviews(self):
        # If no dinners to review, appropriate message is displayed!
        self.client.force_login(self.user)
        response = self.client.get(reverse('reviewIndex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No reviews needed")
        self.assertQuerysetEqual(response.context['available_reviews'], [])
