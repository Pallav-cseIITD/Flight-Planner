# flight.py
class Flight:
    def __init__(self, flight_no, start_city, departure_time, end_city, arrival_time, fare):
        """ Class for the flights

        Args:
            flight_no (int): Unique ID of each flight
            start_city (int): The city no. where the flight starts
            departure_time (int): Time at which the flight starts
            end_city (int): The city no where the flight ends
            arrival_time (int): Time at which the flight ends
            fare (int): The cost of taking this flight
        """
        self.flight_no = flight_no
        self.start_city = start_city
        self.departure_time = departure_time
        self.end_city = end_city
        self.arrival_time = arrival_time
        self.fare = fare

    def __repr__(self):
        """String representation for debugging purposes."""
        return f"Flight({self.flight_no}, {self.start_city}, {self.departure_time}, {self.end_city}, {self.arrival_time}, {self.fare})"

"""
If there are n flights, and m cities:

1. Flight No. will be an integer in {0, 1, ... n-1}
2. Cities will be denoted by an integer in {0, 1, .... m-1}
3. Time is denoted by a non negative integer - we model time as going from t=0 to t=inf
"""

# planner.py
from flight import Flight

class Queue:
    def __init__(self):
        self.lst = []
        self.start = 0
        self.end = 0
    
    def enqueue(self, item):
        self.lst.append(item)
        self.end += 1
    
    def dequeue(self):
        if self.start < self.end:
            item = self.lst[self.start]
            self.start += 1
            return item
        return None
    
    def is_empty(self):
        return self.start >= self.end

class Heap:
    def __init__(self, comparison_function, init_array):
        self.comparison_function = comparison_function
        self.heap = []
        for elem in init_array:
            self.insert(elem)

    def insert(self, value):
        self.heap.append(value)
        self.heapify_up(len(self.heap) - 1)

    def extract(self):
        if len(self.heap) == 0:
            raise IndexError("Extract from an empty heap")
        if len(self.heap) == 1:
            return self.heap.pop()

        top_elem = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        return top_elem

    def heapify_up(self, index):
        prev_index = (index - 1) // 2
        while index > 0 and self.comparison_function(self.heap[index], self.heap[prev_index]):
            self.heap[index], self.heap[prev_index] = self.heap[prev_index], self.heap[index]
            index = prev_index
            prev_index = (index - 1) // 2

    def heapify_down(self, index):
        n = len(self.heap)
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest_index = index

            if left_child_index < n and self.comparison_function(self.heap[left_child_index], self.heap[smallest_index]):
                smallest_index = left_child_index

            if right_child_index < n and self.comparison_function(self.heap[right_child_index], self.heap[smallest_index]):
                smallest_index = right_child_index

            if smallest_index == index:
                break

            self.heap[index], self.heap[smallest_index] = self.heap[smallest_index], self.heap[index]
            index = smallest_index

class Planner:
    def __init__(self, flights):
        self.flights = flights
        max_city = 0

        for flight in flights:
            max_city = max(max_city, flight.start_city, flight.end_city)
        self.start_adj = [[] for i in range(max_city + 1)]

        for i in range(len(flights)):
            flight = flights[i]
            self.start_adj[flight.start_city].append(i)

    def get_ans(self, prev, last_idx):
        if last_idx is None:
            return []
        path = []
        curr = last_idx
        while curr is not None:
            path.append(self.flights[curr])
            curr = prev[curr]
            
        i,j = 0, len(path) - 1
        while (i < j):
            path[i], path[j] = path[j], path[i]
            i += 1
            j -= 1
        return path

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        
        mincount = float('inf')
        early = float('inf')
        best_route = None
        queue = Queue()
        prev = [None] * len(self.flights)
        visited = [False] * len(self.flights)
        
        for i in self.start_adj[start_city]:
            flight = self.flights[i]
            if t1 <= flight.departure_time and flight.arrival_time <= t2:
                queue.enqueue((i, 1, flight.arrival_time))
                visited[i] = True

        while not queue.is_empty():
            idx, count, time = queue.dequeue()
            flight = self.flights[idx]
            
            if flight.end_city == end_city:
                if count < mincount or (count == mincount and time < early):
                    best_route = idx
                    mincount = count
                    early = time
            
            for j in self.start_adj[flight.end_city]:
                if not visited[j]:
                    next_flight = self.flights[j]
                    if (flight.end_city == next_flight.start_city):
                        if (next_flight.arrival_time <= t2 and next_flight.departure_time >= flight.arrival_time + 20):
                            visited[j] = True
                            prev[j] = idx
                            queue.enqueue((j, count + 1, next_flight.arrival_time))
        
        return self.get_ans(prev, best_route)

    def cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        
        def minheap_compare(a, b):
            return a[0] < b[0]
        
        best_route = None
        cheapest = float('inf')
        minheap = Heap(minheap_compare, [])
        prev = [None] * len(self.flights)
        visited = [False] * len(self.flights)
        best_cost = [float('inf')] * len(self.flights)
         
        for i in self.start_adj[start_city]:
            flight = self.flights[i]
            if t1 <= flight.departure_time and flight.arrival_time <= t2:
                minheap.insert((flight.fare, i))
                best_cost[i] = flight.fare
        
        while minheap.heap:
            cost, idx = minheap.extract()
            if visited[idx]:
                continue
                
            visited[idx] = True
            flight = self.flights[idx]
            
            if flight.end_city == end_city and cost < cheapest:
                best_route = idx
                cheapest = cost
            
            for j in self.start_adj[flight.end_city]:
                next_flight = self.flights[j]
                if (flight.end_city == next_flight.start_city):
                    if (next_flight.arrival_time <= t2 and next_flight.departure_time >= flight.arrival_time + 20):
                        new_cost = cost + next_flight.fare
                        if new_cost < best_cost[j]:
                            best_cost[j] = new_cost
                            prev[j] = idx
                            minheap.insert((new_cost, j))
        
        return self.get_ans(prev, best_route)

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        
        def compare(a, b):
            return (a[0], a[1]) < (b[0], b[1])
        
        numb = float('inf')
        mincost = float('inf')
        best_route = None
        minheap = Heap(compare, [])
        prev = [None] * len(self.flights)
        visited = [False] * len(self.flights)
                
        for i in self.start_adj[start_city]:
            flight = self.flights[i]
            if t1 <= flight.departure_time and flight.arrival_time  <= t2:
                minheap.insert((1, flight.fare, i))
        
        while minheap.heap:
            count, cost, idx = minheap.extract()
            if visited[idx]:
                continue
                
            visited[idx] = True
            flight = self.flights[idx]
            
            if (flight.end_city == end_city): 
                if count < numb or (count == numb and cost < mincost):
                    best_route = idx
                    numb = count
                    mincost = cost
            
            for j in self.start_adj[flight.end_city]:
                if not visited[j]:
                    next_flight = self.flights[j]
                    if (flight.end_city == next_flight.start_city):
                        if (next_flight.arrival_time <= t2 and next_flight.departure_time >= flight.arrival_time + 20):
                            minheap.insert((count + 1, cost + next_flight.fare, j))
                            prev[j] = idx
        
        return self.get_ans(prev, best_route)
