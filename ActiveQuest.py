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
        self.name = self.get_valid_name("Enter your name: ")
        self.age = self.get_valid_int("Enter your age: ", 1, 120)
        self.height = self.get_valid_int("Enter your height (in cm): ", 50, 250)
        self.weight = self.get_valid_int("Enter your weight (in kg): ", 10, 300)
        print("Player information updated successfully!")

    # Validate name input (allows letters and numbers)
    def get_valid_name(self, prompt):
        while True:
            name = input(prompt).strip()
            if len(name) > 0 and name.replace(" ", "").isalnum():
                return name
            print("Invalid name. Please enter a valid name (letters and numbers allowed).")

    # Validate integer inputs (e.g., age, height, weight)
    def get_valid_int(self, prompt, min_val, max_val):
        while True:
            try:
                value = int(input(prompt))
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"Please enter a value between {min_val} and {max_val}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

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
        try:
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

        except FileNotFoundError as e:
            print(f"Error: {e}. Make sure all required JSON files are present.")
            exit()
        except json.JSONDecodeError as e:
            print(f"Error loading data from JSON files: {e}")
            exit()

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

    # Create a new player
    def create_player(self):
        print("Welcome to ActiveQuest! Let's create your character.")
        self.player.name = self.player.get_valid_name("Enter your name: ")
        self.player.age = self.player.get_valid_int("Enter your age: ", 1, 120)
        self.player.height = self.player.get_valid_int("Enter your height (in cm): ", 50, 250)
        self.player.weight = self.player.get_valid_int("Enter your weight (in kg): ", 10, 300)
        print(f"Character created! Welcome, {self.player.name}!")

    # Display the menu
    def display_menu(self):
        print("\n******************************")
        print("1. Visit Spot  2. Perform Activity  3. Use Service")
        print("4. Player Stats  5. Log  6. Edit Info  7. Help  8. Exit")
        print("******************************")

    # Visit an active spot and earn points
    def visit_active_spot(self):
        if not self.active_spots:
            print("No active spots available. Please check your JSON data.")
            return

        while True:
            print("\nAvailable Active Spots:")
            for spot in self.active_spots:
                print(f"{spot.id}. {spot.name} ({spot.type}) - Bonus Points: {spot.bonus_points}")

            choice = input("Enter the number of the active spot you want to visit (or 'back' to return): ")
            if choice.lower() == "back":
                return

            try:
                spot = next((s for s in self.active_spots if str(s.id) == choice), None)
                if spot:
                    if spot.id not in self.player.visited_spots:
                        print(f"You visited {spot.name} for the first time! You earned {spot.bonus_points} points!")
                        self.player.total_points += spot.bonus_points
                        self.player.visited_spots.add(spot.id)
                    else:
                        print(f"You revisited {spot.name}.")
                else:
                    print("Invalid choice. Spot not found.")
            except Exception as e:
                print(f"An error occurred while visiting the spot: {e}")

    # Perform an activity and earn points
    def perform_activity(self):
        if not self.activities:
            print("No activities available. Please check your JSON data.")
            return

        while True:
            print("\nAvailable Activities:")
            for activity in self.activities:
                print(f"{activity.id}. {activity.name} - Base Points: {activity.base_points}, First-Time Bonus: {activity.first_time_bonus}")

            choice = input("Enter the number of the activity you want to perform (or 'back' to return): ")
            if choice.lower() == "back":
                return

            try:
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
                    print("Invalid choice. Activity not found.")
            except Exception as e:
                print(f"An error occurred while performing the activity: {e}")

    # Use a service to improve stats
    def use_service(self):
        if not self.services:
            print("No services available. Please check your JSON data.")
            return

        while True:
            print("\nAvailable Services:")
            for service in self.services:
                print(f"{service.id}. {service.name} - Cost: {service.cost} points")

            choice = input("Enter the number of the service you want to use (or 'back' to return): ")
            if choice.lower() == "back":
                return

            try:
                service = next((s for s in self.services if str(s.id) == choice), None)
                if service:
                    if self.player.total_points >= service.cost:
                        self.player.total_points -= service.cost
                        self.player.update_stats(service.skill_boosts)
                        print(f"You used {service.name} and improved your stats!")
                    else:
                        print("Not enough points to use this service.")
                else:
                    print("Invalid choice. Service not found.")
            except Exception as e:
                print(f"An error occurred while using the service: {e}")

    # Display the help menu
    def display_help(self):
        print("\nHelp Menu:")
        print("1. Visit Spot: Go to a location to earn points.")
        print("2. Perform Activity: Complete an activity to earn points and improve stats.")
        print("3. Use Service: Spend points on a service to improve your stats.")
        print("4. Player Stats: Check your stats, total points, and personal information.")
        print("5. Log: See all activities you've done and spots you've visited.")
        print("6. Edit Info: Update your personal details.")
        print("7. Help: View this help menu.")
        print("8. Exit: Save your progress and exit the game.")

    # Main game loop
    def main_menu(self):
        self.display_menu()
        while True:
            choice = input("Choose an option (type 'menu' to see options again): ")

            if choice.lower() == "menu":
                self.display_menu()
            elif choice == "1":
                self.visit_active_spot()
            elif choice == "2":
                self.perform_activity()
            elif choice == "3":
                self.use_service()
            elif choice == "4":
                self.view_stats()
            elif choice == "5":
                self.view_logs()
            elif choice == "6":
                self.player.edit_info()
            elif choice == "7":
                self.display_help()
            elif choice == "8":
                print("Saving progress... Goodbye!")
                self.save_data()
                break
            else:
                print("Invalid choice. Please try again.")

# Start the game
if __name__ == "__main__":
    game = Game()
    game.main_menu()