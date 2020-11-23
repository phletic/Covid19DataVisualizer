import os
import tkinter
from syncCovidData import writeSyncing
from syncerUI import syncer
from graphCreatorUI import graphCreator
from multiprocessing import freeze_support

#asdasdasd
# driver code
class Title(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.testText = tkinter.Label(self.master, text="Covid 19 Interactive Data (realtime)", font=("Arial", 25))
        self.testText.grid(row=0, column=0, columnspan=20)


if __name__ == '__main__':
    freeze_support()
    if not os.path.exists('covid19Data'):
        os.mkdir("covid19Data")
    if not os.path.exists('covid19Data/presets'):
        os.mkdir('covid19Data/presets')
    writeSyncing(False)  # you are not syncing the data set rn
    root = tkinter.Tk()
    root.resizable(0, 0)
    syncClass = Title(root)
    syncClass.grid()
    root.title("Covid-19 visualizer")
    syncClass = syncer(root)
    syncClass.grid()
    test = graphCreator(root)
    test.grid(row=1, column=1)
    root.mainloop()
    root.mainloop()
