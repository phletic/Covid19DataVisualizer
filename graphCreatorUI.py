import tkinter
from graphData import graph,graphException
import pickle
from tkinter import ttk


class graphCreator(tkinter.Frame):
    class elementFrame(tkinter.Frame):
        class graphElements(tkinter.Frame):
            def __init__(self, master,parent):
                self.parent = parent
                super().__init__(master,relief=tkinter.GROOVE,bd=1)
                self.Countries = []
                self.variables = []
                with open("covid19Data/Countries", "rb") as f:
                    self.Countries = list(pickle.load(f))
                with open("covid19Data/Variables", "rb") as f:
                    self.variables = list(pickle.load(f))
                self.loadWidgets()

            def loadWidgets(self):
                tkinter.Label(self,text="Country: ").grid(row=0,column=0)
                self.selctCountry = ttk.Combobox(self, values=self.Countries,width=35)
                self.selctCountry.grid(row=0, column=1,columnspan=6)

                tkinter.Label(self,text="X: ").grid(row=1,column=0)
                self.selectDataX = ttk.Combobox(self, values=self.variables,width=35)
                self.selectDataX.grid(row=1, column=1,columnspan=6)

                tkinter.Label(self,text="Y: ").grid(row=2,column=0)
                self.selectDataY = ttk.Combobox(self, values=self.variables,width=35)
                self.selectDataY.grid(row=2, column=1,columnspan=6)


                tkinter.Label(self,text="red (0-1)").grid(row=3,column=0)
                self.RedEntry = tkinter.Entry(self,width=5)
                self.RedEntry.grid(row=3, column=1)

                tkinter.Label(self,text="green (0-1)").grid(row=3,column=2)
                self.GreenEntry = tkinter.Entry(self,width=5)
                self.GreenEntry.grid(row=3, column=3)

                tkinter.Label(self,text="blue (0-1)").grid(row=3,column=4)
                self.BlueEntry = tkinter.Entry(self,width=5)
                self.BlueEntry.grid(row=3, column=5)

                self.delete = tkinter.Button(self,text="delete",command = self.delete)
                self.delete.grid(row=0,column=100)

            def delete(self):
                self.grid_forget()
                self.parent.remove(self)

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
            newElement = self.graphElements(self.frame,self.elements)
            self.elements.append(newElement)
            newElement.grid(row=len(self.elements), column=0)
            #tkinter.Label(self.frame, text=self.elementCount).grid(row=self.elementCount, column=0)

        def myfunction(self, event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=400, height=400)

    def __init__(self, master):
        super().__init__(master, relief=tkinter.GROOVE, bd=1)
        self.createWidget()

    def createWidget(self):
        self.introduction = tkinter.Label(self, text="graph manager").grid(row=0, column=0,columnspan=2)

        self.addElement = tkinter.Button(self,text="add",command = self.add)
        self.addElement.grid(row=0,column=3)

        self.isShowLegend = tkinter.IntVar()
        self.showLegend = tkinter.Checkbutton(self,text="show legend",variable=self.isShowLegend)
        self.showLegend.grid(row=1,column=0)

        self.isBaseTen = tkinter.IntVar()
        self.showBaseTen = tkinter.Checkbutton(self,text="base 10",variable=self.isBaseTen)
        self.showBaseTen.grid(row=1,column=1)

        self.isGrid = tkinter.IntVar()
        self.showGrid = tkinter.Checkbutton(self,text="show grid",variable=self.isGrid)
        self.showGrid.grid(row=1,column=2)

        self.elements = self.elementFrame(self)
        self.elements.grid(row=2, column=0,columnspan=4)

        self._showGraph = tkinter.Button(self,text="show graph",command=self.showGraph)
        self._showGraph.grid(row=1,column=3)

    def add(self):
        self.elements.add()

    def showGraph(self):
        result = graph(isgrid=True if self.isGrid.get() == 1 else False,
                       useBaseTen=True if self.isBaseTen.get() == 1 else False,
                       useLegend=True if self.isShowLegend.get() == 1 else False)
        #result.plotLine(x=("World", "date"), y=("World", "total_cases"), colour="red", useMarker=False)
        #result.plotLine(x=("World", "date"), y=("World", "total_deaths"), colour="grey", useMarker=False)
        print(self.elements.elements)
        for i in self.elements.elements:
            print(i)
            print(i.selctCountry.get(),i.selectDataX.get(),i.selectDataY.get(),i.RedEntry.get(),i.BlueEntry.get(),i.GreenEntry.get())
            try:
                result.plotLine(x=(i.selctCountry.get(), i.selectDataX.get()), y=(i.selctCountry.get(), i.selectDataY.get())
                                ,colour=(int(i.RedEntry.get()), int(i.GreenEntry.get()), int(i.BlueEntry.get())),
                                useMarker=False)
            except ValueError:
                graphException("some values is of null")
                return
        result.show()
