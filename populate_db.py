import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_project.settings')
django.setup()

from core.models import User, Internship, Application

def populate():
    print("Clearing existing data...")
    Application.objects.all().delete()
    Internship.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    print("Creating users...")
    # Admin User
    admin, _ = User.objects.get_or_create(username='admin', defaults={'role': 'admin'})
    admin.set_password('password')
    admin.save()
    
    # Students
    student1, _ = User.objects.get_or_create(username='student1', defaults={'role': 'student', 'first_name': 'Alice'})
    student1.set_password('password')
    student1.save()

    student2, _ = User.objects.get_or_create(username='student2', defaults={'role': 'student', 'first_name': 'Bob'})
    student2.set_password('password')
    student2.save()

    print("Creating internships...")
    internships = [
        Internship(
            title="Software Engineering Intern",
            company="Tech Giants Inc.",
            deadline=datetime.now() + timedelta(days=30),
            description="Work on scalable backend services using Python and Django.",
            requirements="Familiarity with Python, SQL, and REST APIs."
        ),
        Internship(
            title="Data Science Intern",
            company="DataCorp",
            deadline=datetime.now() + timedelta(days=45),
            description="Analyze large datasets to extract meaningful insights.",
            requirements="Python, Pandas, Machine Learning basics."
        ),
        Internship(
            title="Frontend Developer Intern",
            company="WebMakers",
            deadline=datetime.now() + timedelta(days=15),
            description="Create beautiful, responsive user interfaces using React.",
            requirements="HTML, CSS, JavaScript, React."
        ),
        Internship(
            title="Cybersecurity Analyst Intern",
            company="SecureNet",
            deadline=datetime.now() + timedelta(days=60),
            description="Help secure our internal networks and perform vulnerability assessments.",
            requirements="Basic understanding of network security protocols."
        ),
    ]
    Internship.objects.bulk_create(internships)
    
    # Fetch them back to get IDs
    i1 = Internship.objects.get(title="Software Engineering Intern")
    i2 = Internship.objects.get(title="Data Science Intern")
    i3 = Internship.objects.get(title="Frontend Developer Intern")

    print("Creating applications...")
    applications = [
        Application(
            user=student1,
            internship=i1,
            cover_letter="I am very interested in backend development.",
            status="Applied"
        ),
        Application(
            user=student1,
            internship=i2,
            cover_letter="Data science is my passion.",
            status="Pending"
        ),
        Application(
            user=student2,
            internship=i1,
            cover_letter="I have strong Python skills.",
            status="Accepted"
        ),
        Application(
            user=student2,
            internship=i3,
            cover_letter="I love building UI.",
            status="Rejected"
        )
    ]
    Application.objects.bulk_create(applications)

    print("Database successfully populated!")
    print("\n--- Created Credentials ---")
    print("Admin:")
    print("  Username: admin")
    print("  Password: password")
    print("\nStudents:")
    print("  Username: student1")
    print("  Password: password")
    print("  Username: student2")
    print("  Password: password")

if __name__ == '__main__':
    populate()
