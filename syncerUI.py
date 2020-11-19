import pickle
import time
import tkinter
import multiprocessing
from datetime import datetime
from syncCovidData import sync, isSyncingNow
class syncer(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master,relief=tkinter.GROOVE,bd=1)
        self.grid()
        self.loadWidgets()
        self.setDateTime()

    def loadWidgets(self):
        self.Title = tkinter.Label(self, text="sync data")
        self.Title.grid(row=0 , column=0 )

        self.syncButton = tkinter.Button(self, text="click here to sync", command=self.sync)
        self.syncButton.grid(row=0, column=1)

        self.last_sync = tkinter.Label(self)
        self.last_sync.grid(row=1, column=0, columnspan=2)

    def sync(self):
        self.writeDateTime()
        self.setDateTime()
        print(processes)
        for i in processes:
            if i.is_alive():
                i.terminate()
        processes.clear()
        processes.append(multiprocessing.Process(target=sync))
        processes.append(multiprocessing.Process(target=checkSync))
        for i in processes:
            i.start()

    def writeDateTime(self):
        with open("covid19Data/last_sync", 'wb') as f:
            pickle.dump(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), f)

    def setDateTime(self):
        try:
            with open("covid19Data/last_sync", 'rb') as f:
                currentDateTime = pickle.load(f)
                self.last_sync['text'] = "last synced - {0}".format(currentDateTime)
        except FileNotFoundError:
            self.last_sync['text'] = "never synced before"

    def loading(self):
        self.last_sync['text'] = "syncing now"
class loadingScreen():
    def __init__(self, func):
        self.func = func
        self.newWindow = tkinter.Tk()
        windowWidth = self.newWindow.winfo_reqwidth()
        windowHeight = self.newWindow.winfo_reqheight()
        positionRight = int(self.newWindow.winfo_screenwidth() / 2 - windowWidth / 2 - 150)
        positionDown = int(self.newWindow.winfo_screenheight() / 2 - windowHeight / 2 - 125)
        self.newWindow.geometry(f'300x250+{positionRight}+{positionDown}')
        self.newWindow.resizable(False, False)
        self.newWindow.overrideredirect(True)
        self.newWindow.overrideredirect(1)
        self.frameCnt = 12
        self.frames = [tkinter.PhotoImage(file='200.gif', format='gif -index %i' % (i)) for i in range(self.frameCnt)]
        self.label = tkinter.Label(self.newWindow)
        self.label.pack()
        self.Explanation = tkinter.Label(self.newWindow, text="Process is running, please wait for a while")
        self.Explanation.pack()
        self.newWindow.after(0, self.update, 0)
        self.newWindow.after(1000, self.checkToDestroy)
        self.newWindow.mainloop()

    def update(self, ind):  # update the loading frame
        frame = self.frames[ind]
        ind += 1
        if ind == self.frameCnt:
            ind = 0
        self.label.configure(image=frame)
        self.newWindow.after(100, self.update, ind)

    def checkToDestroy(self):
        if self.func():
            print("still loading")
        else:
            self.newWindow.destroy()
        self.newWindow.after(1000, self.checkToDestroy)


def checkSync():
    time.sleep(0.5)
    loadingScreen(isSyncingNow)
    print("done")
    return

processes = [multiprocessing.Process(target=sync), multiprocessing.Process(target=checkSync)]