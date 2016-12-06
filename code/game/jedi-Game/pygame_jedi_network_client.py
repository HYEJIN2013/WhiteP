def send_json():
    pass

def recieve_json():
    pass

# send username and password
def login(username, password):
    pass

# read character data
def read_character_data():
    pass

# read character data
def read_combat_results():
    json_data = recieve_json()
    {
        
    }

# send our move choice
def send_combat_move(move_name, character_name, hit_points, force_points, expected_die):
    json_data = {'move':{
        'MoveName':move_name,
        'CharName':character_name,
        'HP': hit_points,
        'FP': force_points,
        'expected die': expected_die
    }}
    send_json(json_data)
