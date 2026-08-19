📱 QR Complaint Management System

A QR-based Complaint Management System designed to make complaint reporting easier, faster, and more transparent in a college/campus environment.

Students can scan a QR code placed at a specific location, log in, submit a complaint with optional image evidence, and track its status. Administrators can manage QR codes, students, complaints, replies, and resolutions through an admin dashboard.

🚀 Project Overview

Traditional complaint systems often require students to manually contact staff or submit paper-based complaints.

This project provides a digital, location-based complaint system where each QR code represents a specific campus location.

🔄 Basic Workflow
Admin Generates QR Code
        ↓
QR Code Placed at Location
        ↓
Student Scans QR Code
        ↓
Complaint Portal Opens
        ↓
Student Login / Registration
        ↓
Student Submits Complaint
        ↓
Complaint Stored in Database
        ↓
Admin Reviews Complaint
        ↓
Admin Replies / Updates Status
        ↓
Student Tracks Complaint
        ↓
Complaint Resolved
✨ Features
👨‍🎓 Student Features
🔐 Student registration and login
📷 QR code-based complaint access
📍 Location-specific complaints
📝 Complaint submission
🖼️ Optional image upload
📋 View submitted complaints
🔄 Track complaint status
💬 View admin replies
📊 Complaint history
👨‍💻 Admin Features
🔑 Secure admin login
📱 Generate QR codes for locations
👥 Add and manage students
👨‍💼 Manage admin accounts
📋 View all complaints
🔎 View complaint details
💬 Reply to complaints
🔄 Update complaint status
✅ Resolve/close complaints
📊 Dashboard statistics
👥 View total student count
🏗️ System Architecture

                    ┌──────────────────┐
                    │      ADMIN       │
                    │                  │
                    │ Generate QR Code │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    QR CODE       │
                    │ Campus Location  │
                    └────────┬─────────┘
                             │
                       Scan QR Code
                             │
                             ▼
                    ┌──────────────────┐
                    │ STUDENT PORTAL   │
                    │                  │
                    │ Login/Register   │
                    │ Submit Complaint │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     DATABASE     │
                    │                  │
                    │ Users            │
                    │ Complaints       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  ADMIN DASHBOARD │
                    │                  │
                    │ Review           │
                    │ Reply            │
                    │ Update Status    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     STUDENT      │
                    │ Track Status     │
                    │ View Admin Reply │
                    └──────────────────┘
🗄️ Database Structure

The system uses a database to manage users and complaints.

users
Field	Description
id	Primary key
name	Student/Admin name
gender	Gender
student_class	Student class
roll_no	Roll number
id_card	Unique ID card number
password	User password
role	Student/Admin
status	Account status
complaints
Field	Description
id	Complaint ID
student_id	Student who submitted complaint
location	Complaint location
complaint	Complaint description
image	Uploaded image
status	Open / In Progress / Resolved
reply	Admin response
created_at	Complaint creation time
📊 Complaint Status

The complaint follows a simple status lifecycle:

🟠 OPEN
   ↓
🔵 IN PROGRESS
   ↓
🟢 RESOLVED

The student can check the current status from My Complaints.

📱 Example Use Case

Imagine a student finds that a ceiling fan is not working in Computer Lab 2.

Student
Scans the QR code installed in Computer Lab 2.
Complaint portal opens.
Student logs in.
Location is identified as Computer Lab 2.
Student enters the complaint.
Student uploads a photo of the faulty fan.
Complaint is submitted.
Admin
Admin receives the complaint.
Admin views the complaint from the dashboard.
Admin assigns/reviews the issue.
Admin changes the status to In Progress.
Admin adds a reply.
After the issue is fixed, status becomes Resolved.
Student

The student opens My Complaints and sees:

Complaint #101
Location: Computer Lab 2
Issue: Fan not working

Status: ✅ Resolved

Admin Reply:
Technician has fixed the fan.
🛠️ Technologies

Depending on the implementation/version of the project, the system can be built using:

Python
Flask
HTML5
CSS3
JavaScript
SQLite
QR Code Generation
Image Upload
Session-based Authentication
📂 Suggested Project Structure
QR-Complaint-System/
│
├── app.py
├── database.db
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── complaint.html
│   ├── my_complaints.html
│   ├── admin_dashboard.html
│   ├── students.html
│   └── qr_generator.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── uploads/
│
├── qr_codes/
│
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/QR-Complaint-System.git
cd QR-Complaint-System
2. Create a virtual environment
python -m venv venv
3. Activate the environment

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Run the application
python app.py

Open the application in your browser:

http://127.0.0.1:5000
🔐 Security Considerations

For a production deployment, the project should include:

Password hashing instead of storing plain-text passwords
Proper session management
Input validation
File upload validation
Secure filename handling
CSRF protection
Role-based access control
Database backups
Secure environment variables

Note: The GitHub version should not contain real student passwords, personal information, or production credentials.

🎯 Future Improvements

Possible future upgrades include:

📧 Email notifications
🔔 Real-time complaint notifications
📱 Android/mobile application
📊 Advanced analytics
🧑‍🔧 Staff/technician assignment
⏱️ Complaint resolution time tracking
📍 Interactive campus map
🔔 Push notifications
🔐 OTP authentication
☁️ Cloud database integration
🌐 Online deployment
📈 Monthly complaint reports
🤖 AI-based complaint categorization
🎓 Learning Outcomes

Through this project, I learned about:

Web application development
Backend development with Flask
Database design and SQL
Authentication and authorization
CRUD operations
QR code integration
File/image handling
Admin dashboard development
Session management
Connecting frontend and backend
Designing a real-world problem-solving application
📸 Project Preview

Add your project screenshots here:

![Student Portal](screenshots/student-portal.png)

![Complaint Form](screenshots/complaint-form.png)

![Admin Dashboard](screenshots/admin-dashboard.png)

![System Workflow](screenshots/system-workflow.png)
👨‍💻 Developer

Karan Tukaram Bhalerao

BCA Graduate | Software & Web Development Enthusiast

Interested in:

💻 Software Development
🌐 Web Development
🤖 AI & Automation
🗄️ Database Systems
🚀 Building practical projects
⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

📄 License

This project is created for educational and portfolio purposes. Add an appropriate open-source license if you plan to distribute or modify it publicly.
