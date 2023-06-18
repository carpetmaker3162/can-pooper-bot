import json

def update_data(data):
    with open("src/data.json", "w") as file:
        file.write(json.dumps(data))

def load_data():
    with open("src/data.json", "r") as file:
        return json.loads(file.read())

"""
def add_score(id: int, score: int):
    data = load_data()
    data[str(id)]["score"] = data[str(id)]["score"] + score
    update_data(data)

def remove_score(id: int, score: int):
    add_score(id, score * -1)
"""

if __name__ == "__main__":
    # Fetch dict of user id 1
    print(load_data()["1"])

    # Fetch dict of user id 2
    print(load_data()["2"]["score"])
    
    # Print again
    print(load_data()["2"]["score"])
