import json

# Classes
class ActiveSpot:
    def __init__(self, id, name, location, type, available_activities, bonus_points):
        self.id = id
        self.name = name
        self.location = location
        self.type = type
        self.available_activities = available_activities
        self.bonus_points = bonus_points


class Activity:
    def __init__(self, id, name, skill_boosts, base_points, first_time_bonus, duration):
        self.id = id
        self.name = name
        self.skill_boosts = skill_boosts
        self.base_points = base_points
        self.first_time_bonus = first_time_bonus
        self.duration = duration


class Service:
    def __init__(self, id, name, skill_boosts, cost, linked_active_spot_id):
        self.id = id
        self.name = name
        self.skill_boosts = skill_boosts
        self.cost = cost
        self.linked_active_spot_id = linked_active_spot_id


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

    def update_stats(self, boosts):
        for boost in boosts:
            self.stats[boost] += 1


class Game:
    def __init__(self):
        self.active_spots = []
        self.activities = []
        self.services = []
        self.player = Player()
        self.load_data()
        self.create_player()

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

    def create_player(self):
        print("Welcome to ActiveQuest! Let's create your character.")
        self.player.name = input("Enter your name: ")
        self.player.age = int(input("Enter your age: "))
        self.player.height = int(input("Enter your height (in cm): "))
        self.player.weight = int(input("Enter your weight (in kg): "))
        print(f"Character created! Welcome, {self.player.name}!")

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

    def view_stats(self):
        print("\nPlayer Stats:")
        print(f"Name: {self.player.name}, Age: {self.player.age}, Height: {self.player.height} cm, Weight: {self.player.weight} kg")
        for stat, value in self.player.stats.items():
            print(f"{stat}: {value}")
        print(f"Total Points: {self.player.total_points}")

    def view_logs(self):
        print("\nActivity Log:")
        for entry in self.player.completed_activities:
            print(f"- {entry['name']}")
        print("\nVisited Spots:")
        for spot_id in self.player.visited_spots:
            spot = next((s for s in self.active_spots if s.id == spot_id), None)
            if spot:
                print(f"- {spot.name}")

    def display_help(self):
        print("\nHelp Menu:")
        print("1. Visit an Active Spot: Go to a place to earn points for visiting.")
        print("2. Perform an Activity: Choose and perform an activity to earn points and boost stats.")
        print("3. View Player Stats: Check your stats, points, and character info.")
        print("4. View Logs: See where you’ve been and what activities you’ve done.")
        print("5. Exit: Save your progress and exit the game.")
        print("Type 'help' at any time to see this menu again.")

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Visit an Active Spot")
            print("2. Perform an Activity")
            print("3. View Player Stats")
            print("4. View Logs")
            print("5. Exit")

            choice = input("Choose an option (or type 'help' for commands): ")

            if choice.lower() == "help":
                self.display_help()
            elif choice == "1":
                self.visit_active_spot()
            elif choice == "2":
                self.perform_activity()
            elif choice == "3":
                self.view_stats()
            elif choice == "4":
                self.view_logs()
            elif choice == "5":
                print("Saving progress... Goodbye!")
                self.save_data()
                break
            else:
                print("Invalid choice. Please try again.")

# Start the game
if __name__ == "__main__":
    game = Game()
    game.main_menu()