# 🌍 Smart Trip Planner

A web-based travel planning web application developed using **Python and Django** that helps users plan trips, explore destinations, book hotels and vehicles, manage bookings, and calculate travel expenses.

## 📌 Project Overview

Smart Trip Planner is designed to simplify travel planning through a single web application. Users can register, log in, browse destinations, explore available hotels and vehicles, make bookings, and view their booking details.

The system also provides an administration interface to manage travel-related information and monitor bookings and user feedback.

## ✨ Features

- **User Authentication:** User registration and login.
- **Destination Management:** Browse destinations such as Goa, Manali, Kashmir, and Jaipur.
- **Places to Visit:** Explore tourist attractions associated with destinations.
- **Hotel Booking:** View hotels, prices, and room availability.
- **Vehicle Booking:** Select vehicles based on type, seating capacity, and price per kilometre.
- **Trip Cost Calculation:** Calculate vehicle costs based on destination distance and vehicle rate.
- **Booking Management:** View booking details, travel dates, and booking status.
- **User Profile:** Manage personal details and profile photo.
- **Feedback and Ratings:** Submit feedback and rate the travel experience.
- **Admin Management:** Manage destinations, hotels, vehicles, bookings, and feedback.
- **Booking Reports:** Generate booking reports for a selected date range.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web application framework |
| HTML5 | Page structure |
| CSS3 | Styling and responsive layouts |
| JavaScript | Client-side interactions |
| MySQL | Database |

## Project Modules

1. **Destination Module** – Destination details and tourist attractions.
2. **Hotel Module** – Hotel information, pricing, and room booking.
3. **Vehicle Module** – Vehicle selection and travel-cost calculation.
4. **Booking Module** – Trip booking, dates, and booking summaries.
5. **Profile Module** – User details and profile management.
6. **Admin Module** – Management of travel information and reports.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.9 or a compatible version
- pip
- Git
- A code editor such as Visual Studio Code

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Smart-Trip-Planner.git
cd Smart-Trip-Planner
```

Replace `YOUR-USERNAME` with your GitHub username and adjust the repository name if needed.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

If your project contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```


### Step 4: Configure the Database

Check `settings.py` and configure the database according to your project setup. For a new SQLite database, the default Django configuration is generally sufficient.

If using MySQL, create the database and configure the connection settings before proceeding.

### Step 5: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create an Administrator

```bash
python manage.py createsuperuser
```

Follow the prompts to set the administrator username and password.

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

## 🖥️ How to Use

1. Register a new user account.
2. Log in to the application.
3. Browse the available travel destinations.
4. Explore hotels and vehicles.
5. Select your travel dates and booking preferences.
6. Review the booking summary and total estimated cost.
7. View your booking details.
8. Submit feedback after using the application.

Administrators can use the available management interface to maintain travel information and review bookings.

## 🗄️ Database Design

The project uses Django models to store and manage application data. The main entities include:

- **Destination:** Destination name, description, distance, and type.
- **PlaceToVisit:** Tourist attractions associated with destinations.
- **Hotel:** Hotel details, room information, pricing, and destination.
- **Vehicle:** Vehicle type, seating capacity, and per-kilometre rate.
- **Booking:** User, destination, vehicle, hotel, travel dates, and total amount.
- **UserProfile:** Additional user information and profile photo.
- **Feedback:** User ratings, comments, and submission date.

The exact tables and field names may vary according to the implemented models.

## 🔐 Security Notes

- Do not upload passwords, API keys, database credentials, or secret keys.
- Keep production secrets in environment variables.
- Do not commit your local database if it contains personal or sensitive data.

## 🚀 Future Enhancements

- Integration with maps and route planning.
- Weather forecasts for selected destinations.
- AI-based destination recommendations.
- Online payment gateway integration.
- Email and SMS booking notifications.


## 👨‍💻 Author

**Your Name**

GitHub: https://github.com/Rohini-Patil14

