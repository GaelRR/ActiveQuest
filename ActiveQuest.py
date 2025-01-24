import json

# Class for Active Spots
class ActiveSpot:
    def __init__(self, id, name, location, type, available_activities, bonus_points):
        self.id = id
        self.name = name
        self.location = location
        self.type = type
        self.available_activities = available_activities
        self.bonus_points = bonus_points

# Class for Activities
class Activity:
    def __init__(self, id, name, skill_boosts, base_points, first_time_bonus, duration):
        self.id = id
        self.name = name
        self.skill_boosts = skill_boosts
        self.base_points = base_points
        self.first_time_bonus = first_time_bonus
        self.duration = duration

# Class for Services
class Service:
    def __init__(self, id, name, skill_boosts, cost, linked_active_spot_id):
        self.id = id
        self.name = name
        self.skill_boosts = skill_boosts
        self.cost = cost
        self.linked_active_spot_id = linked_active_spot_id

# Class for Player
class Player:
    def __init__(self):
        self.name = ""
        self.age = 0
        self.height = 0
        self.weight = 0
        self.visited_spots = set()
        self.completed_activities = []
        self.stats = {"⚡ Speed": 0, "🐢 Endurance": 0, "💪 Strength": 0, "🧘 Flexibility": 0, "⚖️ Coordination": 0}
        self.total_points = 0

    # Update player stats after an activity or service
    def update_stats(self, boosts):
        for boost in boosts:
            if boost in self.stats:
                self.stats[boost] += 1
            else:
                print(f"Warning: {boost} is not a valid stat and was skipped.")

    # Edit player information
    def edit_info(self):
        print("\nEdit Player Information:")
        self.name = input("Enter your name: ")
        self.age = int(input("Enter your age: "))
        self.height = int(input("Enter your height (in cm): "))
        self.weight = int(input("Enter your weight (in kg): "))
        print("Player information updated successfully!")

