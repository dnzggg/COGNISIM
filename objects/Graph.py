import tkinter

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

matplotlib.use('TkAgg')


class Graph:
    """Tkinter toplevel that shows graphs

    Attributes
    ----------
    xs: list
        the data of the x axis
    ys: list
        the data of the y axis
    x_label: str
        the title for the x axis
    y_label: str
        the title for the y axis
    title: str
        the title for the graph
    graph: tkinter.Toplevel
        the tkinter object to have multiple screens
    running: bool
        to store if the graph is still open or not
    ax1: matplotlib' s subplot
        The subgraph that is going to be updated
    canvas: tkinter.FigureCanvasTkAgg
        The tkinter canvas where we put the graph and navigation bar

    Methods
    -------
    exit_window()
        Closes the window
    animate()
        Updates the graph being displayed
    update()
        Update the tkinter screen if the values are updated
    """
    def __init__(self, tk, xs, ys, x_label, y_label, title):
        """
        Parameters
        tk: tkinter.Tk()
            tk object of tkinter
        xs: list
            the data of the x axis
        ys: list
            the data of the y axis
        x_label: str
            the title for the x axis
        y_label: str
            the title for the y axis
        title: str
            the title for the graph
        """
        self.xs = xs
        self.ys = ys
        self.x_label = x_label
        self.y_label = y_label
        self.title = title

        self.graph = tkinter.Toplevel(tk)
        self.graph.protocol("WM_DELETE_WINDOW", self.exit_window)
        self.graph.title(title)
        self.graph.geometry("640x520")
        self.graph.resizable(False, False)

        self.running = True

        # plt.style.use('dark_background')
        self.ax1 = (fig := plt.figure()).add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(fig, master=self.graph)
        self.canvas.get_tk_widget().pack()

        NavigationToolbar2Tk(self.canvas, self.graph)

        self.store_xs = None
        self.store_ys = None

    def exit_window(self):
        """Closes the window"""
        self.running = False
        plt.close()
        self.graph.destroy()

    def animate(self):
        """Updates the graph being displayed"""
        self.ax1.clear()
        if isinstance(self.ys, dict):
            move = 0
            for key in self.ys:
                ys = [y + move * 0.1 for y in self.ys[key]]
                self.ax1.plot(self.xs, ys, label=key, marker="o")
                self.ax1.legend()
        else:
            self.ax1.plot(self.xs, self.ys, marker="o")
        self.ax1.set_xlabel(self.x_label)
        self.ax1.set_ylabel(self.y_label)

    def update(self):
        """Update the tkinter screen if the values are updated"""
        if self.store_xs != self.xs or self.store_ys != self.ys:
            self.animate()
            self.canvas.draw()
            self.store_xs = self.xs.copy()
            self.store_ys = self.ys.copy()
