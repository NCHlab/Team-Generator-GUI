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


# label_object = list()
# player_checkbox = list()

class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, height=42, width=42)
        self.master = master
        master.title("Team Generator")

        self.frame1 = tk.LabelFrame(self.master, padx=5, pady=5)
        self.frame1.grid(row=5, column =0)

        self.frame2 = tk.LabelFrame(root, padx=5, pady=5) 
        self.frame2.grid(row=5, column =1)

        self.initialise_data()


    def load_data(self):

        try:
            with open("./team_list.json", "r") as wr:
                self.team_data = json.load(wr)
        except json.decoder.JSONDecodeError:
            messagebox.showerror(title= "File Format Incorrect", message="team_list.json Error, Please remove trailing comma from end of names & ensure it is JSON compliant")
            exit()

        self.team_data["names"] = list(map(lambda x: x.title(), self.team_data["names"]))

        self.team_list = self.team_data.get("names", [])
        self.num_of_team = self.team_data.get('numOfTeam',2) if type(self.team_data['numOfTeam']) == int else int(self.team_data.get('numOfTeam',2))


    def initialise_data(self):
        self.load_data()
        self.generate_labels()
        self.generate_player()
        self.generate_button()


    def generate_player(self):
        self.num_of_players = len(self.team_list)
        self.player_checkbox = list()

        column = 6 
        row = 5
        
        for i in range(self.num_of_players):
            self.player_checkbox.append(Person(column, row, self.team_list[i],self.frame2))
            row+=1


    def generate_labels(self):
        self.label_object = list()

        for _ in range(self.num_of_team):
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

        settings_btn = tk.Button(self.master, text="Settings", bg="#e0dcdd", fg="#ff195e",padx= 20, pady=14, command=lambda: self.change_settings())
        settings_btn.grid(column=1, row=4)


    def num_dropdown_widget(self):
        self.menu_opt = tk.IntVar()
        self.menu_opt.set(self.num_of_team)

        team_options = [2,3,4,5,6,7,8,9,10]

        dropdown_label = tk.Label(self.settings_window, text="Number of Teams")
        dropdown_label.grid(row=0, column=0)

        team_Dropdown = tk.OptionMenu(self.settings_window, self.menu_opt, *team_options)
        team_Dropdown.grid(row=0, column=1)

        update_btn = tk.Button(self.settings_window, text="Update", bg="#e0dcdd", fg="#ff195e",command=lambda: self.update_team_list("update"))
        update_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=60)

    def username_add_widget(self):
        username_label = tk.Label(self.settings_window, text="Username")
        username_label.grid(row=3, column=0)

        self.username = tk.Entry(self.settings_window, width=30)
        self.username.grid(row=3, column =1)

        add_btn = tk.Button(self.settings_window, text="Add User", bg="#e0dcdd", fg="#ff195e",command=lambda: self.update_team_list("add"))
        add_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=60)
    

    def username_del_widget(self):
        delete_user_label = tk.Label(self.settings_window, text="Delete User:")
        delete_user_label.grid(row=5, column=0)

        self.delete_user = tk.Entry(self.settings_window, width=30)
        self.delete_user.grid(row=5, column =1)

        delete_btn = tk.Button(self.settings_window, text="Delete User", bg="#e0dcdd", fg="#ff195e",command=lambda: self.update_team_list("delete"))
        delete_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=60)


    def change_settings(self):
        self.settings_window = tk.Toplevel(self)
        self.settings_window.title("Settings - Modify Team List")
        self.settings_window.geometry('400x300')

        self.num_dropdown_widget()
        self.username_add_widget()
        self.username_del_widget()


    def add_mode(self, data):
        new_data = self.username.get()
        self.username.delete(0, 'end')
        new_data = new_data.strip()

        if new_data.title() in map(lambda x:x.title(),data["names"]):
            self.updated_field = tk.Label(self.settings_window, text='Duplicate Error. Name Taken!', fg='red')
            self.updated_field.grid(row=4, column=3)
            self.updated_field.after(1500, self.updated_field.destroy)
        elif new_data:
            data["names"].append(new_data.title())
        else:
            self.updated_field = tk.Label(self.settings_window, text='Field is Empty', fg='red')
            self.updated_field.grid(row=4, column=3)
            self.updated_field.after(1000, self.updated_field.destroy)

        return data

    def delete_mode(self, data):
        user_to_delete = self.delete_user.get()
        self.delete_user.delete(0, 'end')
        user_to_delete = user_to_delete.strip()

        if user_to_delete.title() and user_to_delete.title() in data["names"]:
            data["names"].remove(user_to_delete.title())
        else:
            self.updated_field = tk.Label(self.settings_window, text='Delete Failed. Name not in List', fg='red')
            self.updated_field.grid(row=6, column=3)
            self.updated_field.after(1000, self.updated_field.destroy)

        return data

    def update_mode(self, data):
        self.num_of_team = self.menu_opt.get()
        data["numOfTeam"] = self.num_of_team
        self.updated_text = tk.Label(self.settings_window, text='Number Updated!', fg='green')
        self.updated_text.grid(row=1, column=3)
        self.updated_text.after(1000, self.updated_text.destroy)

        return data

    def update_team_list(self, mode="update"):

        data = json_local_load()
        data["names"] = list(map(lambda x: x.title(), data["names"]))

        if mode == "add":
            data = self.add_mode(data)
        elif mode == "delete":
            data = self.delete_mode(data)
        else:
            data = self.update_mode(data)
        
        json_local_write(data)

        if mode == "add" or mode == "delete":
            for i in self.player_checkbox:
                i.chk.destroy() # Remove Checkbox Instance

                if i.user_in_globallist():
                    i.deactivate_player()
                
            self.team_list = data["names"]
            del self.player_checkbox
            self.generate_player()



        for i in self.label_object:
            i.destroy() # Remove label instances

        self.generate_labels()





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

    def destroy_chk(self):
        return self.chk.destroy()
    
    def check_active(self):
        if self.name in global_list:
            self.deactivate_player()
        else:
            self.activate_player()
    
    def activate_player(self):
        global_list.append(self.name)
    
    def deactivate_player(self):
        global_list.remove(self.name)

    def user_in_globallist(self):
        return self.name in global_list


def split_list(seq, size):
    return (seq[i::size] for i in range(size))


def shuffle_teams(data, n):
    random.shuffle(data)
    teams = list(split_list(data, n))

    return teams


def json_local_load():
    json_file = open("team_list.json", "r")
    data = json.load(json_file) 
    json_file.close()

    return data


def json_local_write(data):
    json_file = open("team_list.json", "w+")
    json_file.write(json.dumps(data, indent=4))
    json_file.close()



if __name__ == "__main__":

    if not os.path.exists("team_list.json"):
        response = messagebox.askyesno(title= "File does not exist", message="team_list.json does not exist. Create this file now?")
        if response:
            with open("team_list.json", 'w') as write_file:
                json.dump({"names": [],"numOfTeam": 2}, write_file, indent=4)
        else:
            exit()

    
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