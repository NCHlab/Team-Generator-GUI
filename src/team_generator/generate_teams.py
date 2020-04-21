import os
import json
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from sys import exit
import requests

global_list = []
root = tk.Tk()


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        # master.iconbitmap("./icons/icon.ico")
        master.title("Team Generator")

        # CheckBoxes
        self.frame2 = tk.LabelFrame(self.master, padx=5, pady=5, relief="solid") 
        self.frame2.grid(row=1, column=1, sticky="nsew")

        # Grid Organisation
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=0)
        self.master.grid_columnconfigure(2, weight=1)

        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=0)
        self.master.grid_rowconfigure(2, weight=0)
        self.master.grid_rowconfigure(3, weight=0)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_rowconfigure(5, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_rowconfigure(7, weight=1)
        self.master.grid_rowconfigure(8, weight=1)
        self.master.grid_rowconfigure(9, weight=1)
        self.master.grid_rowconfigure(10, weight=1)

        self.initialise_data()
        
    
    def initialise_data(self):

        self.load_menubar()
        self.load_data()
        self.generate_frame_labels() # frame1+
        self.generate_labels()
        self.generate_player()
        self.generate_button()


    def load_menubar(self):
        menubar = tk.Menu(self.master)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        submenu = tk.Menu(filemenu, tearoff=0)
        settingsmenu = tk.Menu(menubar, tearoff=0)
        helpmenu = tk.Menu(menubar, tearoff=0)

        filemenu.add_cascade(label='Import', menu=submenu)
        submenu.add_command(label="JSON File", command=lambda: self.import_custom_file())
        
        filemenu.add_command(label="Generate Teams", command=lambda: self.display_list())
        filemenu.add_command(label="Options", command=lambda: self.team_options())
        filemenu.add_separator()
        filemenu.add_command(label="Send To Slack", command=lambda: self.process_for_slack())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command= lambda: exit(0))
        
        settingsmenu.add_command(label="Generate Empty List (JSON)", command=lambda: create_new_jsonfile("regen"))
        settingsmenu.add_command(label="Modify Json File (Advanced)", command=lambda: messagebox.showinfo(title="!", message="Work In Progress, Coming Soon!"))
        settingsmenu.add_command(label="Set Slack Key", command=lambda: self.set_slack_key())

        helpmenu.add_command(label="How To Use", command=lambda: 1+1)
        helpmenu.add_separator()
        helpmenu.add_command(label="About", command=lambda: self.about_me())

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Settings", menu=settingsmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)


    def about_me(self):
        messagebox.showinfo(title="Thanks for using!", message="App Created Using TKinter.\nAuthor: Nayam Chowdhury\nWebsite: http://nayamc.com")


    def load_data(self):

        try:
            with open("./team_list.json", "r") as wr:
                self.team_data = json.load(wr)
        except json.decoder.JSONDecodeError:
            messagebox.showerror(title= "File Format Incorrect", message="team_list.json Error, Please remove trailing comma from end of names & ensure it is JSON compliant")
            response = messagebox.askyesno(title= "", message="Create a new team_list.json?")
            file_error(response)
            with open("./team_list.json", "r") as wr:
                self.team_data = json.load(wr)

        # Format the data into Capital Letter for first letter: User.Smith
        self.team_data["names"] = list(map(lambda x: x.title(), self.team_data["names"]))
        self.team_data["balance"] = list(map(lambda x: x.title(), self.team_data["balance"]))

        self.team_list = self.team_data.get("names", [])
        self.team_list_balance = self.team_data.get("balance", [])
        self.num_of_team = self.team_data.get('numOfTeam',2) if type(self.team_data['numOfTeam']) == int else int(self.team_data.get('numOfTeam',2))

        if not self.team_list: # Option menu provided to add new users
            self.team_options()


    def import_custom_file(self):

        ftypes = [('Json files', '*.json')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        file_dir = dlg.show()

        if file_dir != '':
            data = json_local_load(file_dir)
            if "names" in data and "numOfTeam" in data:
                json_local_write(data)
                self.refresh_ui(data)
                messagebox.showinfo(title= "Import Complete", message="File imported. The new settings file (team_list.json) can be found in the same directory as this program")
            else:
                messagebox.showerror(title="Error", message="Uploaded JSON file format incorrect. Please ensure 'names' and 'numOfTeam' fields are present.")

            

    def generate_frame_labels(self):
        self.team_obj = []

        row=4
        column = 0

        for i in range(self.num_of_team):
            if self.num_of_team == 2:
                self.team_obj.append(tk.LabelFrame(self.master, padx=5, pady=5, relief="flat"))
                self.team_obj[i].grid(row=row, column=column, sticky="nesw")
                column+=2
            else:
                if i%3 == 0:
                    column=0
                    row+=1
                self.team_obj.append(tk.LabelFrame(self.master, padx=5, pady=5, relief="flat"))
                self.team_obj[i].grid(row=row, column=column, sticky="nesw")
                column+=1


    def generate_labels(self):
        self.label_object = list()

        for i in range(self.num_of_team):
            self.label_object.append(tk.Label(self.team_obj[i], text="", font=("Arial Bold", 10)))


    def generate_player(self):
        self.num_of_players = len(self.team_list)
        self.player_checkbox = list()

        column = 6 
        row = 5
        
        for i in range(self.num_of_players):
            if i%10 == 0:
                column+=1
                row=5
            self.player_checkbox.append(Person(column, row, self.team_list[i],self.frame2))
            row+=1

    def set_slack_key(self):

        def set_key():
            os.environ['SLACK_KEY2'] = self.slack_key_field.get()
            self.slack_key_window.geometry('220x100')
            self.field_text(self.slack_key_window, text='Key Set!', fg='green',row=2, column=0, timeout=1500)
            self.slack_key_field.delete(0, 'end')
            
        self.slack_key_window = tk.Toplevel(self)
        self.slack_key_window.title("Set Key")
        self.slack_key_window.geometry('220x70')
        self.slack_key_window.attributes('-topmost', True) # Add infront at all times
        self.slack_key_window.update()

        self.slack_key_field = tk.Entry(self.slack_key_window, width=30)
        self.slack_key_field.grid(row=0, column =0)

        add_key_btn = ttk.Button(self.slack_key_window, text="Add Slack Key",command=lambda: set_key())
        add_key_btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=60)

        



    def process_for_slack(self):
        if hasattr(self, 'shuffled_teams'):
            response = send_to_slack(self.shuffled_teams)
            if response == "Fail":
                messagebox.showwarning(title="Slack Message Failed", message="Please Set OS Environment Variable (Settings > Add Slack Key)")
        else:
            messagebox.showwarning(title="Players not generated", message="Please Generate a team first.")

    def display_list(self):

        self.shuffled_teams = shuffle_teams(global_list, self.num_of_team, self.team_list_balance)
        colours = ["blue","red","green","#d69e02","#ff3df9","#00c9c9","black","purple","#bab700","#c900b2"]

        if self.num_of_team > 10:
            colours = colours + [random.choice(colours) for x in range(self.num_of_team)]

        column = 1
        row = 7

        for i in range(self.num_of_team):
            self.label_object[i].configure(text=f"TEAM {i+1}\n"+"\n".join(self.shuffled_teams[i]), fg=colours[i], anchor="w")
            self.label_object[i].grid(column=column, row=row, sticky="e")
            self.label_object[i].configure(anchor="center")
            row +=1


    def generate_button(self): 
        self.btnselectboxes = tk.StringVar()
        self.btnselectboxes.set("Select All")

        btn2 = ttk.Button(self.master, text="Generate Teams", command=lambda: self.display_list())
        btn2.grid(column=1, row=2)

        settings_btn = ttk.Button(self.master, text="Team Options", command=lambda: self.team_options())
        settings_btn.grid(column=1, row=3)

        select_btn = ttk.Button(self.master, textvariable=self.btnselectboxes, command=lambda: self.select_deselect_checkboxes())
        select_btn.grid(column=1, row=0)
    
    
    def select_deselect_checkboxes(self):
        
        if self.btnselectboxes.get() == "Select All":
            self.btnselectboxes.set("DeSelect All")
                
            for i in self.player_checkbox:
                i._chk_state.set(True)
                i.activate_player()

        else:
            self.btnselectboxes.set("Select All")

            for i in self.player_checkbox:
                i._chk_state.set(False)
                i.deactivate_player()


    def team_options(self):
        self.options_window = tk.Toplevel(self)
        self.options_window.title("Options - Modify Team List")
        self.options_window.geometry('400x300')
        self.options_window.attributes('-topmost', True) # Add infront at all times
        self.options_window.update()

        self.num_dropdown_widget()
        self.username_add_widget()
        self.username_del_widget()


    def num_dropdown_widget(self):
        self.menu_opt = tk.IntVar()
        self.menu_opt.set(self.num_of_team)

        def alwaysActiveStyle(widget):
            widget.config(state="active")
            widget.bind("<Leave>", lambda e: "break")


        s = ttk.Style(self.master)
        s.configure('N.TButton', foreground='black')

        team_options_list = [2,3,4,5,6,7,8,9,10]

        dropdown_label = tk.Label(self.options_window, text="Number of Teams")
        dropdown_label.grid(row=0, column=0)

        team_Dropdown = ttk.OptionMenu(self.options_window, self.menu_opt, "Choose", *team_options_list)
        alwaysActiveStyle(team_Dropdown)
        team_Dropdown.grid(row=0, column=1)
        team_Dropdown.focus()

        update_btn = ttk.Button(self.options_window, text="Update",command=lambda: self.update_team_list("update"))
        update_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=60)


    def username_add_widget(self):
        username_label = tk.Label(self.options_window, text="Username")
        username_label.grid(row=3, column=0)

        self.username = tk.Entry(self.options_window, width=30)
        self.username.grid(row=3, column =1)

        add_btn = ttk.Button(self.options_window, text="Add User",command=lambda: self.update_team_list("add"))
        add_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=60)
    

    def username_del_widget(self):
        delete_user_label = tk.Label(self.options_window, text="Delete User:")
        delete_user_label.grid(row=5, column=0)

        self.delete_user = tk.Entry(self.options_window, width=30)
        self.delete_user.grid(row=5, column =1)

        delete_btn = ttk.Button(self.options_window, text="Delete User",command=lambda: self.update_team_list("delete"))
        delete_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=60)


    def field_text(self, window, text, fg, row, column, timeout):
        self.updated_field = tk.Label(window, text=text, fg=fg)
        self.updated_field.grid(row=row, column=column)
        self.updated_field.after(timeout, self.updated_field.destroy)
    

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
            self.refresh_ui(data)
        else:
            self.refresh_labels()


    def add_mode(self, data):
        new_data = self.username.get()
        self.username.delete(0, 'end')
        new_data = new_data.strip()

        if new_data.title() in map(lambda x:x.title(),data["names"]):
            self.field_text(self.options_window, text='Duplicate Error. Name Taken!', fg='red',row=4, column=3, timeout=1500)
        elif new_data:
            data["names"].append(new_data.title())
            self.field_text(self.options_window, text='User Added', fg='green',row=4, column=3, timeout=1000)
        else:
            self.field_text(self.options_window, text='Field is Empty', fg='red',row=4, column=3, timeout=1000)

        self.username.focus_set()
        return data


    def delete_mode(self, data):
        user_to_delete = self.delete_user.get()
        self.delete_user.delete(0, 'end')
        user_to_delete = user_to_delete.strip()

        if user_to_delete.title() and user_to_delete.title() in data["names"]:
            data["names"].remove(user_to_delete.title())
            self.field_text(self.options_window, text='User Deleted.', fg='green',row=6, column=3, timeout=1000)
        else:
            self.field_text(self.options_window, text='Delete Failed. Name not in List', fg='red',row=6, column=3, timeout=1000)

        self.delete_user.focus_set()
        return data


    def update_mode(self, data):
        self.num_of_team = self.menu_opt.get()
        data["numOfTeam"] = self.num_of_team
        self.field_text(self.options_window, text='Number Updated!', fg='green',row=1, column=3, timeout=1000)

        return data


    def refresh_ui(self, data):

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
        
    

    def refresh_labels(self):
        for i in self.team_obj:
            i.destroy()

        for i in self.label_object:
                i.destroy() # Remove label instances

        self.generate_frame_labels()
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
        if self.name not in global_list:
            global_list.append(self.name)
    
    def deactivate_player(self):
        if self.name in global_list:
            global_list.remove(self.name)

    def user_in_globallist(self):
        return self.name in global_list


