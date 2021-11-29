import os
import time
from tkinter import *
from tkinter import ttk

months = {"Jan": 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" : 9, "Oct" : 10, "Nov" : 11, "Dec" : 12}

eng_dow = {"Mon" : "monday", "Tue" : "tuesday", "Wed" : "wednesday", "Thu" : "thursday", "Fri" : "friday", "Sat" : "saturday", "Sun" : "sunday"}

def month_to_number(month):
    if month in months:
        return str(months[month])
    else:
        return "0"

def dow_to_eng(dow):
    if dow in eng_dow:
        return eng_dow[dow]
    else:
        return "0"

def format_time(curr_time):
    s = ""
    curr = curr_time.split()
    year = curr[-1]
    month = curr[1]
    day = curr[2]
    dow = curr[0]
    s = year + '_' + month_to_number(month) + '_' + day + '_' + dow_to_eng(dow)
    return s

class App:
    def __init__(self, root):
        
        # root
        self.root = root
        
        # frames
        self.f0 = Frame(self.root)
        self.f1 = Frame(self.root)
        
        # variables
        self.text_var = StringVar(self.root)
        self.directory = '' #################### IMPORTANT #################### Type the path to the directory in which you want all your solutions to be in
        self.path = os.path.abspath(self.directory)
        
        # treeview
        self.tv = ttk.Treeview(self.f0, show = 'tree')
        self.ybar = Scrollbar(self.f0, orient = VERTICAL, command = self.tv.yview)
        self.tv.configure(yscroll = self.ybar.set)
        self.tv.heading('#0', text = 'Dir：' + self.directory, anchor = 'w')
        
        # adding files/directories to treeview
        self.node = self.tv.insert('', 'end', text = self.path, open = True)
        self.traverse_dir(self.node, self.path)
        
        # buttons
        self.button = Button(self.f1, command = self.get_sel_path, text = "Selection")
        self.button_create_sln = Button(self.f1, command = self.create_solution, text = "Solution")
        self.button_create_project = Button(self.f1, command = self.create_project, text = "Project")
        
        # entries
        self.entry_sln = Entry(self.f1, textvariable = self.text_var)
        self.entry_sln.insert(10, format_time(time.ctime()))
        self.entry_project = Entry(self.f1)
        
        # labels
        self.label_sln = Label(self.f1, text = "Input name of new solution:")
        self.label_project = Label(self.f1, text = "Input name of new project:")
        
        # packing
        self.ybar.pack(side = RIGHT, fill = Y)
        self.tv.pack()
        self.button.grid(row = 0, column = 1)
        self.button_create_sln.grid(row = 1, column = 1)
        self.button_create_project.grid(row = 3, column = 1)
        self.f0.pack(side = LEFT)
        self.f1.pack(side = RIGHT)
        self.label_sln.grid(row = 0, column = 0)
        self.entry_sln.grid(row = 1, column = 0)
        self.label_project.grid(row = 2, column = 0)
        self.entry_project.grid(row = 3, column = 0)

    def traverse_dir(self, parent, path):
        for d in os.listdir(path):
            full_path = os.path.join(path, d)
            isdir = os.path.isdir(full_path)
            id = self.tv.insert(parent, 'end', text = d, open = False)
            if isdir:
                self.traverse_dir(id, full_path)
        
    def update_variable(self, *args):
        for arg in args:
            if arg == "path":
                self.text_var.set(args[arg])
            else:
                self.text_var.set(self.tv.item(self.tv.selection(), "text"))
        
    def get_sel_path(self):
        item = self.tv.selection()[0]
        item_text = self.tv.item(item,"text")
        s = item_text
        item_parent = self.tv.parent(item)
        item_parent_text = self.tv.item(item_parent, "text")
        while(item_parent != ''):
            s = item_parent_text + '/' + s
            item_parent = self.tv.parent(item_parent)
            item_parent_text = self.tv.item(item_parent, "text")
        self.update_variable({"path" : s})
        self.entry_sln.delete(0, END)
        self.entry_sln.insert(0, item_text)
    
    def create_solution(self):
        path = self.directory
        sln_dir = self.entry_sln.get()
        dir_exists = os.path.exists(path + sln_dir)
        if dir_exists:
            isdir = os.path.isdir(path + sln_dir)
            if isdir:
                print("That directory already exists.")
            else:
                print("That is not a directory.")
        else:
            new_sln_command = "dotnet new sln -o " + sln_dir
            os.system(new_sln_command)
            node = self.tv.insert(self.node, 'end', text = sln_dir, open = False)
            self.traverse_dir(node, path + sln_dir)
    
    def create_project(self):
        path = self.directory
        sln_dir = self.entry_sln.get()
        project_name = self.entry_project.get()
        dir_exists = os.path.exists(path + sln_dir)
        if dir_exists:
            isdir = os.path.isdir(path + sln_dir)
            if isdir:
                project_exists = os.path.exists(path + sln_dir + "/" + project_name)
                if project_exists:
                    print("Project with that name already exists in that solution.")
                else:
                    new_project_command = "dotnet new console -lang c# -n " + project_name + " -o " + sln_dir + "/" + project_name + " -f net5.0"
                    os.system(new_project_command)
                    add_project2sln_command = "dotnet sln " + sln_dir + "/" + sln_dir + ".sln add " + sln_dir + "/" + project_name
                    os.system(add_project2sln_command)
                    node = [i for i in self.tv.get_children(self.node)][[self.tv.item(i, "text") for i in self.tv.get_children(self.node)].index(sln_dir)]
                    node = self.tv.insert(node, 'end', text = project_name, open = False)
                    self.traverse_dir(node, path + sln_dir + "/" + project_name)
            else:
                print("That is not a directory.")
        else:
            creating_sln = input("That solution is not yet created, do you wish to create it? (Y/N)")
            if creating_sln.upper() == "Y":
                self.create_solution()
            elif creating_sln.upper() == "N":
                print("Solution will not be created.")
            else:
                print("You have not entered a correct option.")

root = Tk()
App(root)
root.mainloop()
