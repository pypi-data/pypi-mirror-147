import json
print(json.__file__)
data = {
    "student": {
        "name": "Maria Markevich",
        "number group": "INBO-05-20"
    },

    "Task": {
        "number practice": 3,
        "number": 5,
        "level": "VERYYY HAAAAAAAAAAAARD"
    }
}

with open("data.json", "w") as file:
    json.dump(data, file)

