from math import sqrt
from typing import List

import heapq


class Airport:
    AIRPORT_TYPES = ['L', 'M', 'S']

    def __init__(self, a_id: str, loc: List[float], airport_type: str):
        self.a_id = a_id
        self.loc = loc
        self.airport_type = airport_type.upper()

    @property
    def a_id(self) -> str:
        return self._a_id

    @property
    def loc(self) -> list:
        return self._loc

    @property
    def airport_type(self) -> str:
        return self._airport_type

    @a_id.setter
    def a_id(self, a_id: str):
        if len(a_id) == 3:
            self._a_id = a_id
        else:
            raise ValueError("Invalid airport ID")

    @loc.setter
    def loc(self, loc: list):
        if len(loc) == 2:
            self._loc = loc
        else:
            raise ValueError("Invalid location")

    @airport_type.setter
    def airport_type(self, airport_type):
        if airport_type.upper() in Airport.AIRPORT_TYPES:
            self._airport_type = airport_type.upper()
        else:
            raise ValueError("Invalid airport type")

    def __str__(self):
        return f"Airport: {self.a_id}\nLocation: {self.loc}\nType: {self.airport_type}"


class Flight:
    AIRCRAFT_TYPES = ['L', 'M', 'S']

    def __init__(self, dep: str, des: str, aircraft_type: str):
        self.dep = dep
        self.des = des
        self.aircraft_type = aircraft_type

    @property
    def dep(self):
        return self._dep

    @property
    def des(self):
        return self._des

    @property
    def aircraft_type(self):
        return self._aircraft_type

    @dep.setter
    def dep(self, dep):
        if isinstance(dep, Airport):
            self._dep = dep
        else:
            raise ValueError("Invalid airport")

    @des.setter
    def des(self, des):
        if isinstance(des, Airport):
            self._des = des
        else:
            raise ValueError("Invalid airport")

    @aircraft_type.setter
    def aircraft_type(self, aircraft_type):
        if aircraft_type.upper() in Flight.AIRCRAFT_TYPES:
            self._aircraft_type = aircraft_type.upper()
        else:
            raise ValueError("Invalid aircraft type")

    def __str__(self):
        return f"Departure: {self.dep}\nDestination: {self.des}\nAircraft type: {self.aircraft_type}"


class AirportSystem:
    AIRCRAFT_MULTIPLIER = {'L': 1.5, 'M': 1.0, 'S': 0.8}
    AIRPORT_MULTIPLIER = {'L': 1.5, 'M': 1.0, 'S': 0.8}

    def __init__(self):
        self.airports = dict()
        self.flights = list()

    def add_airport(self, airport: Airport):
        if airport.a_id in self.airports:
            raise ValueError("Airport already exists")
        self.airports[airport.a_id] = airport

    def remove_airport(self, a_id: str):
        if a_id not in self.airports:
            raise ValueError("Airport does not exist")
        del self.airports[a_id]

    def update_airport(self, a_id: str, new_loc: List[float] = None, new_type: str = None):
        if a_id not in self.airports:
            raise ValueError("Airport does not exist")
        airport = self.airports[a_id]
        if new_loc:
            airport.loc = new_loc
        if new_type:
            airport.airport_type = new_type

    def display_airports(self):
        for airport in self.airports.values():
            print("Airport info" + "=" * 20)
            print(airport)

    def add_flight(self, new_flight: Flight):
        self.flights.append(new_flight)

    def display_flights(self):
        for current_flight in self.flights:
            print("Flight info" + "-" * 20)
            print(current_flight)

    @staticmethod
    def calculate_cost(f: Flight) -> float:
        dep_airport = f.dep
        des_airport = f.des

        distance = sqrt((dep_airport.loc[0] - des_airport.loc[0]) ** 2 + (dep_airport.loc[1] - des_airport.loc[1]) ** 2)

        aircraft_multiplier = AirportSystem.AIRCRAFT_MULTIPLIER[f.aircraft_type]

        dep_airport_multiplier = AirportSystem.AIRPORT_MULTIPLIER[dep_airport.airport_type]
        des_airport_multiplier = AirportSystem.AIRPORT_MULTIPLIER[des_airport.airport_type]
        airport_multiplier = des_airport_multiplier + dep_airport_multiplier

        f_cost = distance * aircraft_multiplier * airport_multiplier

        return f_cost

    def find_shortest_route(self, start_id: str, end_id: str):
        if start_id not in self.airports or end_id not in self.airports:
            raise ValueError("One or both airports not found")

        distances = {airport: float('infinity') for airport in self.airports}
        previous_airports = {airport: None for airport in self.airports}
        distances[start_id] = 0
        pq = [(0, start_id)]

        while pq:
            current_distance, current_airport = heapq.heappop(pq)

            if current_distance > distances[current_airport]:
                continue

            for f in self.flights:
                if f.dep.a_id == current_airport:
                    neighbor = f.des.a_id
                    f_cost = self.calculate_cost(f)

                    new_distance = current_distance + f_cost
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous_airports[neighbor] = current_airport
                        heapq.heappush(pq, (new_distance, neighbor))

        # Reconstruct the shortest path
        f_path = []
        current_airport = end_id
        while previous_airports[current_airport] is not None:
            f_path.insert(0, current_airport)
            current_airport = previous_airports[current_airport]
        f_path.insert(0, start_id)

        return f_path, distances[end_id]


if __name__ == '__main__':
    airport_system = AirportSystem()

    airport_system.add_airport(Airport("JFK", [40.6413, -73.7781], "L"))
    airport_system.add_airport(Airport("LAX", [33.9416, -118.4085], "L"))

    flight = Flight(airport_system.airports["JFK"], airport_system.airports["LAX"], "L")
    airport_system.add_flight(flight)

    airport_system.display_airports()
    airport_system.display_flights()

    cost = airport_system.calculate_cost(flight)
    print("Cost:", cost)

    path, cost = airport_system.find_shortest_route("JFK", "LAX")
    print("Shortest path:", path, "with cost:", cost)
