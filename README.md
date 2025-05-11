Cross multiple theaters in various Indian cities. The application features both user and admin interfaces with a focus on usability and security.

## 🎬 Features

### User Features
- **User Registration & Authentication**: Secure signup and login system
- **City-based Movie Filtering**: Choose your city to see relevant theaters and movies
- **Genre-based Movie Recommendations**: Find movies based on your preferred genres
- **Interactive Seat Selection**: Visual seat booking interface with real-time availability
- **Booking Management**: View and track your movie bookings
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Admin Features
- **Movie Management**: Add, update, and remove movies from the system
- **Pricing Control**: Manage theater-specific pricing for different seat categories
- **Analytics Dashboard**: Track customer recommendations and preferences
- **User Management**: Monitor bookings and user activities

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLAlchemy with SQLite
- **Security**: Werkzeug security for password hashing
- **Frontend**: HTML, CSS, JavaScript (with templates rendered by Flask)
- **File Handling**: Werkzeug utilities for secure file uploads

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/filmflare.git
   cd filmflare
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   flask db upgrade
   ```

5. **Run the application**
   ```bash
   flask run
   ```

6. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:5000`
   - For admin access, use:
     - Username: `admin`
     - Password: `admin123`

## 📁 Project Structure

```
filmflare/
├── static/
│   ├── css/
│   ├── js/
│   └── images/         # Movie posters and UI assets
├── templates/
│   ├── admin/          # Admin interface templates
│   └── ...             # User interface templates
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## 🎥 Supported Cities

The application currently supports the following Indian cities:
- Mumbai
- Delhi
- Bangalore
- Hyderabad
- Chennai
- Kolkata
- Pune
- Ahmedabad
- Jaipur
- Lucknow
- Kochi
- Indore

## 🔒 Security Features

- Password hashing with Werkzeug
- CSRF protection
- Secure file uploads with extension validation
- Session management
- Authorization checks for protected routes

## 🎭 Sample Movies

The system comes pre-loaded with several popular movies across different genres:
- Inception (Sci-Fi, Thriller)
- The Dark Knight (Action, Thriller)
- La La Land (Romance, Musical)
- Interstellar (Sci-Fi, Adventure)
- Dangal (Drama, Sports)
- Baahubali (Action, Drama)
- 3 Idiots (Comedy, Drama)
- Gujarati Natak (Drama, Comedy)

## 🔍 Future Enhancements

- Payment gateway integration
- Email confirmation for bookings
- User reviews and ratings
- Mobile app integration
- Social media sharing
- Performance analytics for theater owners

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - (https://github.com/AkshatLaxman)

## 🙏 Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Werkzeug Documentation](https://werkzeug.palletsprojects.com/)
