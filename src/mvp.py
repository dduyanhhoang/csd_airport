from math import sqrt
from typing import List

import heapq
import os


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
            for c in loc:
                if not isinstance(c, float):
                    raise ValueError("Invalid location")
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

    def find_shortest_route_with_stop(self, start_id: str, stop_id: str, end_id: str):
        path1, cost1 = self.find_shortest_route(start_id, stop_id)

        path2, cost2 = self.find_shortest_route(stop_id, end_id)

        full_path = path1[:-1] + path2

        total_cost = cost1 + cost2

        return full_path, total_cost

    def display_graph(self):
        adjacency_list = {airport: [] for airport in self.airports}
        for f in self.flights:
            adjacency_list[f.dep.a_id].append((f.des.a_id, f))

        print("Airline Graph:")
        for airport, neighbors in adjacency_list.items():
            print(f"{airport}:")
            for neighbor in neighbors:
                print(
                    f"  -> {neighbor[0]} (Aircraft: {neighbor[1].aircraft_type}, Cost: {self.calculate_cost(neighbor[1]):.2f})")

    def generate_mermaid(self) -> str:
        mermaid = ["flowchart TD"]

        for a in self.airports:
            mermaid.append(f"\t{a}({a})")

        for f in self.flights:
            dep_id = f.dep.a_id
            des_id = f.des.a_id
            c = self.calculate_cost(f)
            mermaid.append(f"\t{dep_id}({dep_id}) -->|{c:.2f}| {des_id}({des_id})")

        return "\n".join(mermaid)


def example():
    airport_system = AirportSystem()

    # Add some airports
    airport_system.add_airport(Airport("JFK", [40.6413, -73.7781], "L"))
    airport_system.add_airport(Airport("LAX", [33.9416, -118.4085], "L"))
    airport_system.add_airport(Airport("ORD", [41.9742, -87.9073], "L"))
    airport_system.add_airport(Airport("ATL", [33.6407, -84.4277], "L"))
    airport_system.add_airport(Airport("DFW", [32.8998, -97.0403], "L"))
    airport_system.add_airport(Airport("DEN", [39.8561, -104.6737], "L"))
    airport_system.add_airport(Airport("SFO", [37.6213, -122.3790], "L"))

    # Add some flights
    airport_system.add_flight(Flight(airport_system.airports["JFK"], airport_system.airports["LAX"], "L"))
    airport_system.add_flight(Flight(airport_system.airports["JFK"], airport_system.airports["LAX"], "M"))
    airport_system.add_flight(Flight(airport_system.airports["JFK"], airport_system.airports["LAX"], "M"))
    airport_system.add_flight(Flight(airport_system.airports["JFK"], airport_system.airports["ORD"], "M"))
    airport_system.add_flight(Flight(airport_system.airports["ORD"], airport_system.airports["LAX"], "S"))
    airport_system.add_flight(Flight(airport_system.airports["ORD"], airport_system.airports["ATL"], "L"))
    airport_system.add_flight(Flight(airport_system.airports["ATL"], airport_system.airports["DFW"], "M"))
    airport_system.add_flight(Flight(airport_system.airports["DFW"], airport_system.airports["LAX"], "S"))
    airport_system.add_flight(Flight(airport_system.airports["DFW"], airport_system.airports["DEN"], "M"))
    airport_system.add_flight(Flight(airport_system.airports["DEN"], airport_system.airports["SFO"], "L"))
    airport_system.add_flight(Flight(airport_system.airports["LAX"], airport_system.airports["SFO"], "L"))

    while True:
        try:
            clear_screen()
            airport_system.display_graph()
            print_graph = input("Do you want to display the graph? (Y/N): ").strip().upper()
            if print_graph not in ['Y', 'N']:
                clear_screen()
                raise ValueError("Invalid choice. Please enter 'Y' or 'N'.")
            break
        except ValueError as ve:
            print(f"Error: {ve}")
            input("Press Enter to try again...")

    if print_graph == 'Y':
        with open("output.md", "a") as file:
            file.write("```mermaid\n")
            file.write(airport_system.generate_mermaid())
            file.write("\n```\n\n")
        print("Mermaid graph code written to output.md")

    while True:
        try:
            user_input = input("Perform the finding the short test path? (Y/N): ").strip().upper()
            if user_input not in ['Y', 'N']:
                raise ValueError("Invalid choice. Please enter 'Y' or 'N'.")
            break
        except ValueError as ve:
            print(f"Error: {ve}")
            input("Press Enter to try again...")

    if user_input == 'Y':
        s = input("Enter start airport ID: ").strip().upper()
        e = input("Enter end airport ID: ").strip().upper()

        path, cost = airport_system.find_shortest_route(s, e)
        print("\nShortest path from JFK to SFO:", path, "with cost:", cost)

        with open("output.md", "a") as file:
            file.write("```mermaid\n")
            file.write(airport_system.generate_mermaid())
            for d in path:
                file.write(f"\n\tstyle {d} stroke:#0f0")
            file.write("\n```\n\n")
            print("Mermaid graph code written to output.md")


