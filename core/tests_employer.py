from django.test import TestCase
from django.urls import reverse
from .models import User, Internship, Application

class EmployerTests(TestCase):
    def setUp(self):
        self.employer_user = User.objects.create_user(username='employer', password='password', role='employer')
        self.student_user = User.objects.create_user(username='student', password='password', role='student')
        
    def test_employer_dashboard_access(self):
        self.client.login(username='employer', password='password')
        response = self.client.get(reverse('employer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Employer Dashboard")

    def test_employer_create_internship(self):
        self.client.login(username='employer', password='password')
        response = self.client.post(reverse('employer_create_internship'), {
            'title': 'Test Internship',
            'company': 'Test Co',
            'deadline': '2026-12-31',
            'description': 'Test description',
            'requirements': 'Test requirements'
        })
        self.assertEqual(response.status_code, 302) # Redirect to dashboard
        self.assertTrue(Internship.objects.filter(title='Test Internship', employer=self.employer_user).exists())

    def test_employer_only_sees_own_internships(self):
        # Create internship for another employer
        other_employer = User.objects.create_user(username='other', password='password', role='employer')
        Internship.objects.create(title='Other Job', company='Other Co', deadline='2026-12-31', employer=other_employer)
        
        # Current employer posts one
        Internship.objects.create(title='My Job', company='My Co', deadline='2026-12-31', employer=self.employer_user)
        
        self.client.login(username='employer', password='password')
        response = self.client.get(reverse('employer_dashboard'))
        self.assertContains(response, "My Job")
        self.assertNotContains(response, "Other Job")

    def test_employer_update_application_status(self):
        internship = Internship.objects.create(title='Job', company='Co', deadline='2026-12-31', employer=self.employer_user)
        application = Application.objects.create(user=self.student_user, internship=internship, status='Applied')
        
        self.client.login(username='employer', password='password')
        response = self.client.post(reverse('employer_update_application_status', args=[application.pk]), {
            'status': 'Accepted'
        })
        self.assertEqual(response.status_code, 302)
        application.refresh_from_db()
        self.assertEqual(application.status, 'Accepted')
