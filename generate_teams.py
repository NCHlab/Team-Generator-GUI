import os
import json
import random
import tkinter as tk
from tkinter import messagebox


global_list = []
root = tk.Tk()
# root.title("Team Generator")
# frame1 = tk.LabelFrame(root, padx=5, pady=5)
# frame1.grid(row=5, column =0)
# frame2 = tk.LabelFrame(root, padx=5, pady=5) 
# frame2.grid(row=5, column =1)
# frame2.pack(row=10, column=10)
# root.iconbitmap("./icons/icon.ico")

team_data = {}
label_object = list()
player_checkbox = list()

class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, height=42, width=42)
        self.master = master
        master.title("Team Generator")

        self.team_list = None
        self.num_of_team = None
        self.num_of_players = None
        self.label_object = list()
        self.player_checkbox = list()
        self.shuffled_teams = list()

        self.frame1 = tk.LabelFrame(self.master, padx=5, pady=5)
        self.frame1.grid(row=5, column =0)

        self.frame2 = tk.LabelFrame(root, padx=5, pady=5) 
        self.frame2.grid(row=5, column =1)

        self.initialise_data()


    def load_data(self):


        with open("./team_list.json", "r") as wr:
            team_data = json.load(wr)

        self.team_list = team_data.get("names", [])
        self.num_of_team = team_data.get('numOfTeam',2) if type(team_data['numOfTeam']) == int else int(team_data.get('numOfTeam',2))


    def initialise_data(self):

        self.load_data()
        self.generate_labels(self.num_of_team)
        self.generate_player()
        self.generate_button()

    def generate_player(self):

        column = 6
        row = 5
        self.num_of_players = len(self.team_list)

        for i in range(self.num_of_players):
            self.player_checkbox.append(Person(column, row, self.team_list[i],self.frame2))
            row+=1

    def generate_labels(self, n):

        for _ in range(n):
            self.label_object.append(tk.Label(self.frame1, text="", font=("Arial Bold", 10)))

    def display_list(self):

        self.shuffled_teams = shuffle_teams(global_list, self.num_of_team)
        print(self.shuffled_teams)

        column = 1
        row = 7

        for i in range(self.num_of_team):
            # label_object[i].configure(text=", \n".join(shuffled_teams[i]))
            self.label_object[i].configure(text=str(self.shuffled_teams[i]))
            self.label_object[i].grid(column=column, row=row)
            row +=1


    def generate_button(self): 

        btn2 = tk.Button(self.master, text="GENERATE TEAMS", bg="#bbede8", fg="#0003c9",padx= 20, pady=14, command=lambda: self.display_list())
        btn2.grid(column=0, row=4)




class Person():
    def __init__(self, column, row, name, frame2):
        self.row = row
        self.column = column
        self.name = name
        self._team = None
        self.frame2 = frame2


        self._chk_state = tk.BooleanVar()
        self._chk_state.set(False)
        self.chk = tk.Checkbutton(self.frame2, text=self.name, var=self._chk_state, command=lambda: self.check_active())
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







def change_settings(num_of_team):
    settings_window = tk.Toplevel()
    settings_window.title("Settings - Modify Team List")
    settings_window.geometry('400x300')

    menu_opt = tk.IntVar()
    menu_opt.set(num_of_team)

    team_options = [2,3,4,5,6,7,8,9,10]

    dropdown_label = tk.Label(settings_window, text="Last Name")
    dropdown_label.grid(row=0, column=0)

    team_Dropdown = tk.OptionMenu(settings_window, menu_opt, *team_options)
    team_Dropdown.grid(row=0, column=1)

    update_btn = tk.Button(settings_window, text="Update", bg="#e0dcdd", fg="#ff195e",command=lambda: update_team_list(menu_opt.get(), "update"))
    update_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=60)


    username_label = tk.Label(settings_window, text="Last Name")
    username_label.grid(row=2, column=0)

    username = tk.Entry(settings_window, width=30)
    username.grid(row=2, column =1)

    add_btn = tk.Button(settings_window, text="Add User", bg="#e0dcdd", fg="#ff195e",command=lambda: update_team_list(username.get(), "add"))
    add_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=60)


    def update_team_list(new_data, mode="update"):

        json_file = open("team_list.json", "r")
        data = json.load(json_file) 
        json_file.close()

        if mode == "add":
            username.delete(0, 'end')
            new_data = new_data.strip()
            if new_data:
                data["names"].append(new_data)
            else:
                return
        elif mode == "delete":
            pass
        else:
            data["numOfTeam"] = new_data


        json_file = open("team_list.json", "w+")
        json_file.write(json.dumps(data, indent=4))
        json_file.close()




# def generate_button(num_of_team): 

#     btn2 = tk.Button(root, text="GENERATE TEAMS", bg="#bbede8", fg="#0003c9",padx= 20, pady=14, command=lambda: display_list(num_of_team))
#     btn2.grid(column=0, row=4)

    # settings_btn = tk.Button(root, text="Settings", bg="#e0dcdd", fg="#ff195e",padx= 20, pady=14, command=lambda: change_settings(num_of_team))
    # settings_btn.grid(column=1, row=4)



if __name__ == "__main__":

    if not os.path.exists("team_list.json"):
        response = messagebox.askyesno(title= "File does not exist", message="team_list.json does not exist. Create this file now?")
        print(response)
        if response:
            with open("team_list.json", 'w') as write_file:
                json.dump({"names": [],"numOfTeam": 2}, write_file, indent=4)
        else:
            exit()

    
    # initialise_data()
    # App((root).pack(side="top", fill="both", expand=True))
    obj = App(root)
    root.geometry('800x720')
    root.mainloop()

# set it up so that a person enters the name into the file and then can adjust by ticking a box to select / deselect that person
# make selected people green + bold
# make unselected people black
# create an active list of names

# integrate into slack so it tells users the team & also say the number of regens made.

# error handling, remove arrays that have empty data
# error handling for file doesnt exist