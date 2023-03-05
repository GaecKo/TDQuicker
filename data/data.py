import json
FILE = "data/data.json"

def write_content(content: dict):
    with open(FILE, 'w') as f:
        json.dump(content, f, indent=4)

def load_content() -> dict:
    with open(FILE, 'r') as f:
        return json.load(f)

def save_task(task_text: str, date: str):
    data = load_content()
    data["todo"][task_text] = date
    write_content(data)

def delete_task(task_text: str, state: bool):
    data = load_content()
    if state:
        state = "done"
    else:
        state= "todo"
    del data[state][task_text]
    write_content(data)

def move_saved_task(task_text: str, new_state: bool):
    # new state: true = it has been done; false = it has to be done
    if new_state:
        bef_state, new_state = "todo", "done"
    else:
        bef_state, new_state = "done", "todo"
    
    data = load_content()
    # {'done': {'task_text': '22/05'}, 'todo': {'task_text': '23/05'}}

    task_date = data[bef_state][task_text]
    del data[bef_state][task_text]
    data[new_state][task_text] = task_date

    write_content(data)

