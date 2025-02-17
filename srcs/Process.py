class Process:

    def __init__(self):
        self.name = ""
        self.needs = {}  # Using a set to represent needs (hashable items)
        self.results = {}  # Using a set to represent results (hashable items)
        self.delay = 0

    def add_need(self, name, quantity):
        self.needs[name] = quantity
    
    def add_result(self, name, quantity):
        self.results[name] = quantity

    def __lt__(self, other):
        # Compare based on the delay
        return self.delay < other.delay
