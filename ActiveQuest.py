import json

# Classes
class ActiveSpot:
    # Represents an active spot (e.g., park, gym, home) where activities can be performed
    def __init__(self, id, name, location, type, available_activities, bonus_points):
        self.id = id
        self.name = name
        self.location = location
        self.type = type
        self.available_activities = available_activities
        self.bonus_points = bonus_points

class Activity:
    # Represents an activity (e.g., soccer, yoga) that players can perform to earn points and improve stats
    def __init__(self, id, name, skill_boosts, base_points, first_time_bonus, duration):
        self.id = id
        self.name = name
        self.skill_boosts = skill_boosts
        self.base_points = base_points
        self.first_time_bonus = first_time_bonus
        self.duration = duration

class Service:
    # Represents a service (e.g., physiotherapy, personal training) that players can purchase for benefits
    def __init__(self, id, name, skill_boosts, cost, linked_active_spot_id):
        self.id = id
        self.name = name
        self.skill_boosts = skill_boosts
        self.cost = cost
        self.linked_active_spot_id = linked_active_spot_id

class Game:
    # The main game class that manages active spots, activities, services, and user interaction
    def __init__(self):
        self.active_spots = []  # List of active spots
        self.activities = []   # List of activities
        self.services = []     # List of services
        self.load_data()       # Load data from JSON files

    def load_data(self):
        # Load active spots, activities, and services data from JSON files
        with open("active_spots.json", "r") as f:
            active_spots_data = json.load(f)
            for spot in active_spots_data:
                self.active_spots.append(ActiveSpot(**spot))

        with open("activities.json", "r") as f:
            activities_data = json.load(f)
            for activity in activities_data:
                self.activities.append(Activity(**activity))

        with open("services.json", "r") as f:
            services_data = json.load(f)
            for service in services_data:
                self.services.append(Service(**service))

    def save_data(self):
        # Save active spots, activities, and services data to JSON files
        with open("active_spots.json", "w") as f:
            json.dump([spot.__dict__ for spot in self.active_spots], f, indent=4)
        with open("activities.json", "w") as f:
            json.dump([activity.__dict__ for activity in self.activities], f, indent=4)
        with open("services.json", "w") as f:
            json.dump([service.__dict__ for service in self.services], f, indent=4)

    def display_active_spots(self):
        # Display a list of all active spots with their details
        print("\nActive Spots:")
        for spot in self.active_spots:
            print(f"{spot.id}. {spot.name} ({spot.type}) - Bonus Points: {spot.bonus_points}")

    def display_activities(self):
        # Display a list of all activities with their details
        print("\nActivities:")
        for activity in self.activities:
            print(f"{activity.id}. {activity.name} - Base Points: {activity.base_points}, First-Time Bonus: {activity.first_time_bonus}")

    def display_services(self):
        # Display a list of all services with their details
        print("\nServices:")
        for service in self.services:
            print(f"{service.id}. {service.name} - Cost: {service.cost} points")

    def display_help(self):
        # Display the help menu with instructions for using the game
        print("\nHelp Menu:")
        print("1. View Active Spots: Displays all active spots you can visit.")
        print("2. View Activities: Lists all available activities with their details.")
        print("3. View Services: Shows services available at active spots and their costs.")
        print("4. Exit: Saves your progress and exits the game.")
        print("Type the corresponding number to navigate to a menu option.")

    def main_menu(self):
        # Display the main menu and handle user input
        print("Welcome to ActiveQuest! Type 'help' to see all available commands.")
        while True:
            print("\nMain Menu:")
            print("1. View Active Spots")
            print("2. View Activities")
            print("3. View Services")
            print("4. Exit")
            print("Type 'help' for a list of commands.")

            choice = input("Choose an option: ")

            if choice.lower() == "help":
                # Display help menu if user types 'help'
                self.display_help()
            elif choice == "1":
                # Display active spots
                self.display_active_spots()
            elif choice == "2":
                # Display activities
                self.display_activities()
            elif choice == "3":
                # Display services
                self.display_services()
            elif choice == "4":
                # Exit the game and save progress
                print("Goodbye! Thanks for playing ActiveQuest.")
                self.save_data()
                break
            else:
                # Handle invalid input
                print("Invalid choice. Try again.")

# Initialize and start the game
if __name__ == "__main__":
    game = Game()
    game.main_menu()