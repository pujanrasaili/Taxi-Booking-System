"""
Fare Calculator Module
Calculates taxi fares based on distance, vehicle type, and time
"""

from datetime import datetime


class FareCalculator:
    """Calculate taxi fares with various pricing rules"""
    
    # Base fare by vehicle type (in currency units)
    BASE_FARE = {
        "Sedan": 50,
        "SUV": 80,
        "Hatchback": 40,
        "Van": 100,
        "Bike": 30
    }
    
    # Per kilometer rate by vehicle type
    PER_KM_RATE = {
        "Sedan": 12,
        "SUV": 18,
        "Hatchback": 10,
        "Van": 20,
        "Bike": 8
    }
    
    # Peak hours surcharge (1.5x during 8-10 AM and 5-8 PM)
    PEAK_HOUR_MULTIPLIER = 1.5
    PEAK_HOURS = [(8, 10), (17, 20)]
    
    # Night surcharge (1.3x from 11 PM to 6 AM)
    NIGHT_MULTIPLIER = 1.3
    NIGHT_HOURS = (23, 6)
    
    @staticmethod
    def calculate_fare(distance, vehicle_type, pickup_time=None):
        """
        Calculate total fare for a trip
        
        Args:
            distance (float): Distance in kilometers
            vehicle_type (str): Type of vehicle
            pickup_time (datetime or str): Pickup time for surge pricing
        
        Returns:
            float: Total fare rounded to 2 decimal places
        """
        if distance <= 0:
            return FareCalculator.BASE_FARE.get(vehicle_type, 50)
        
        # Get base fare and per km rate
        base = FareCalculator.BASE_FARE.get(vehicle_type, 50)
        per_km = FareCalculator.PER_KM_RATE.get(vehicle_type, 12)
        
        # Calculate base fare
        fare = base + (distance * per_km)
        
        # Apply time-based multipliers if pickup_time is provided
        if pickup_time:
            multiplier = FareCalculator._get_time_multiplier(pickup_time)
            fare *= multiplier
        
        return round(fare, 2)
    
    @staticmethod
    def _get_time_multiplier(pickup_time):
        """
        Get time-based fare multiplier
        
        Args:
            pickup_time (datetime or str): Pickup time
        
        Returns:
            float: Multiplier (1.0, 1.3, or 1.5)
        """
        if isinstance(pickup_time, str):
            try:
                pickup_time = datetime.strptime(pickup_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return 1.0
        
        hour = pickup_time.hour
        
        # Check peak hours
        for start, end in FareCalculator.PEAK_HOURS:
            if start <= hour < end:
                return FareCalculator.PEAK_HOUR_MULTIPLIER
        
        # Check night hours
        if hour >= FareCalculator.NIGHT_HOURS[0] or hour < FareCalculator.NIGHT_HOURS[1]:
            return FareCalculator.NIGHT_MULTIPLIER
        
        return 1.0
    
    @staticmethod
    def estimate_distance(pickup, dropoff):
        """
        Estimate distance between two locations (simplified)
        In a real application, this would use a mapping API
        
        Args:
            pickup (str): Pickup location
            dropoff (str): Dropoff location
        
        Returns:
            float: Estimated distance in kilometers
        """
        # Simple hash-based distance estimation for demo purposes
        # In production, use Google Maps API or similar
        hash_pickup = sum(ord(c) for c in pickup.lower())
        hash_dropoff = sum(ord(c) for c in dropoff.lower())
        
        # Generate distance between 2-50 km based on location names
        base_distance = abs(hash_pickup - hash_dropoff) % 48 + 2
        
        return round(base_distance, 1)
    
    @staticmethod
    def get_fare_breakdown(distance, vehicle_type, pickup_time=None):
        """
        Get detailed fare breakdown
        
        Returns:
            dict: Breakdown of fare components
        """
        base = FareCalculator.BASE_FARE.get(vehicle_type, 50)
        per_km = FareCalculator.PER_KM_RATE.get(vehicle_type, 12)
        distance_fare = distance * per_km
        
        multiplier = 1.0
        multiplier_text = "Standard"
        
        if pickup_time:
            multiplier = FareCalculator._get_time_multiplier(pickup_time)
            if multiplier == FareCalculator.PEAK_HOUR_MULTIPLIER:
                multiplier_text = "Peak Hours (1.5x)"
            elif multiplier == FareCalculator.NIGHT_MULTIPLIER:
                multiplier_text = "Night Time (1.3x)"
        
        subtotal = base + distance_fare
        total = subtotal * multiplier
        
        return {
            "base_fare": base,
            "distance": distance,
            "per_km_rate": per_km,
            "distance_fare": round(distance_fare, 2),
            "subtotal": round(subtotal, 2),
            "multiplier": multiplier,
            "multiplier_text": multiplier_text,
            "total": round(total, 2)
        }