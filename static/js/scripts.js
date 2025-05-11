document.addEventListener('DOMContentLoaded', () => {
    console.log('Scripts loaded');

    // Booking form seat selection
    const bookingForm = document.querySelector('#booking-form');
    if (bookingForm) {
        console.log('Booking form found');
        const seats = document.querySelectorAll('.seat');
        const seatIdsInput = document.querySelector('#seat_ids');
        const totalPriceInput = document.querySelector('#total_price');
        const totalPriceDisplay = document.querySelector('#total-price-display');
        const showtimeSelect = document.querySelector('#showtime');
        const movieId = bookingForm.action.match(/\/book\/(\d+)/)?.[1];

        if (!movieId) {
            console.error('Movie ID not found in form action');
            return;
        }
        if (!seats.length) {
            console.error('No seats found in seat selection grid');
            return;
        }
        if (!totalPriceInput || !totalPriceDisplay) {
            console.error('Total price elements not found');
            return;
        }

        let selectedSeats = [];

        // Fetch booked seats
        function fetchBookedSeats() {
            const showtime = showtimeSelect.value;
            console.log(`Fetching booked seats for movie ${movieId}, showtime ${showtime}`);
            fetch(`/get_booked_seats/${movieId}/${encodeURIComponent(showtime)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(bookedSeats => {
                    console.log('Booked seats:', bookedSeats);
                    seats.forEach(seat => {
                        const seatId = seat.dataset.seat;
                        if (bookedSeats.includes(seatId)) {
                            seat.classList.remove('available', 'selected');
                            seat.classList.add('booked');
                            selectedSeats = selectedSeats.filter(id => id !== seatId);
                        } else {
                            if (!seat.classList.contains('selected')) {
                                seat.classList.add('available');
                            }
                        }
                    });
                    updateSeatIdsAndPrice();
                })
                .catch(error => {
                    console.error('Error fetching booked seats:', error);
                });
        }

        // Update hidden inputs with selected seat IDs and total price
        function updateSeatIdsAndPrice() {
            seatIdsInput.value = selectedSeats.join(',');
            let totalPrice = 0;
            selectedSeats.forEach(seatId => {
                const seat = document.querySelector(`.seat[data-seat="${seatId}"]`);
                if (seat) {
                    const price = parseFloat(seat.dataset.price) || 0;
                    totalPrice += price;
                    console.log(`Seat ${seatId}: ₹${price}`);
                }
            });
            totalPriceInput.value = totalPrice.toFixed(2);
            totalPriceDisplay.textContent = totalPrice.toFixed(2);
            console.log('Selected seats:', selectedSeats, 'Total price: ₹', totalPrice);
        }

        // Handle seat clicks
        seats.forEach(seat => {
            seat.addEventListener('click', () => {
                const seatId = seat.dataset.seat;
                const price = seat.dataset.price;
                console.log(`Seat clicked: ${seatId}, Price: ₹${price}`);
                if (!seat.classList.contains('booked')) {
                    if (seat.classList.contains('selected')) {
                        seat.classList.remove('selected');
                        seat.classList.add('available');
                        selectedSeats = selectedSeats.filter(id => id !== seatId);
                    } else {
                        seat.classList.remove('available');
                        seat.classList.add('selected');
                        selectedSeats.push(seatId);
                    }
                    updateSeatIdsAndPrice();
                }
            });
        });

        // Fetch booked seats on page load and showtime change
        fetchBookedSeats();
        showtimeSelect.addEventListener('change', fetchBookedSeats);

        // Form validation
        bookingForm.addEventListener('submit', (e) => {
            if (!seatIdsInput.value) {
                e.preventDefault();
                alert('Please select at least one seat.');
                console.log('Form submission blocked: No seats selected');
            }
        });
    } else {
        console.warn('Booking form not found');
    }

    // Add movie form validation
    const addMovieForm = document.querySelector('form[action*="/add_movie"]');
    if (addMovieForm) {
        addMovieForm.addEventListener('submit', (e) => {
            const title = document.querySelector('#title').value.trim();
            if (!title) {
                e.preventDefault();
                alert('Movie title is required.');
            }
        });
    }
});