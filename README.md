# InternVault - Internship Tracking Portal

InternVault is a premium, full-stack internship management system designed to bridge the gap between students seeking opportunities and employers looking for talent. Built with Django, it features a modern, responsive user interface with role-based access control for three distinct modules: Student, Employer, and Admin.

## 🚀 Key Modules & Functionalities

### 1. Student (User) Module
Designed for students to discover and apply for internship opportunities seamlessly.
- **Personalized Dashboard:** View applied internships and track their statuses in real-time.
- **Internship Discovery:** Browse a comprehensive list of approved internships with detailed descriptions.
- **Application Management:** 
  - Apply for internships with custom cover letters.
  - Edit submitted applications before they are processed.
  - Withdraw applications if no longer interested.
- **Profile Management:** Secure signup, login, and the ability to delete the account.

### 2. Employer (Company) Module
Empowers companies to manage their recruitment process efficiently.
- **Employer Dashboard:** Overview of posted internships and received applications.
- **Job Posting:** Create, edit, and delete internship listings with specific requirements and deadlines.
- **Applicant Tracking:**
  - View all students who applied for a specific internship.
  - Read cover letters and assess candidates.
  - Update application statuses (Pending, Accepted, Rejected) directly.
- **Company Profile:** Associate postings with a specific company name.

### 3. Admin Module
Provides complete oversight and moderation of the entire platform.
- **Admin Dashboard:** High-level summary of system activity, including total internships and applications.
- **Moderation:** Approve or reject internship postings to ensure quality and legitimacy.
- **Global Management:**
  - Full CRUD (Create, Read, Update, Delete) permissions for all internships.
  - Update any application status.
  - Oversee all user roles and accounts.

---

## ✨ Features & Technologies

- **Role-Based Access Control (RBAC):** Securely separated interfaces for Students, Employers, and Admins.
- **Modern UI/UX:** A premium, dark-themed interface featuring glassmorphism aesthetics and responsive design.
- **Authentication:** Robust user authentication system (Signup/Login/Logout).
- **Backend:** Powered by **Python Django** for a scalable and secure architecture.
- **Database:** Uses **SQLite** (default) with support for MySQL/PostgreSQL.
- **Frontend:** HTML5, CSS3 (Vanilla), and JavaScript with Google Fonts (Inter/Outfit).

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd internship_tracker
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py run_server
   ```

6. **Access the application:**
   Open `http://127.0.0.1:8000` in your browser.

## 👥 Contributors
- **Akshai** (Project Lead & Developer)

---
*Built with ❤️ for a better internship experience.*
