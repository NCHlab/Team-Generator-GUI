import json
import random
import tkinter as tk


global_list = []
window = tk.Tk()
window.title("Team Generator")

team_data = {}
label_object = list()
player_checkbox = list()


# class TeamPicker():
#     def __init__(self):
#         self.t = t

class Person():
    def __init__(self, column, row, name):
        self.row = row
        self.column = column
        self.name = name
        self._team = None


        self._chk_state = tk.BooleanVar()
        self._chk_state.set(False)
        self.chk = tk.Checkbutton(window, text=self.name, var=self._chk_state, command=lambda: self.check_active())
        self.chk.grid(column=self.column, row=self.row)
    
    def check_active(self):
        if self.name in global_list:
            self.deactivate_player()
        else:
            self.activate_player()
    
    def activate_player(self):
        global_list.append(self.name)
    
    def deactivate_player(self):
        global_list.remove(self.name)


def split_list(seq, size):
    return (seq[i::size] for i in range(size))


def shuffle_teams(data, n):
    random.shuffle(data)
    teams = list(split_list(data, n))

    return teams


def initialise_data():

    with open("./team_list.json", "r") as wr:
        team_data = json.load(wr)

    team_list = team_data["names"]
    num_of_team = team_data['numOfTeam'] if type(team_data['numOfTeam']) == int else int(team_data['numOfTeam'])

    return team_list, num_of_team


def generate_labels(n):

    for _ in range(n):
        label_object.append(tk.Label(window, text="", font=("Arial Bold", 10)))


def generate_player(num_of_players):

    column = 6
    row = 5
    for i in range(num_of_players):       
        player_checkbox.append(Person(column, row, team_list[i]))
        row+=1


def display_list():

    shuffled_teams = shuffle_teams(global_list, num_of_team)
    print(shuffled_teams)

    column = 1
    row = 7

    for i in range(num_of_team):
        label_object[i].configure(text=str(shuffled_teams[i]))
        label_object[i].grid(column=column, row=row)
        row +=1


def generate_button(): 

    btn2 = tk.Button(window, text="GENERATE TEAMS", bg="#bbede8", fg="#0003c9", command=display_list)
    btn2.grid(column=5, row=4)


if __name__ == "__main__":
    team_list, num_of_team = initialise_data()
    generate_labels(num_of_team)
    generate_player(len(team_list))
    generate_button()

    window.geometry('800x720')
    window.mainloop()

# set it up so that a person enters the name into the file and then can adjust by ticking a box to select / deselect that person
# make selected people green + bold
# make unselected people black
# create an active list of names

# integrate into slack so it tells users the team & also say the number of regens made.

# error handling, remove arrays that have empty data
# error handling for file doesnt exist