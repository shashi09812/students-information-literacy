# Information Literacy Learning Effect Predictor

A professional pedagogical platform designed to evaluate and predict the learning outcomes of college students based on their information literacy behaviors. This system empowers mentors with data-driven insights using advanced analytical models.

## 🚀 Features

- **Mentor Ecosystem**: Secure authentication layer with multi-mentor data isolation.
- **Advanced Analytics**: Utilizes specialized models (Random Forest, Neural Networks, etc.) with >92% accuracy.
- **Professional Dashboard**: Abstracted, user-friendly metrics focused on Study Time, Quizzes, and Pre-test success.
- **History & Tracking**: Mentors can save, track, and analyze student performances over time.
- **PostgreSQL Powered**: High-performance, production-ready data storage.

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL 15 / SQLAlchemy
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Frontend**: TailwindCSS, Vanilla JavaScript
- **Automation**: Batch scripting for one-click startup and updates.

## 📦 Setup Instructions

### 1. Prerequisites
- Python 3.10+
- PostgreSQL 15 installed locally.
- Git

### 2. Database Configuration
1. Open PostgreSQL and create a database named `info_literacy_db`.
2. Ensure you have the `postgres` user credentials.

### 3. Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/shashi09812/students-information-literacy.git
   cd students-information-literacy
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your Environment:
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/info_literacy_db
   ```

### 4. Running the Project
The project comes with a built-in automation script for Windows users:
- Double-click **`start_platform.bat`**.
  
This script will:
1. Automatically pull the latest updates from GitHub.
2. Install/Update dependencies.
3. Verify or re-train analytical models.
4. Launch the platform at `http://localhost:5000`.

## 👩‍🏫 Mentor Access
- **Landing Page**: View project usage and functionality.
- **Signup/Login**: Register as a mentor to access your private dashboard.
- **Assessment**: Input student metrics and view professional breakdown reports.

## 📄 License
This project is developed for pedagogical research purposes. 

---
*Empowering education through predictive analytics.*
