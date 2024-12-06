from .models import Booking

class BookingCounter:
    def __init__(self, user):
        self.user = user

    def count_bookings(self):
        return Booking.objects.filter(user=self.user)
        