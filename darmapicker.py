from tkinter import *

class Calculator(Frame):
    """
    An example of a calculator app developed using the 
    Tkinter GUI.
    """

    def __init__(self, master):
        """
        Initializes the frame.
        :param master: root.Tk()
        """
        Frame.__init__(self, master)
        self.create_widgets()
        self.grid()
        
        self.watched_drama = []
        self.watching = []
        self.dropped = []
        self.on_hold = []
        
        
    def show_list(self, list_data, title):
        top =Toplevel(self)
        top.title(title)
        top.geometry("300x300")
        
        text_box = Text(top, width=40, height=15)
        text_box.pack()
        
        if len(list_data) == 0:
            text_box.insert(END, "No Items yet")
        else:
            for i in list_data:
                text_box.insert(END, f"-{i}\n")  
                
    def get_input(self, list_data, title):  
        top = Toplevel(self)
        top.title(title)
        top.geometry("300x200")
        
        label = Label(top, text = "Enter drama name: ")
        label.pack()
        
        entry = Entry(top, width = 30)
        entry.pack()
        
        def save_value():
            value = entry.get()
            if value.strip():
                list_data.append(value)
            top.destroy()
        Button(top, text = "Save", command = save_value).pack()
        
    
    
    def create_widgets(self):
        """
        Creates the widgets to be used in the grid.
        :return: None
        """
        


        self.dropped_input_bttn = Button(self, text="Add Dropped", width=12, height=3, command=lambda: self.get_input(self.dropped, "Added to Dropped List"))
        self.dropped_input_bttn.grid(row=2, column=3)

        self.dropped_bttn = Button(self, text="Dropped", width=12, height=3, command=lambda: self.show_list(self.dropped, "Dropped Dramas: "))
        self.dropped_bttn.grid(row=1, column=3)

        self.watched_drama_bttn = Button(self, text="Watched Drama", width=12, height=3, command=lambda: self.show_list(self.watched_drama, "Watched Dramas: "))
        self.watched_drama_bttn.grid(row=1, column=0)

        self.watching_bttn = Button(self, text="Watching", width=12, height=3, command=lambda: self.show_list(self.watching, "Currently Watching: "))
        self.watching_bttn.grid(row=1, column=1)

        self.on_hold_bttn = Button(self, text="On Hold", width=12, height=3, command=lambda: self.show_list(self.on_hold, "Dramas On Hold: "))
        self.on_hold_bttn.grid(row=1, column=2)

        self.watched_drama_input_bttn = Button(self, text="Add Watched Drama", width=12, height=3, command=lambda: self.get_input(self.watched_drama, "Added to Watched Drama List"))
        self.watched_drama_input_bttn.grid(row=2, column=0)

        self.watched_drama_bttn = Button(self, text="Add Watching", width=12, height=3, command=lambda: self.get_input(self.watching, "Added to Watching List"))
        self.watched_drama_bttn.grid(row=2, column=1)

        self.on_hold_input_bttn = Button(self, text="Add On Hold", width=12, height=3, command=lambda: self.get_input(self.on_hold, "Added to On Hold List"))
        self.on_hold_input_bttn.grid(row=2, column=2)

        self.drama_roulette_bttn = Button(self, text="Drama Roulette", width=12, height=3, command=lambda: self.show_list(self.watched_drama, "CHANGE TO RANDOM DRAMA"))
        self.drama_roulette_bttn.grid(row=3, column=3)



root = Tk()
root.geometry()
root.title("Drama Picker")
app = Calculator(root)
root.mainloop()