def split_list(seq, size):
    return (seq[i::size] for i in range(size))


def shuffle_teams(data, num_of_team, players_to_balance):

    # Create copy to not affect global / class instance
    data = data.copy()
    players_to_balance = players_to_balance.copy()

    # Ensure Players are selected
    if players_to_balance and data:

        temp_list = []

        for player in players_to_balance:
            # Remove duplicates from list
            if player in data:
                data.remove(player)
            else:
                # Save to remove from balance list
                temp_list.append(player)

        # Remove from playing since they arent in data
        for player in temp_list:
            players_to_balance.remove(player)

        random.shuffle(data)
        teams = list(split_list(data, num_of_team))

        random.shuffle(players_to_balance)
        teams_balanced = list(split_list(players_to_balance, num_of_team))

        # Add balanced players back into team
        # As balanced players added to end, Shuffling to make GUI randomize list
        for i in range(num_of_team):
            teams[i] += teams_balanced[i]
            random.shuffle(teams[i])

    else:
        random.shuffle(data)
        teams = list(split_list(data, num_of_team))

    return teams


def json_local_load(*args):

    if args:
        file_path = args[0]
        json_file = open(file_path, "r")
    else:
        json_file = open("team_list.json", "r")

    data = json.load(json_file) 
    json_file.close()

    return data


def json_local_write(data):
    json_file = open("team_list.json", "w+")
    json_file.write(json.dumps(data, indent=4))
    json_file.close()


def create_new_jsonfile(*args):
    with open("team_list.json", 'w') as write_file:
        json.dump({"names": [],"numOfTeam": 2,"balance": []}, write_file, indent=4)
    
    if args:
        obj.refresh_ui({"names": [],"numOfTeam": 2,"balance": []})
        obj.team_options()


def file_error(response):
    
    if response:
        create_new_jsonfile()
    else:
        exit(0)

def send_to_slack(data):
    try:
        slack_key = os.environ['SLACK_KEY2']
    except KeyError:
        return "Fail"

    url = "https://hooks.slack.com/services/"+slack_key
    
    for e,i in enumerate(data):

        text = ",\n ".join(i)
        post_obj = {"text": f"TEAM {e+1}\n {text}"}

        myobj = json.dumps(post_obj)
        x = requests.post(url, data=myobj)

        print(x.text)

if __name__ == "__main__":

    if not os.path.exists("team_list.json"):
        response = messagebox.askyesno(title= "File does not exist", message="team_list.json does not exist. Create this file now?")
        file_error(response)

    
    obj = App(root)
    root.geometry('600x600')
    root.mainloop()