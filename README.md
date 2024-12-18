# Flight-Planner

## Overview
The Flight Planner is a Python-based program that helps users plan flight itineraries between cities with three optimization goals:

1. **Fewest Flights and Earliest Arrival**: Minimize the number of flights and prioritize the earliest arrival time.
2. **Cheapest Trip**: Minimize the total fare of the trip.
3. **Fewest Flights and Cheapest Trip**: Minimize the number of flights and prioritize the lowest fare.

This project uses a graph-based approach where cities are nodes and flights are edges with specific attributes like departure time, arrival time, and fare. The program employs efficient data structures such as queues and heaps to ensure optimized solutions.

---

## File Structure

### `flight.py`
Contains the `Flight` class to represent individual flights. Each flight has:
- **Flight Number**: Unique identifier.
- **Start City**: City of departure.
- **Departure Time**: Time of departure (integer).
- **End City**: Destination city.
- **Arrival Time**: Time of arrival (integer).
- **Fare**: Cost of the flight.

### `planner.py`
Contains the `Planner` class, which implements the route-finding algorithms:

- **`least_flights_earliest_route`**: Finds the route with the fewest flights and the earliest arrival.
- **`cheapest_route`**: Finds the route with the lowest fare.
- **`least_flights_cheapest_route`**: Finds the route with the fewest flights and the lowest fare.

It also includes utility data structures:
- **`Queue`**: Used for BFS in route optimization.
- **`Heap`**: Used for cost-based and combined optimizations.

### `main.py`
Driver script to demonstrate the functionality of the planner. It initializes sample flight data, runs the route-finding algorithms, and compares the results with expected outputs.

---

## How to Run
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd flight-planner
   ```

2. Ensure Python 3.x is installed.

3. Run the `main.py` file:
   ```bash
   python main.py
   ```

---

## Example Usage
Given flights and a planning instance, you can find routes by calling:

```python
planner = Planner(flights)
route1 = planner.least_flights_earliest_route(start_city, end_city, t1, t2)
route2 = planner.cheapest_route(start_city, end_city, t1, t2)
route3 = planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
```

---

## Requirements
- Python 3.x

---

## Key Features
- **Optimized Algorithms**: Routes are computed efficiently using BFS and priority queues.
- **Modularity**: The code is modular, allowing for easy extension and testing.

---


