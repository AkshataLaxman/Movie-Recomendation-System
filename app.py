import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'AIzaSyCDP41yeNITJz3ahy7cvwldmvm7Lv0afjg'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/images')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# List of Indian cities
INDIAN_CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata',
    'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Kochi', 'Indore'
]

# Theater model
class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    classic_price = db.Column(db.Float, nullable=False, default=500.0)
    premium_price = db.Column(db.Float, nullable=False, default=1000.0)

# Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    showtimes = db.Column(db.String(200), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    poster_url = db.Column(db.String(200), nullable=False)
    theater = db.relationship('Theater', backref='movies')

# User model for customers (removed otp and is_verified)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seat_ids = db.Column(db.String(200), nullable=False)
    showtime = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    movie = db.relationship('Movie', backref='bookings')
    user = db.relationship('User', backref='bookings')

# Admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Recommendation search model
class RecommendationSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), nullable=False)
    recommended_movies = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Create database and seed data
with app.app_context():
    db.create_all()
    if not Theater.query.first():
        theaters = [
            Theater(name="PVR Orion Mall", location="Bangalore", classic_price=500.0, premium_price=1000.0),
            Theater(name="INOX South City", location="Kolkata", classic_price=500.0, premium_price=1000.0),
            Theater(name="PVR Ambience Mall", location="Delhi", classic_price=500.0, premium_price=1000.0),
            Theater(name="Cinepolis Viviana Mall", location="Mumbai", classic_price=500.0, premium_price=1000.0),
            Theater(name="Sathyam Cinemas", location="Chennai", classic_price=500.0, premium_price=1000.0),
            Theater(name="PVR Banjara Hills", location="Hyderabad", classic_price=500.0, premium_price=1000.0),
            Theater(name="INOX Amanora Mall", location="Pune", classic_price=500.0, premium_price=1000.0),
            Theater(name="PVR SG Highway", location="Ahmedabad", classic_price=500.0, premium_price=1000.0),
        ]
        db.session.bulk_save_objects(theaters)
        db.session.commit()
    
    if not Movie.query.first():
        theaters = Theater.query.all()
        movies = [
            Movie(
                title="Inception",
                genre="Sci-Fi, Thriller",
                showtimes="4:00 PM,7:00 PM,10:00 PM",
                theater_id=theaters[0].id,  # Bangalore
                poster_url="images/inception.jpg"
            ),
            Movie(
                title="The Dark Knight",
                genre="Action, Thriller",
                showtimes="5:00 PM,8:00 PM,11:00 PM",
                theater_id=theaters[1].id,  # Kolkata
                poster_url="images/dark_knight.jpg"
            ),
            Movie(
                title="La La Land",
                genre="Romance, Musical",
                showtimes="3:00 PM,6:00 PM,9:00 PM",
                theater_id=theaters[2].id,  # Delhi
                poster_url="images/lalaland.jpg"
            ),
            Movie(
                title="Interstellar",
                genre="Sci-Fi, Adventure",
                showtimes="6:00 PM,9:00 PM,12:00 AM",
                theater_id=theaters[3].id,  # Mumbai
                poster_url="images/interstellar.jpg"
            ),
            Movie(
                title="Dangal",
                genre="Drama, Sports",
                showtimes="2:00 PM,5:00 PM,8:00 PM",
                theater_id=theaters[4].id,  # Chennai
                poster_url="images/dangal.jpg"
            ),
            Movie(
                title="Baahubali",
                genre="Action, Drama",
                showtimes="3:00 PM,6:00 PM,9:00 PM",
                theater_id=theaters[5].id,  # Hyderabad
                poster_url="images/baahubali.jpg"
            ),
            Movie(
                title="3 Idiots",
                genre="Comedy, Drama",
                showtimes="4:00 PM,7:00 PM,10:00 PM",
                theater_id=theaters[6].id,  # Pune
                poster_url="images/3idiots.jpg"
            ),
            Movie(
                title="Gujarati Natak",
                genre="Drama, Comedy",
                showtimes="5:00 PM,8:00 PM,11:00 PM",
                theater_id=theaters[7].id,  # Ahmedabad
                poster_url="images/gujarati_natak.jpg"
            ),
        ]
        db.session.bulk_save_objects(movies)
        db.session.commit()
    
    if not Admin.query.first():
        admin = Admin(username="admin", password_hash=generate_password_hash("admin123"))
        db.session.add(admin)
        db.session.commit()

