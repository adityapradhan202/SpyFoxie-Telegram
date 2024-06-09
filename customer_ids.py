import random

customer_id_pass = {
    "carot7654":"jazzy@quilt73",
    "pumpkin_fox378":"mystic#pond89",
    "spyfox4309":"brisk$valley42",
    "spooky_predator7212":"fable@thorn61",
    "wacky_esper621":"ivid#clerk58"
}

def random_id():
    keys = list(customer_id_pass.keys())
    rand_index = random.randint(0, len(keys)-1)
    
    chosen_id = keys[rand_index]
    return chosen_id

def id_password(pswd):
    corres_pass = customer_id_pass[pswd]
    return corres_pass

