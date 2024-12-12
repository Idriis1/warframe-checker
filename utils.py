def load_items_from_file(filename="list.txt"):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{filename} not found. Using empty list.")
        return []
