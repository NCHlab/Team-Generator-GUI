import os
import json
import random
import tkinter as tk
from tkinter import messagebox


global_list = []
root = tk.Tk()
root.title("Team Generator")
frame1 = tk.LabelFrame(root, padx=5, pady=5)
frame1.grid(row=5, column =0)
frame2 = tk.LabelFrame(root, padx=5, pady=5) 
frame2.grid(row=5, column =1)
# frame2.pack(row=10, column=10)
# root.iconbitmap("./icons/icon.ico")

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
        self.chk = tk.Checkbutton(frame2, text=self.name, var=self._chk_state, command=lambda: self.check_active())
        self.chk.grid(column=self.column, row=self.row, sticky="w")
    
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

    team_list = team_data.get("names", [])
    num_of_team = team_data.get('numOfTeam',2) if type(team_data['numOfTeam']) == int else int(team_data.get('numOfTeam',2))

    return team_list, num_of_team


def generate_labels(n):

    for _ in range(n):
        label_object.append(tk.Label(frame1, text="", font=("Arial Bold", 10)))


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
        label_object[i].configure(text=", \n".join(shuffled_teams[i]))
        label_object[i].grid(column=column, row=row)
        row +=1

def change_settings():
    settings_window = tk.Toplevel()
    settings_window.title("Settings - Modify Team List")
    settings_window.geometry('400x300')

def generate_button(): 

    btn2 = tk.Button(root, text="GENERATE TEAMS", bg="#bbede8", fg="#0003c9",padx= 20, pady=14, command=display_list)
    btn2.grid(column=0, row=4)

    settings_btn = tk.Button(root, text="Settings", bg="#e0dcdd", fg="#ff195e",padx= 20, pady=14, command=change_settings)
    settings_btn.grid(column=1, row=4)


if __name__ == "__main__":

    if not os.path.exists("team_list.json"):
        messagebox.showwarning(title= "File does not exist", message="team_list.json does not exist. Please create this file :)")
        exit()

    team_list, num_of_team = initialise_data()
    generate_labels(num_of_team)
    generate_player(len(team_list))
    generate_button()

    root.geometry('800x720')
    root.mainloop()

# set it up so that a person enters the name into the file and then can adjust by ticking a box to select / deselect that person
# make selected people green + bold
# make unselected people black
# create an active list of names

# integrate into slack so it tells users the team & also say the number of regens made.

# error handling, remove arrays that have empty data
# error handling for file doesnt exist