# Main Game Class
class Game:
    def __init__(self):
        self.active_spots = []  # List of ActiveSpot objects
        self.activities = []   # List of Activity objects
        self.services = []     # List of Service objects
        self.player = Player() # Player object
        self.load_data()       # Load data from JSON files
        self.create_player()   # Initialize player information

    # Load active spots, activities, and services from JSON files
    def load_data(self):
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

    # Save player progress to a JSON file
    def save_data(self):
        with open("player_data.json", "w") as f:
            json.dump({
                "name": self.player.name,
                "age": self.player.age,
                "height": self.player.height,
                "weight": self.player.weight,
                "visited_spots": list(self.player.visited_spots),
                "completed_activities": self.player.completed_activities,
                "stats": self.player.stats,
                "total_points": self.player.total_points
            }, f, indent=4)

    # Create a new player or load existing data
    def create_player(self):
        print("Welcome to ActiveQuest! Let's create your character.")
        self.player.name = input("Enter your name: ")
        self.player.age = int(input("Enter your age: "))
        self.player.height = int(input("Enter your height (in cm): "))
        self.player.weight = int(input("Enter your weight (in kg): "))
        print(f"Character created! Welcome, {self.player.name}!")

    # Display the menu
    def display_menu(self):
        print("\n******************************")
        print("1. Edit Info  2. Visit Spot  3. Activity  4. Stats")
        print("5. Logs       6. Services    7. Use Svc   8. Help")
        print("9. Exit")
        print("******************************")

    # Visit an active spot and earn points
    def visit_active_spot(self):
        print("\nAvailable Active Spots:")
        for spot in self.active_spots:
            print(f"{spot.id}. {spot.name} ({spot.type}) - Bonus Points: {spot.bonus_points}")

        choice = input("Enter the number of the active spot you want to visit: ")
        spot = next((s for s in self.active_spots if str(s.id) == choice), None)

        if spot:
            if spot.id not in self.player.visited_spots:
                print(f"You visited {spot.name} for the first time! You earned {spot.bonus_points} points!")
                self.player.total_points += spot.bonus_points
                self.player.visited_spots.add(spot.id)
            else:
                print(f"You revisited {spot.name}.")
        else:
            print("Invalid choice. Returning to the menu.")

    # Perform an activity and earn points
    def perform_activity(self):
        print("\nAvailable Activities:")
        for activity in self.activities:
            print(f"{activity.id}. {activity.name} - Base Points: {activity.base_points}, First-Time Bonus: {activity.first_time_bonus}")

        choice = input("Enter the number of the activity you want to perform: ")
        activity = next((a for a in self.activities if str(a.id) == choice), None)

        if activity:
            first_time = activity.id not in [a["id"] for a in self.player.completed_activities]
            points = activity.base_points + (activity.first_time_bonus if first_time else 0)
            self.player.total_points += points
            self.player.update_stats(activity.skill_boosts)
            self.player.completed_activities.append({"id": activity.id, "name": activity.name})

            if first_time:
                print(f"You performed {activity.name} for the first time! You earned {points} points!")
            else:
                print(f"You performed {activity.name} and earned {points} points.")
        else:
            print("Invalid choice. Returning to the menu.")

    # View player stats
    def view_stats(self):
        print("\nPlayer Stats:")
        print(f"Name: {self.player.name}, Age: {self.player.age}, Height: {self.player.height} cm, Weight: {self.player.weight} kg")
        for stat, value in self.player.stats.items():
            print(f"{stat}: {value}")
        print(f"Total Points: {self.player.total_points}")

    # View activity log and visited spots
    def view_logs(self):
        print("\nActivity Log:")
        for entry in self.player.completed_activities:
            print(f"- {entry['name']}")
        print("\nVisited Spots:")
        for spot_id in self.player.visited_spots:
            spot = next((s for s in self.active_spots if s.id == spot_id), None)
            if spot:
                print(f"- {spot.name}")

    # View available services
    def view_services(self):
        print("\nAvailable Services:")
        for service in self.services:
            print(f"{service.id}. {service.name} - Cost: {service.cost} points")

    # Use a service to improve stats
    def use_service(self):
        self.view_services()
        choice = input("Enter the number of the service you want to use: ")
        service = next((s for s in self.services if str(s.id) == choice), None)

        if service:
            if self.player.total_points >= service.cost:
                self.player.total_points -= service.cost
                self.player.update_stats(service.skill_boosts)
                print(f"You used {service.name} and improved your stats!")
            else:
                print("Not enough points to use this service.")
        else:
            print("Invalid choice. Returning to the menu.")

    # Display the help menu
    def display_help(self):
        print("\nHelp Menu:")
        print("1. Edit Info: Update your personal details.")
        print("2. Visit Spot: Go to a location to earn points.")
        print("3. Activity: Complete an activity to earn points and improve stats.")
        print("4. Stats: Check your stats, total points, and personal information.")
        print("5. Logs: See all activities you've done and spots you've visited.")
        print("6. Services: List of available services and their costs.")
        print("7. Use Svc: Spend points on a service to improve your stats.")
        print("8. Help: View this help menu.")
        print("9. Exit: Save your progress and exit the game.")

    # Main game loop
    def main_menu(self):
        self.display_menu()
        while True:
            choice = input("Choose an option (type 'menu' to see options again): ")

            if choice.lower() == "menu":
                self.display_menu()
            elif choice == "1":
                self.player.edit_info()
            elif choice == "2":
                self.visit_active_spot()
            elif choice == "3":
                self.perform_activity()
            elif choice == "4":
                self.view_stats()
            elif choice == "5":
                self.view_logs()
            elif choice == "6":
                self.view_services()
            elif choice == "7":
                self.use_service()
            elif choice == "8":
                self.display_help()
            elif choice == "9":
                print("Saving progress... Goodbye!")
                self.save_data()
                break
            else:
                print("Invalid choice. Please try again.")

# Start the game
if __name__ == "__main__":
    game = Game()
    game.main_menu()