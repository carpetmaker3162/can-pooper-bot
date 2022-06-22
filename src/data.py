import json

def update_data(data, path="data.json"):
    with open(path, "w") as file:
        json.dump(data, file)

def load_data(path="data.json"):
    with open(path, "r") as file:
        return json.loads(file.read())

def add_score(id: int, score: int):
    data = load_data()
    data[str(id)]["score"] = data[str(id)]["score"] + score
    update_data(data)

def remove_score(id: int, score: int):
    add_score(id, score * -1)

if __name__ == "__main__":
    # Fetch dict of user id 1
    print(load_data()["1"])

    # Fetch dict of user id 2
    print(load_data()["2"]["score"])

    # Add 20 score to user id 2
    add_score(2, 20)
    
    # Print again
    print(load_data()["2"]["score"])
