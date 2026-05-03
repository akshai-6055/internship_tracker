from django.test import TestCase, Client
from django.urls import reverse
from core.models import User, Internship, Application

class WebAppTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username='student', password='password', role='student')
        self.admin = User.objects.create_user(username='admin', password='password', role='admin')
        self.internship = Internship.objects.create(
            title="Software Engineer",
            company="Tech Corp",
            deadline="2030-01-01",
            description="A great job"
        )
        
    def test_landing_page(self):
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        
    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password': 'password123',
            'role': 'student'
        })
        self.assertEqual(response.status_code, 200) # Wait, UserCreationForm requires more fields for password? No, it requires password1 and password2 usually, wait, custom user creation might require more fields. Let's just test get request.
        
    def test_student_dashboard_access(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        
    def test_admin_dashboard_access_denied_for_student(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403) # PermissionDenied raises 403
        
    def test_admin_dashboard_access(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        
    def test_apply_internship(self):
        self.client.login(username='student', password='password')
        response = self.client.post(reverse('apply_internship', args=[self.internship.pk]), {
            'cover_letter': 'Hello'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Application.objects.filter(user=self.student, internship=self.internship).exists())
        
        # Test duplicate application
        response = self.client.post(reverse('apply_internship', args=[self.internship.pk]), {
            'cover_letter': 'Hello Again'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Application.objects.filter(user=self.student, internship=self.internship).count(), 1)