# Check if user is admin
def is_admin():
    return session.get('admin_logged_in', False)

# Check if user is logged in
def is_user_logged_in():
    return session.get('user_id') is not None

# User registration (simplified, no OTP)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_user_logged_in():
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# User login (redirect to city selection after login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_user_logged_in():
        if 'selected_city' in session:
            return redirect(url_for('index'))
        return redirect(url_for('select_city'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Logged in successfully! Please select your city.', 'success')
            return redirect(url_for('select_city'))
        flash('Invalid username or password.', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

# City selection route
@app.route('/select_city', methods=['GET', 'POST'])
def select_city():
    if not is_user_logged_in():
        flash('Please log in to select a city.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        city = request.form['city']
        if city in INDIAN_CITIES:
            session['selected_city'] = city
            return redirect(url_for('index'))
        flash('Please select a valid city.', 'error')
        return redirect(url_for('select_city'))
    
    return render_template('select_city.html', cities=INDIAN_CITIES)

# User logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('selected_city', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

# Homepage (filter by selected city)
@app.route('/')
def index():
    if not is_user_logged_in():
        flash('Please log in to access the movie booking system.', 'error')
        return redirect(url_for('login'))
    
    if 'selected_city' not in session:
        flash('Please select a city to view theaters.', 'error')
        return redirect(url_for('select_city'))
    
    city = session['selected_city']
    theaters = Theater.query.filter_by(location=city).all()
    movies = Movie.query.filter(Movie.theater.has(location=city)).all()
    return render_template('index.html', movies=movies, theaters=theaters, selected_city=city)

# Recommend movies (filter by selected city)
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if not is_user_logged_in():
        flash('Please log in to access recommendations.', 'error')
        return redirect(url_for('login'))
    
    if 'selected_city' not in session:
        flash('Please select a city to view recommendations.', 'error')
        return redirect(url_for('select_city'))
    
    city = session['selected_city']
    if request.method == 'POST':
        genre = request.form['genre']
        recommended_movies = Movie.query.filter(
            Movie.genre.ilike(f'%{genre}%'),
            Movie.theater.has(location=city)
        ).all()
        if recommended_movies:
            movie_titles = ",".join([movie.title for movie in recommended_movies])
            search_entry = RecommendationSearch(
                genre=genre,
                recommended_movies=movie_titles
            )
            db.session.add(search_entry)
            db.session.commit()
        return render_template('recommend.html', movies=recommended_movies)
    return render_template('recommend.html', movies=[])

# Get booked seats for a movie and showtime
@app.route('/get_booked_seats/<int:movie_id>/<showtime>')
def get_booked_seats(movie_id, showtime):
    if not is_user_logged_in():
        return jsonify({'error': 'Please log in to access this resource.'}), 401
    bookings = Booking.query.filter_by(movie_id=movie_id, showtime=showtime).all()
    booked_seats = []
    for booking in bookings:
        booked_seats.extend(booking.seat_ids.split(','))
    return jsonify(booked_seats)

# Booking (require user login)
@app.route('/book/<int:movie_id>', methods=['GET', 'POST'])
def book(movie_id):
    if not is_user_logged_in():
        flash('Please log in to book a movie.', 'error')
        return redirect(url_for('login'))
    
    if 'selected_city' not in session:
        flash('Please select a city to book a movie.', 'error')
        return redirect(url_for('select_city'))
    
    movie = Movie.query.get_or_404(movie_id)
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        seat_ids = request.form['seat_ids']
        showtime = request.form['showtime']
        total_price = float(request.form['total_price'])
        
        booked_seats = Booking.query.filter_by(movie_id=movie_id, showtime=showtime).all()
        booked_seat_list = []
        for booking in booked_seats:
            booked_seat_list.extend(booking.seat_ids.split(','))
        selected_seats = seat_ids.split(',')
        if any(seat in booked_seat_list for seat in selected_seats):
            flash('One or more selected seats are already booked.', 'error')
            return redirect(url_for('book', movie_id=movie_id))
        
        booking = Booking(
            movie_id=movie.id,
            user_id=user.id,
            seat_ids=seat_ids,
            showtime=showtime,
            total_price=total_price
        )
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('confirmation', booking_id=booking.id))
    return render_template('booking.html', movie=movie, user=user)

# Booking confirmation (require login)
@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    if not is_user_logged_in():
        flash('Please log in to view your booking.', 'error')
        return redirect(url_for('login'))
    
    if 'selected_city' not in session:
        flash('Please select a city to view your booking.', 'error')
        return redirect(url_for('select_city'))
    
    booking = Booking.query.get_or_404(booking_id)
    movie = Movie.query.get(booking.movie_id)
    user = User.query.get(session['user_id'])
    if booking.user_id != user.id:
        flash('You are not authorized to view this booking.', 'error')
        return redirect(url_for('index'))
    return render_template('confirmation.html', booking=booking, movie=movie)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('admin_login'))
    movies = Movie.query.all()
    return render_template('admin/dashboard.html', movies=movies)

@app.route('/admin/add_movie', methods=['GET', 'POST'])
def add_movie():
    if not is_admin():
        return redirect(url_for('admin_login'))
    theaters = Theater.query.all()
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        showtimes = request.form['showtimes']
        theater_id = request.form['theater_id']
        
        if 'poster' not in request.files:
            flash('No file part in the request.', 'error')
            return redirect(url_for('add_movie'))
        file = request.files['poster']
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('add_movie'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            base, extension = os.path.splitext(filename)
            counter = 1
            while os.path.exists(file_path):
                filename = f"{base}_{counter}{extension}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                counter += 1
            file.save(file_path)
            poster_url = f"images/{filename}"
        else:
            flash('Invalid file type. Allowed types: jpg, jpeg, png.', 'error')
            return redirect(url_for('add_movie'))
        
        movie = Movie(
            title=title,
            genre=genre,
            showtimes=showtimes,
            theater_id=theater_id,
            poster_url=poster_url
        )
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_movie.html', theaters=theaters)

@app.route('/admin/remove_movie/<int:movie_id>')
def remove_movie(movie_id):
    if not is_admin():
        return redirect(url_for('admin_login'))
    movie = Movie.query.get_or_404(movie_id)
    poster_path = os.path.join(basedir, 'static', movie.poster_url)
    if os.path.exists(poster_path):
        os.remove(poster_path)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie removed successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/view_recommendations', methods=['GET', 'POST'])
def view_recommendations():
    if not is_admin():
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        genre = request.form['genre']
        recommended_movies = Movie.query.filter(Movie.genre.ilike(f'%{genre}%')).all()
        return render_template('admin/view_recommendations.html', movies=recommended_movies)
    return render_template('admin/view_recommendations.html', movies=[])

@app.route('/admin/customer_recommendations')
def customer_recommendations():
    if not is_admin():
        return redirect(url_for('admin_login'))
    searches = RecommendationSearch.query.order_by(RecommendationSearch.timestamp.desc()).all()
    return render_template('admin/customer_recommendations.html', searches=searches)

@app.route('/admin/manage_seat_prices', methods=['GET', 'POST'])
def manage_seat_prices():
    if not is_admin():
        return redirect(url_for('admin_login'))
    theaters = Theater.query.all()
    if request.method == 'POST':
        for theater in theaters:
            theater.classic_price = float(request.form[f'classic_price_{theater.id}'])
            theater.premium_price = float(request.form[f'premium_price_{theater.id}'])
        db.session.commit()
        flash('Seat prices updated successfully', 'success')
        return redirect(url_for('manage_seat_prices'))
    return render_template('admin/manage_seat_prices.html', theaters=theaters)

if __name__ == '__main__':
    app.run(debug=True)