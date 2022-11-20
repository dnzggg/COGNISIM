import pygame
from pygame import gfxdraw
import tkinter


class Blob:
    """Blob object to draw agents on the screen.

    Attributes
    ----------
    pos: list [int, int]
        position that it is to be drawn
    playing: bool
        stores if the agent is playing or not
    watching: bool
        stores if the agent is watching or not
    gossiping: bool
        stores if the agent is gossiping or not
    color: list(int, int, int)
        Color of the object to be displayed
    circle: pygame.Rect
        The object that stores the position and size of the blobs

    Methods
    -------
    render(screen)
        Renders the image according to rect on pygame screen.
    update(playing=False, watching=False, gossiping=False)
        Update the color of the agent
    handle_events(event, agent)
        When blob is clicked does something
    """
    def __init__(self, pos, width, radius, agent, player=False, conductor=False):
        """
        Parameters
        ----------
        pos: tuple[int, int]
            position that it is to be drawn
        playing: bool
            stores if the agent is playing or not
        watching: bool
            stores if the agent is watching or not
        gossiping: bool
            stores if the agent is gossiping or not
        """
        self.pos = pos
        self.o_pos = pos
        self.radius = radius
        self.o_radius = radius
        self.inner_radius = radius - 6
        self.o_inner_radius = self.inner_radius
        self.width = width
        self.o_width = self.width
        self.circle = pygame.Rect(pos[0]*self.width, pos[1]*self.width+87, radius, radius)
        self.o_circle = pygame.Rect(pos[0]*self.width, pos[1]*self.width+87, radius, radius)

        self.player = player
        self.agent = agent

        if conductor:
            self.color = (255, 0, 0, 100)
        elif player:
            self.color = (0, 255, 0, 100)

        self.show_name = False
        self.font = pygame.font.Font("Images/Montserrat-Regular.ttf", 15)

        self.shift_x = 0
        self.shift_y = 0
        self.tk = None
        self.main_dialog = None
        self.mouse_scroll = 1

    def render(self, screen):
        """Renders the blob on the pygame screen

        Parameters
        ----------
        screen: pygame.Surface
            pygame screen
        """
        r = int(self.radius / 2)

        x = self.pos[0] * self.width + self.shift_x + r
        y = self.pos[1] * self.width + self.shift_y + r + 87

        gfxdraw.filled_circle(screen, x, y, r, self.color)
        gfxdraw.aacircle(screen, x, y, r, self.color)
        gfxdraw.aacircle(screen, x, y, int(self.inner_radius / 2), (0, 0, 0))

        if self.show_name:
            text = self.font.render(self.agent.name + ":" + self.agent.strategy, True, (255, 255, 255))
            w = text.get_size()[0]
            pygame.draw.rect(screen, (112, 112, 112), (x + 7, y - 27, w + 6, 20), border_radius=3)
            screen.blit(text, (x + 10, y - 27))

    def update(self, gossiping=False, giver=False, receiver=False, shift=(0, 0), zoom=100, width=25):
        """Update the color of the agent

        Parameters
        ----------
        gossiping: bool
            stores if the agent is playing or not
        giver: bool
            stores if the agent is watching or not
        receiver: bool
            stores if the agent is gossiping or not
        """
        if self.player:
            self.color = (0, 255, 0, 100)
            if gossiping:
                self.color = (0, 255, 0)
            if giver:
                self.color = (255, 255, 0)
            if receiver:
                self.color = (255, 0, 255)
        else:
            self.color = (255, 0, 0, 100)
            if gossiping:
                self.color = (255, 0, 0)

        self.radius = int(self.o_radius * zoom / 100)
        self.inner_radius = int(self.o_inner_radius * zoom / 100)
        self.shift_x, self.shift_y = shift
        self.width = width
        self.circle = pygame.Rect(self.pos[0] * self.width + shift[0], self.pos[1] * self.width + 87 + shift[1], self.radius, self.radius)

    def handle_events(self, event, manager, round):
        """When blob is clicked does something

        Parameters
        ----------
        agent: Agent
            Agent object to identify
        event: pygame.event.Event
            pygame event
        """
        if event.type == pygame.MOUSEMOTION:
            if self.circle.collidepoint(event.pos[0], event.pos[1]):
                self.show_name = True
            else:
                self.show_name = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.circle.collidepoint(event.pos[0], event.pos[1]):
                self.tk = manager.tk
                self.tk.title(self.agent.name)
                for widget in self.tk.winfo_children():
                    widget.destroy()
                self.tk.deiconify()

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
                self.scrollable_frame.bind("<Configure>", lambda e: self.history.configure(scrollregion=self.history.bbox("all")))

                self.scrollable_frame.bind("<Enter>", self.entered)
                self.scrollable_frame.bind("<Leave>", self.left)

                self.history.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
                self.history.configure(yscrollcommand=scrollbar.set)

                self.draw()

    def _on_mouse_wheel(self, event):
        self.history.yview_scroll(-1 * int((event.delta / 120)), "units")

    def entered(self, event):
        if self.mouse_scroll:
            self.scrollable_frame.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def left(self, event):
        if self.mouse_scroll:
            self.scrollable_frame.unbind_all("<MouseWheel>")

    def draw(self):
        frame = tkinter.Canvas(self.canvas, width=500, height=250, bg="#333", highlightthickness=0, bd=0)
        frame.pack(side=tkinter.TOP, padx=10, pady=10)

        label = tkinter.Label(frame, text=self.agent.name, bg="#333", fg="white", font=("Montserrat", 14))
        label.place(x=0, y=0)
        label2 = tkinter.Label(frame, text="Time Point:", bg="#333", fg="white", font=("Montserrat", 14))
        label2.place(x=100, y=0)

        label3 = tkinter.Label(frame, text="Types of\nQuestion", bg="#333", fg="white", font=("Montserrat", 10))
        label3.place(x=0, y=40)

        scrollbar = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar.place(x=548, y=40, height=38)
        self.listbox = tkinter.Listbox(frame, width=62, height=2, yscrollcommand=scrollbar.set, exportselection=0,
                                       borderwidth=2, relief="groove", fg="white", bg="#707070")
        self.listbox.place(x=100, y=40)
        self.listbox.insert(tkinter.END, "Why")
        self.listbox.insert(tkinter.END, "Why not")
        self.listbox.bind("<Enter>", self.left)
        self.listbox.bind("<Leave>", self.entered)
        scrollbar.config(command=self.listbox.yview)

        label4 = tkinter.Label(frame, text="About", bg="#333", fg="white", font=("Montserrat", 10))
        label4.place(x=0, y=100)

        scrollbar2 = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar2.place(x=548, y=100, height=55)
        self.listbox2 = tkinter.Listbox(frame, width=62, height=3, yscrollcommand=scrollbar2.set, exportselection=0,
                                        borderwidth=2, relief="groove", fg="white", bg="#707070")
        self.listbox2.place(x=100, y=100)
        self.listbox2.insert(tkinter.END, "Action")
        self.listbox2.insert(tkinter.END, "Belief")
        self.listbox2.insert(tkinter.END, "Goal")
        self.listbox2.insert(tkinter.END, "Need")
        self.listbox2.insert(tkinter.END, "Plan")
        scrollbar2.config(command=self.listbox2.yview)

        label5 = tkinter.Label(frame, text="What", bg="#333", fg="white", font=("Montserrat", 10))
        label5.place(x=0, y=180)

        self.text = tkinter.Text(frame, height=1, width=45, borderwidth=2, relief="groove", fg="white", bg="#707070")
        self.text.place(x=100, y=180)

        self.button = tkinter.Button(frame, text="Ask", command=self.ask, width=45, bg="#3897f4", fg="white",
                                font=("Montserrat", 10))
        self.button.place(x=100, y=220)

    def ask(self):
        for i in self.listbox.curselection():
            print(self.listbox.get(i))
        # else:
        #     self.listbox["bg"] = "red"
        for i in self.listbox2.curselection():
            print(self.listbox2.get(i))
        # else:
        #     self.listbox2["bg"] = "red"
        print(self.text.get("1.0", tkinter.END))
        label = tkinter.Label(self.scrollable_frame, text="Explanation: " + self.text.get("1.0", tkinter.END),
                              bg="#333", foreground="orange", font=("Montserrat", 10), width=42, wraplength=320, anchor="w", justify="left")
        label.pack(side=tkinter.TOP, anchor="w", fill="none")
        self.text.delete("1.0", tkinter.END)
        # self.button["state"] = "disabled"
        # self.listbox["state"] = "disabled"
        # self.listbox2["state"] = "disabled"
        # self.text["state"] = "disabled"
        # self.listbox["bg"] = "black"
        # self.listbox2["bg"] = "black"
        # self.text["bg"] = "black"
        # self.listbox["selectbackground"] = "green"
        # self.listbox2["selectbackground"] = "green"

    def make_scroll(self, parent, thing):
        v = tkinter.Scrollbar(parent, orient=tkinter.VERTICAL, command=thing.yview)
        v.grid(row=0, column=1, sticky=tkinter.NS)
        thing.config(yscrollcommand=v.set)

    def get_pos(self):
        x = self.circle.x + self.circle.w / 2
        y = self.circle.y + self.circle.h / 2
        return x, y

    def open(self):
        string_var = tkinter.StringVar()
        string_var.set(self.agent.name)
        label = tkinter.Label(self.tk, textvariable=string_var)
        label.pack()
