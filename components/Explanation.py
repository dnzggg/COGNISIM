import tkinter
from tkinter import messagebox


class Explanation:
    def __init__(self, manager):
        self.agent = None
        self.time_stamp = None

        self.tk = manager.tk
        for widget in self.tk.winfo_children():
            widget.destroy()

        frame = tkinter.Frame(self.tk)
        frame.pack(fill=tkinter.BOTH, expand=True)

        self.canvas = tkinter.Canvas(frame, bg="#333")
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.history = tkinter.Canvas(frame, width=300, height=250, bg="#333", borderwidth=0, highlightthickness=0)
        self.history.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)
        scrollbar.config(command=self.history.yview)

        self.scrollable_frame = tkinter.Frame(self.history, bg="#333")
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.history.configure(scrollregion=self.history.bbox("all")))

        self.scrollable_frame.bind("<Enter>", self.entered)
        self.scrollable_frame.bind("<Leave>", self.left)

        self.history.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.history.configure(yscrollcommand=scrollbar.set)

        self.draw()

        self.main_dialog = None
        self.mouse_scroll = 1

    def __call__(self, time_stamp, agent):
        if self.agent != agent:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            self.agent = agent
            self.tk.title(self.agent.name)

        self.tk.deiconify()
        self.time_stamp = time_stamp
        self.label2.config(text="Time Point: " + str(self.time_stamp))

    def _on_mouse_wheel(self, event):
        self.history.yview_scroll(-1 * int((event.delta / 120)), "units")

    def entered(self, _):
        if self.mouse_scroll:
            self.scrollable_frame.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def left(self, _):
        if self.mouse_scroll:
            self.scrollable_frame.unbind_all("<MouseWheel>")

    def draw(self):
        frame = tkinter.Canvas(self.canvas, width=500, height=250, bg="#333", highlightthickness=0, bd=0)
        frame.pack(side=tkinter.TOP, padx=10, pady=10)

        # label = tkinter.Label(frame, text=self.agent.name, bg="#333", fg="white", font=("Montserrat", 14))
        # label.place(x=0, y=0)
        self.label2 = tkinter.Label(frame, text="Time Point: ", bg="#333", fg="white",
                                    font=("Montserrat", 14))
        self.label2.place(x=0, y=0)

        label3 = tkinter.Label(frame, text="Types of\nQuestion", bg="#333", fg="white", font=("Montserrat", 10))
        label3.place(x=0, y=40)

        scrollbar = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar.place(x=548, y=40, height=38)
        self.listbox = tkinter.Listbox(frame, width=48, height=6, yscrollcommand=scrollbar.set, exportselection=0,
                                       borderwidth=2, relief="groove", fg="white", bg="#707070")
        self.listbox.place(x=100, y=40)
        self.listbox.insert(tkinter.END, "Why Action ")
        self.listbox.insert(tkinter.END, "Why not Action ")
        self.listbox.insert(tkinter.END, "Why Belief ")
        self.listbox.insert(tkinter.END, "Why not Belief ")
        self.listbox.insert(tkinter.END, "Why Goal ")
        self.listbox.insert(tkinter.END, "Why not Goal ")
        scrollbar.config(command=self.listbox.yview)

        # label4 = tkinter.Label(frame, text="About", bg="#333", fg="white", font=("Montserrat", 10))
        # label4.place(x=0, y=100)

        # scrollbar2 = tkinter.Scrollbar(frame, orient="vertical")
        # scrollbar2.place(x=548, y=100, height=55)
        # self.listbox2 = tkinter.Listbox(frame, width=62, height=3, yscrollcommand=scrollbar2.set, exportselection=0,
        #                                 borderwidth=2, relief="groove", fg="white", bg="#707070")
        # self.listbox2.place(x=100, y=100)
        # self.listbox2.insert(tkinter.END, "Action ")
        # self.listbox2.insert(tkinter.END, "Belief ")
        # self.listbox2.insert(tkinter.END, "Goal ")
        # # self.listbox2.insert(tkinter.END, "Need ")
        # # self.listbox2.insert(tkinter.END, "Plan ")
        # scrollbar2.config(command=self.listbox2.yview)

        label5 = tkinter.Label(frame, text="What", bg="#333", fg="white", font=("Montserrat", 10))
        label5.place(x=0, y=180)

        self.text = tkinter.Text(frame, height=1, width=48, borderwidth=2, relief="groove", fg="white", bg="#707070")
        self.text.place(x=100, y=180)

        self.button = tkinter.Button(frame, text="Ask", command=self.ask, width=45, bg="#3897f4", fg="white",
                                     font=("Montserrat", 10))
        self.button.place(x=100, y=220)

    def ask(self):
        for i in self.listbox.curselection():
            if self.listbox.get(i):
                selection1 = self.listbox.get(i)
                break
        else:
            messagebox.showerror('Selection Error', 'Error: You haven\'t selected a "Type of Question"!')
            return

        # for i in self.listbox2.curselection():
        #     if self.listbox2.get(i):
        #         selection2 = self.listbox2.get(i)
        #         break
        # else:
        #     messagebox.showerror('Selection Error', 'Error: You haven\'t selected one of "About"!')
        #     return

        if text := self.text.get("1.0", "end-1c"):
            pass
        else:
            messagebox.showerror('Text Error', 'Error: You haven\'t entered a "What"!')
            return

        question = tkinter.Label(self.scrollable_frame,
                                 text="Question: " + selection1 + text + " at time point " + str(
                                     self.time_stamp) + "?",
                                 bg="#333", foreground="orange", font=("Montserrat", 10), width=42, wraplength=320,
                                 anchor="w", justify="left")
        question.pack(side=tkinter.TOP, anchor="w", fill="none")

        explanation = tkinter.Label(self.scrollable_frame, text="Explanation: " + "This is an explanation",
                                    bg="#333", foreground="orange", font=("Montserrat", 10), width=42, wraplength=320,
                                    anchor="w", justify="left")
        explanation.pack(side=tkinter.TOP, anchor="w", fill="none")
        empty = tkinter.Label(self.scrollable_frame, text="",
                              bg="#333", foreground="orange", font=("Montserrat", 10), width=42, wraplength=320,
                              anchor="w", justify="left")
        empty.pack(side=tkinter.TOP, anchor="w", fill="none")

        self.text.delete("1.0", tkinter.END)
        self.listbox.selection_clear(0, tkinter.END)
        # self.listbox2.selection_clear(0, tkinter.END)

    def make_scroll(self, parent, thing):
        v = tkinter.Scrollbar(parent, orient=tkinter.VERTICAL, command=thing.yview)
        v.grid(row=0, column=1, sticky=tkinter.NS)
        thing.config(yscrollcommand=v.set)

    def open(self):
        string_var = tkinter.StringVar()
        string_var.set(self.agent.name)
        label = tkinter.Label(self.tk, textvariable=string_var)
        label.pack()
