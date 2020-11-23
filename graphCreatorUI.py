import os
import tkinter
from graphData import graph, graphException
import pickle
from tkinter import ttk
from tkinter import filedialog

class graphCreator(tkinter.Frame):
    class elementFrame(tkinter.Frame):
        class graphElements(tkinter.Frame):
            def __init__(self, master, parent):
                self.parent = parent
                super().__init__(master, relief=tkinter.GROOVE, bd=1)
                self.Countries = []
                self.variables = []
                with open("covid19Data/Countries", "rb") as f:
                    self.Countries = list(pickle.load(f))
                with open("covid19Data/Variables", "rb") as f:
                    self.variables = list(pickle.load(f))
                self.loadWidgets()

            def loadWidgets(self):
                tkinter.Label(self, text="Country: ").grid(row=0, column=0)
                self.selctCountry = ttk.Combobox(self, values=self.Countries, width=35)
                self.selctCountry.grid(row=0, column=1, columnspan=6)

                tkinter.Label(self, text="X: ").grid(row=1, column=0)
                self.selectDataX = ttk.Combobox(self, values=self.variables, width=35)
                self.selectDataX.grid(row=1, column=1, columnspan=6)

                tkinter.Label(self, text="Y: ").grid(row=2, column=0)
                self.selectDataY = ttk.Combobox(self, values=self.variables, width=35)
                self.selectDataY.grid(row=2, column=1, columnspan=6)

                self.options = ["Line","Bar"]
                tkinter.Label(self, text="Bar type: ").grid(row=3, column=0)
                self.GraphType = ttk.Combobox(self, values=self.options, width=35)
                self.GraphType.grid(row=3, column=1, columnspan=6)

                tkinter.Label(self, text="red (0-1)").grid(row=4, column=0)
                self.RedEntry = tkinter.Entry(self, width=5)
                self.RedEntry.grid(row=4, column=1)

                tkinter.Label(self, text="green (0-1)").grid(row=4, column=2)
                self.GreenEntry = tkinter.Entry(self, width=5)
                self.GreenEntry.grid(row=4, column=3)

                tkinter.Label(self, text="blue (0-1)").grid(row=4, column=4)
                self.BlueEntry = tkinter.Entry(self, width=5)
                self.BlueEntry.grid(row=4, column=5)

                self.isUseMarker = tkinter.IntVar()
                self.UseMarker = tkinter.Checkbutton(self,text="use marker",variable=self.isUseMarker)
                self.UseMarker.grid(row=4, column=6)

                self.delete = tkinter.Button(self, text="delete", command=self.delete)
                self.delete.grid(row=0, column=100)

            def delete(self):
                self.grid_forget()
                self.parent.remove(self)
                del self

            def test(self):
                print("hello world")

        def __init__(self, master):
            self.elements = []
            super().__init__(master, relief=tkinter.GROOVE, bd=2)
            self.canvas = tkinter.Canvas(self)
            self.frame = tkinter.Frame(self.canvas)
            self.myscrollbar = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.myscrollbar.set)
            self.myscrollbar.pack(side="right", fill="y")
            self.canvas.pack(side="left")
            self.canvas.create_window((0, 0), window=self.frame, anchor='n')
            self.frame.bind("<Configure>", self.myfunction)
            self.frame.bind("<MouseWheel>", self._on_mousewheel)

        def _on_mousewheel(self, event):
            self.canvas.yview_scroll(-1 * (event.delta / 120), "units")

        def add(self):
            newElement = self.graphElements(self.frame, self.elements)
            self.elements.append(newElement)
            newElement.grid(row=len(self.elements), column=0)
            return newElement
            # tkinter.Label(self.frame, text=self.elementCount).grid(row=self.elementCount, column=0)

        def myfunction(self, event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=500, height=400)

    def __init__(self, master):
        super().__init__(master, relief=tkinter.GROOVE, bd=1)
        self.createWidget()

    def createWidget(self):
        self.introduction = tkinter.Label(self, text="graph manager").grid(row=0, column=0, columnspan=2)

        self.addElement = tkinter.Button(self, text="add", command=self.add)
        self.addElement.grid(row=0, column=3)

        self.isShowLegend = tkinter.IntVar()
        self.showLegend = tkinter.Checkbutton(self, text="show legend", variable=self.isShowLegend)
        self.showLegend.grid(row=1, column=0)

        self.isBaseTen = tkinter.IntVar()
        self.showBaseTen = tkinter.Checkbutton(self, text="base 10", variable=self.isBaseTen)
        self.showBaseTen.grid(row=1, column=1)

        self.isGrid = tkinter.IntVar()
        self.showGrid = tkinter.Checkbutton(self, text="show grid", variable=self.isGrid)
        self.showGrid.grid(row=1, column=2)

        self.elements = self.elementFrame(self)
        self.elements.grid(row=2, column=0, columnspan=6)

        self._showGraph = tkinter.Button(self, text="show graph", command=self.showGraph)
        self._showGraph.grid(row=1, column=3)

        self.saveGraph = tkinter.Button(self, text="save graph", command=self.save)
        self.saveGraph.grid(row=1, column=4)

        self.loadGraph = tkinter.Button(self, text="load graph", command=self.load)
        self.loadGraph.grid(row=1, column=5)


    def save(self):
        for i in self.elements.elements:
            self.checkProblem(i)
        SavingGraph(self.elements.elements)

    def load(self):
        filename = tkinter.filedialog.askopenfilenames(initialdir = "covid19Data/presets",title='select', filetypes=[
                    ("graph", ".graph"),
        ])[0]
        contents = []
        with open(filename,"rb") as f:
            contents = pickle.load(f)

        for i in reversed(self.elements.elements):
            i.grid_forget()
            self.elements.elements.remove(i)

        for i in contents:
            newElement = self.elements.add()
            newElement.selctCountry.current(i[0])
            newElement.selectDataX.current(i[1])
            newElement.selectDataY.current(i[2])
            newElement.GraphType.current(i[3])
            newElement.RedEntry.insert(0, i[4])
            newElement.GreenEntry.insert(0, i[5])
            newElement.BlueEntry.insert(0, i[6])
            newElement.isUseMarker.set(i[7])

    def add(self):
        self.elements.add()

    def showGraph(self):
        # result.plotLine(x=("World", "date"), y=("World", "total_cases"), colour="red", useMarker=False)
        # result.plotLine(x=("World", "date"), y=("World", "total_deaths"), colour="grey", useMarker=False)
        elements = []
        for i in self.elements.elements:
            try:
                result = self.checkProblem(i)
                if result == 0:
                    elements.append(
                    [(i.selctCountry.get(), i.selectDataX.get()), (i.selctCountry.get(), i.selectDataY.get())
                        , (float(i.RedEntry.get()), float(i.GreenEntry.get()), float(i.BlueEntry.get())),
                     True if i.isUseMarker.get() == 1 else False])
                else:
                    return
            except ValueError:
                graphException("some values is of null / miscellaneous error")
                return
        result = graph(isgrid=True if self.isGrid.get() == 1 else False,
                       useBaseTen=True if self.isBaseTen.get() == 1 else False,
                       useLegend=True if self.isShowLegend.get() == 1 else False)
        for i,e in enumerate(elements):
            if self.elements.elements[i].GraphType.get() == 'Line':
                result.plotLine(*e)
            elif self.elements.elements[i].GraphType.get() == 'Bar':
                result.plotBar(*e)
        result.show()

    def checkProblem(self,i):
        currentXAxis = ""
        isDateTime_y = False
        # sorry Im going full on if statements. Thats why my coding will never be pro level....
        if not i.GraphType.get() or not i.selectDataY.get() or not i.selectDataX.get():
            raise ValueError
        if i.GraphType.get() not in i.options:
            graphException("graph type not found in data set")
            return 1
        if i.selectDataY.get() not in i.variables or i.selectDataX.get() not in i.variables:
            graphException("axis value not in data set")
            return 1
        if not currentXAxis:
            currentXAxis = i.selectDataX.get()
        if i.selectDataX.get() != currentXAxis:
            graphException("x axis inconsistent!")
            return 1
        if i.selectDataY.get() == 'date':
            graphException("y axis cannot be a date")
            return 1
        if i.selctCountry.get() not in i.Countries:
            graphException("country not found in data set. Check your spacing and spelling")
            return 1
        if float(i.RedEntry.get()) > 1 or float(i.GreenEntry.get()) > 1 or  float(i.BlueEntry.get()) > 1:
            graphException("RGB can only be a value between 0 and 1!")
            return 1
        else: return 0

class SavingGraph():
    def __init__(self,file):
        self.newWindow = tkinter.Tk()
        self.newWindow.title("Save Covid19 graph")

        tkinter.Label(self.newWindow,text="Save current graph").grid(row=0,column=0,columnspan=5)

        tkinter.Label(self.newWindow,text="file name").grid(row=1,column=0)
        self.name = tkinter.Entry(self.newWindow)
        self.name.grid(row=1,column=1,columnspan=3,rowspan=5)

        self.saveButton = tkinter.Button(self.newWindow,text="save",command = lambda :self.save(self.name.get(),file)).grid(row=6,column=5)
        
        self.newWindow.geometry(f'300x250')
        self.newWindow.mainloop()

    def save(self,name,content):
        if not name:
            graphException("provide a name!")
            return
        file = []
        for i in content:
            element = [i.selctCountry.current(),i.selectDataX.current(),i.selectDataY.current(),i.GraphType.current(),i.RedEntry.get(),i.GreenEntry.get(),i.BlueEntry.get(),i.isUseMarker.get()]
            file.append (element)
        print(file)
        with open(f"covid19Data/presets/{name}.graph","wb") as f:
            pickle.dump(file,f)
