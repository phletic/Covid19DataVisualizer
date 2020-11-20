from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from tkinter import messagebox


class graphException:
    def __init__(self, message):
        super().__init__()
        self.message = message
        messagebox.showerror(title="fatal error while graphing", message="graph manager says: " + str(self.message))
        return


class graph:
    def __init__(self, isgrid, useBaseTen, useLegend):
        self.isShowing = False
        CovidData = pd.read_csv("covid19Data/CovidData.csv", parse_dates=True)
        CovidData.date = pd.to_datetime(CovidData.date)
        self.fig, self.ax = plt.subplots()
        self.useLegend = useLegend
        self.data = CovidData
        if isgrid:
            self.ax.grid(True)
        if useBaseTen:
            plt.ticklabel_format(style='plain', axis='x')
            plt.ticklabel_format(style='plain', axis='y')

    def getStat(self, location, id):
        return self.data[self.data["location"] == location][id]

    def plotLine(self, x, y, colour, useMarker):
        xGraph = self.getStat(x[0], x[1])
        yGraph = self.getStat(y[0], y[1])
        ico = self.getStat(x[0], "iso_code").iloc[0]
        self.ax.plot(xGraph, yGraph, label=f'{ico}: {y[1].replace("_", " ")} over {x[1].replace("_", " ")}',
                     color=colour, marker="o" if useMarker == True else '')

    def plotBar(self, x, y, colour,useMarker):
        xGraph = self.getStat(x[0], x[1])
        yGraph = self.getStat(y[0], y[1])
        ico = self.getStat(x[0], "iso_code").iloc[0]
        self.ax.bar(xGraph, yGraph, label=f'{ico}: {y[1].replace("_", " ")} over {x[1].replace("_", " ")}',
                    color=colour)

    def show(self):
        if self.useLegend:
            self.ax.legend()
        try:
            self.fig.autofmt_xdate()
        except:
            pass
        plt.show()

if __name__ == '__main__':
    stats = graph(isgrid=False, useBaseTen=True, useLegend=True)
    stats.plotBar(("World", "date"), ("World", "total_cases"), (1, 0.25, 0), False)
    stats.show()
    # CovidData.date = pd.to_datetime(CovidData.date)
    # options
    # isgrid
    # location
    # use scientific notation
    # use legend
    """
    #plt.ion()
    for i in range(50):
        y = np.random.random([10,1])
        plt.plot(y)
        plt.draw()
        plt.pause(0.0001)
        plt.clf()
        
        
        
    
    fig, ax = plt.subplots()
    ax.plot(CovidData[CovidData["location"]=="Singapore"]["date"],CovidData[CovidData["location"]=="Singapore"]["total_cases"],label="Singapre cases per mill")
    ax.plot(CovidData[CovidData["location"]=="United States"]["date"],CovidData[CovidData["location"]=="United States"]["total_cases_per_million"],label="USA cases per mill")
    ax.bar(CovidData[CovidData["location"]=="Singapore"]["date"],CovidData[CovidData["location"]=="Singapore"]["stringency_index"]*100,label="Singapre stringency index")
    ax.plot(CovidData[CovidData["location"]=="United States"]["date"],CovidData[CovidData["location"]=="United States"]["total_cases"]*100,label="USA stringency index")
    # use a more precise date string for the x axis locations in the
    # toolbar
    fig.autofmt_xdate()
    ax.grid(True)
    ax.legend()
    plt.ticklabel_format(style='plain', axis='y')
    plt.show()
    
    """
