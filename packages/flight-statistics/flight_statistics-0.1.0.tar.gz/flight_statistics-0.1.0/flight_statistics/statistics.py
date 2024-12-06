class FlightStatistics:
    def __init__(self, flights):
        self.flights = flights

    def total_flights(self):
        return len(self.flights)

    def average_price(self):
        if not self.flights:
            return 0
        total_price = sum(flight['price'] for flight in self.flights)
        return total_price / len(self.flights)