def clear_screen():
    if os.name == 'nt':
        os.system('cls')  # For Windows
    else:
        os.system('clear')


def menu():
    airport_system = AirportSystem()

    while True:
        clear_screen()
        print("Airport System Menu")
        print("1. Add airport")
        print("2. Remove airport")
        print("3. Update airport")
        print("4. Display airports")
        print("5. Add flight")
        print("6. Display flights")
        print("7. Calculate cost")
        print("8. Find shortest route")
        print("9. Find shortest route with stop")
        print("10. Display graph")
        print("11. Generate Mermaid")
        print("12. Exit")

        choice = input("Enter choice: ").strip()

        if choice not in [str(i) for i in range(1, 13)]:
            clear_screen()
            print("Invalid choice. Please enter a number between 1 and 12.")
            input("Press Enter to return to the menu...")
            continue

        clear_screen()

        try:
            if choice == "1":
                a_id = input("Enter airport ID: ").strip()
                if not a_id:
                    raise ValueError("Airport ID cannot be blank.")
                loc = [float(x) for x in input("Enter location (lat, long): ").strip().split(",")]
                if len(loc) != 2:
                    raise ValueError("Location must contain two values: latitude and longitude.")
                airport_type = input("Enter airport type (L, M, S): ").strip().upper()
                if airport_type not in ['L', 'M', 'S']:
                    raise ValueError("Airport type must be 'L', 'M', or 'S'.")
                airport_system.add_airport(Airport(a_id, loc, airport_type))
                print("Airport added successfully.")
                airport_system.display_airports()
            elif choice == "2":
                a_id = input("Enter airport ID: ").strip()
                if not a_id:
                    raise ValueError("Airport ID cannot be blank.")
                airport_system.remove_airport(a_id)
                for f in airport_system.flights:
                    if f.dep.a_id == a_id or f.des.a_id == a_id:
                        airport_system.flights.remove(f)

                print("Airport removed successfully.")
                airport_system.display_airports()
            elif choice == "3":
                a_id = input("Enter airport ID: ").strip()
                if not a_id:
                    raise ValueError("Airport ID cannot be blank.")
                new_loc = [float(x) for x in input("Enter new location (lat, long): ").strip().split(",")]
                if len(new_loc) != 2:
                    raise ValueError("Location must contain two values: latitude and longitude.")
                new_type = input("Enter new airport type (L, M, S): ").strip().upper()
                if new_type not in ['L', 'M', 'S']:
                    raise ValueError("Airport type must be 'L', 'M', or 'S'.")
                airport_system.update_airport(a_id, new_loc, new_type)
                print("Airport updated successfully.")
                airport_system.display_airports()
            elif choice == "4":
                airport_system.display_airports()
            elif choice == "5":
                dep = input("Enter departure airport ID: ").strip()
                des = input("Enter destination airport ID: ").strip()
                aircraft_type = input("Enter aircraft type (L, M, S): ").strip().upper()
                if aircraft_type not in ['L', 'M', 'S']:
                    raise ValueError("Aircraft type must be 'L', 'M', or 'S'.")
                if dep not in airport_system.airports or des not in airport_system.airports:
                    raise ValueError("Both departure and destination airports must exist in the system.")
                airport_system.add_flight(Flight(airport_system.airports[dep], airport_system.airports[des], aircraft_type))
                print("Flight added successfully.")
                airport_system.display_flights()
            elif choice == "6":
                airport_system.display_flights()
            elif choice == "7":
                dep = input("Enter departure airport ID: ").strip()
                des = input("Enter destination airport ID: ").strip()
                aircraft_type = input("Enter aircraft type (L, M, S): ").strip().upper()
                if aircraft_type not in ['L', 'M', 'S']:
                    raise ValueError("Aircraft type must be 'L', 'M', or 'S'.")
                if dep not in airport_system.airports or des not in airport_system.airports:
                    raise ValueError("Both departure and destination airports must exist in the system.")
                flight = Flight(airport_system.airports[dep], airport_system.airports[des], aircraft_type)
                cost = airport_system.calculate_cost(flight)
                print("Cost:", cost)
            elif choice == "8":
                start_id = input("Enter start airport ID: ").strip()
                end_id = input("Enter end airport ID: ").strip()
                if start_id not in airport_system.airports or end_id not in airport_system.airports:
                    raise ValueError("Both start and end airports must exist in the system.")
                path, cost = airport_system.find_shortest_route(start_id, end_id)
                print("Shortest path:", path, "with cost:", cost)

                with open("output.md", "a") as file:
                    file.write("```mermaid\n")
                    file.write(airport_system.generate_mermaid())
                    for d in path:
                        file.write(f"\n\tstyle {d} stroke:#0f0")
                    file.write("\n```\n\n")
                    print("Mermaid graph code written to output.md")
            elif choice == "9":
                start_id = input("Enter start airport ID: ").strip()
                stop_id = input("Enter stop airport ID: ").strip()
                end_id = input("Enter end airport ID: ").strip()
                if start_id not in airport_system.airports or stop_id not in airport_system.airports or end_id not in airport_system.airports:
                    raise ValueError("All start, stop, and end airports must exist in the system.")
                path, cost = airport_system.find_shortest_route_with_stop(start_id, stop_id, end_id)
                print("Shortest path with stop:", path, "with cost:", cost)
            elif choice == "10":
                airport_system.display_graph()
                mermaid_graph = airport_system.generate_mermaid()
                with open("output.md", "a") as file:
                    file.write("```mermaid\n")
                    file.write(mermaid_graph)
                    file.write("\n```")
                print("Mermaid graph code written to output.md")
            elif choice == "11":
                mermaid_graph = airport_system.generate_mermaid()
                print(mermaid_graph)
                with open("output.md", "a") as file:
                    file.write("```mermaid\n")
                    file.write(mermaid_graph)
                    file.write("\n```\n")
                print("Mermaid graph code written to output.md")
            elif choice == "12":
                break
        except ValueError as ve:
            print(f"Error: {ve}")
        except KeyError as ke:
            print(f"Error: {ke}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        input("Press Enter to return to the menu...")


if __name__ == '__main__':
    while True:
        clear_screen()
        user_choice = input("Do you want to run the example or the menu? (E/M): ").strip().upper()
        if user_choice in ['E', 'M']:
            break
        else:
            print("Invalid choice. Please enter 'E' for example or 'M' for menu.")
            input("Press Enter to try again...")

    if user_choice == 'E':
        example()
    else:
        menu()
