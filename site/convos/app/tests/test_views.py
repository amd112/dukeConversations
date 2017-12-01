from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from app.models import Student, Application, Professor, Dinner

def createDinners():
    profs = list(Professor.objects.all())
    for prof in profs:
        Dinner.objects.create(date_time=timezone.now() + timezone.timedelta(days=-5),
        professor_id=prof, topic="Ultramegachemicobiophysioquantum dynamics",
        description="blah")

    return Dinner.objects.all()

def createApplications_AllSelected():
    students = Student.objects.all()
    dinners = Dinner.objects.all()
    for stud in students:
        for din in dinners:
            Application.objects.create(username=stud, dinner_id=din,
            selected=True, attendance=True, interest="WOOOOW SO INTERESTING!!!")
    return Application.objects.all()

def createProfessor(name, gender="1", food_restriction="Broccoli"):
    return Professor.objects.create(gender=gender, name=name, food_restrictions=food_restriction)





# Create your tests here.
class ReviewIndexViewTests(TestCase):

    def setUp(self):
        Student.objects.create(major="12", pronoun="1", year="2018", phone_number="9196272390", netid="su26", id="11111",
        username='sarp', name="Sarp Uner")
        self.user = User.objects.create_user(username='sarp', email='sarpim@gmail.com', password='top_secret')

    def test_login_protection(self):
        response = self.client.get(reverse('reviewIndex'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_no_reviews(self):
        # If no dinners to review, appropriate message is displayed!
        self.client.force_login(self.user)
        response = self.client.get(reverse('reviewIndex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No reviews needed")
        self.assertQuerysetEqual(response.context['available_reviews'], [])

    def test_with_reviews(self):
        self.client.force_login(self.user)
        createProfessor("Jun Yang")
        createDinners()
        createApplications_AllSelected()
        attended_dinners = Application.objects.filter(username=Student.StudentForUsername(self.user)).filter(selected=True).filter(attendance=True).values('dinner_id')
        response = self.client.get(reverse('reviewIndex'))
        self.assertContains(response, "Please review the dinners below")
        self.assertQuerysetEqual(response.context['available_reviews'], map(repr, attended_dinners))
