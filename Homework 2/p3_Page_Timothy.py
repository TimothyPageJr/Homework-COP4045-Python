# Timothy Page  Problem 3
import csv

def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Add a user to the social network."""
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except Exception as error:
        print(f"Error adding user: {error}")
        raise

def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """Add a mutual friend link."""
    try:
        if user1 not in sn or user2 not in sn:
            return False
        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)
        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)
        return True
    except Exception as error:
        print(f"Error adding friend: {error}")
        raise

def get_friends(sn: dict, user1: str, distance: int) -> list:
    """Return friends within the given distance."""
    try:
        if user1 not in sn or distance <= 0:
            return []
        visited, current, result = {user1}, [user1], []
        for _ in range(distance):
            next_level = []
            for user in current:
                for friend in sn[user][1]:
                    if friend not in visited:
                        visited.add(friend)
                        result.append(friend)
                        next_level.append(friend)
            current = next_level
        return result
    except Exception as error:
        print(f"Error getting friends: {error}")
        raise

def save_network(filename: str, sn: dict) -> None:
    """Save the social network to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for username, (fullname, friends) in sn.items():
                writer.writerow([username, fullname] + friends)
    except Exception as error:
        print(f"Error saving network: {error}")
        raise

def load_network(filename: str) -> dict:
    """Load a social network from a CSV file."""
    try:
        sn = {}
        with open(filename, "r", newline="", encoding="utf-8") as file:
            for row in csv.reader(file):
                sn[row[0]] = (row[1], row[2:])
        return sn
    except Exception as error:
        print(f"Error loading network: {error}")
        raise

def main() -> None:
    """Test all social network functions."""
    print("Timothy Page - Problem 3")
    sn = {}

    print("\nA - Add Users")
    for user, name in [("alice", "Alice Smith"), ("maria", "Maria Cortez"),
                       ("joe", "Joseph Adams"), ("eve", "Evelyn Cooper"),
                       ("david", "David Benson")]:
        print(add_user(sn, user, name))

    print("\nB - Add Friends")
    for user1, user2 in [("alice", "maria"), ("maria", "joe"),
                         ("maria", "david"), ("joe", "eve")]:
        print(add_friend(sn, user1, user2))

    print("\nC - Get Friends")
    print(get_friends(sn, "alice", 1))
    print(get_friends(sn, "alice", 2))

    print("\nD - Save Network")
    save_network("social_network.csv", sn)
    print("Network saved.")

    print("\nE - Load Network")
    print(load_network("social_network.csv"))

if __name__ == "__main__":
    main()