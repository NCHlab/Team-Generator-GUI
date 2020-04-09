import json
import random
import tkinter as tk
# from tkinter import *
# from tkinter.ttk import *


global_list = []

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




window = tk.Tk()

window.title("Team Fortress 2 Team Picker")

team_data = {}
num_team_data = list()


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))

# def split_list(data):
#     half = len(data)//2
#     return data[:half], data[half:]

# def shuffle_teams(data):
#     random.shuffle(data)
#     blue_team, red_team = split_list(data)

#     return blue_team, red_team

def shuffle_teams(data, n):
    random.shuffle(data)
    teams = list(chunker_list(data, n))

    return teams

with open("./team_list.json", "r") as wr:
    team_data = json.load(wr)

team_list = team_data["names"]
num_of_team = team_data['numOfTeam'] if type(team_data['numOfTeam']) == int else int(team_data['numOfTeam'])

# print(num_of_team)

for i in range(num_of_team):
    num_team_data.append(tk.Label(window, text="", font=("Arial Bold", 10)))

# Team1 = tk.Label(window, text="", font=("Arial Bold", 10))
# Team2 = tk.Label(window, text="", font=("Arial Bold", 10))

    

# btn = tk.Button(window, text="Generate", bg="#000000", fg="red", command=lambda: shuffle_teams(team_data, num_of_team))
# btn.grid(column=1, row=0)


objs = list()
column = 6
row = 5

for i in range(len(team_list)):
    
    objs.append(Person(column, row, team_list[i]))
    row+=1


def display_list():

    test2 = shuffle_teams(global_list, num_of_team)
    print(test2)

    column = 1
    row = 7

    for i in range(num_of_team):
        num_team_data[i].configure(text=str(test2[i]))
        num_team_data[i].grid(column=column, row=row)
        row +=1

    

    # lbl.configure(text=str(test2[0]))
    # lbl.grid(column=1, row=7)

    # lbl2.configure(text=str(test2[1]))
    # lbl2.grid(column=1, row=8)


# def display_list():

#     test2 = shuffle_teams(global_list)

#     lbl.configure(text=str(test2[0]))
#     lbl.grid(column=1, row=7)

#     lbl2.configure(text=str(test2[1]))
#     lbl2.grid(column=1, row=8)
    

btn2 = tk.Button(window, text="GENERATE TEAMS", bg="#bbede8", fg="#0003c9", command=display_list)
btn2.grid(column=1, row=4)


if __name__ == "__main__":
    window.geometry('800x720')
    window.mainloop()

# set it up so that a person enters the name into the file and then can adjust by ticking a box to select / deselect that person
# make selected people green + bold
# make unselected people black
# create an active list of names

# integrate into slack so it tells users the team & also say the number of regens made.

# error handling, remove arrays that have empty data
# error handling for file doesnt exist