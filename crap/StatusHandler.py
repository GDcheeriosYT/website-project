class StatusHandler:
    def __init__(self, name: str):
        self.name = name
        self.total_amount = 0
        self.successful_amount = 0
        self.health = 100

    def calculate_health(self):
        self.health = int((self.successful_amount/self.total_amount) * 100)

    def successful(self):
        print(f"{self.name} request successful")
        self.total_amount += 1
        self.successful_amount += 1
        self.calculate_health()

    def unsuccessful(self):
        print(f"{self.name} request unsuccessful")
        self.total_amount += 1
        self.calculate_health()
