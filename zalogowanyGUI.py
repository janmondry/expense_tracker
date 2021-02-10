import tkinter as tk
from tkinter import ttk
from pandas import DataFrame
from TreeView import TreeView as TV
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import showinfo
import numpy as np

from GUI import GUI
from category import Category


class ZalogowanyGUI(GUI):
    def __init__(self, controller):
        super().__init__(controller)
        self.navbar = None
        self.mainframe = None
        self.navBtnAdd = None
        self.navBtnHistory = None
        self.navBtnWykresy = None

        # dodawanie
        self.labelName = None
        self.nameEntry = None
        self.labelCat = None
        self.catCombo = None
        self.labelValue = None
        self.valueEntry = None
        self.labelDate = None
        self.dateEntry = None

        # historia
        self.zaznaczony_wpis = None

        # wykresy
        self.barchart = None

    def printGUI(self):
        super().printGUI()
        self.navbar = tk.Frame(self.window)
        self.mainframe = tk.Frame(self.window)
        self.navbar.pack(side=tk.TOP, pady=10)
        self.mainframe.pack(fill=tk.BOTH)
        font = ('TkDefaultFont', 15)

        self.navBtnAdd = tk.Button(self.navbar, text="Dodaj wydatek", font=font, command=self.dodajwydatekFrame).grid(row=0, column=0, ipadx=10, padx=10)
        self.navBtnHistory = tk.Button(self.navbar, text="Historia", font=font, command=self.historiaFrame).grid(row=0, column=1, ipadx=20, padx=10)
        self.navBtnWykresy = tk.Button(self.navbar, text="Wykresy", font=font, command=self.wykresyFrame).grid(row=0, column=2, ipadx=20, padx=10)
        self.window.mainloop()

    def refreshMainframe(self):
        self.mainframe.destroy()
        self.mainframe = tk.Frame(self.window)
        self.mainframe.pack(fill=tk.BOTH, pady=10)

    def printAddingFrame(self):
        self.refreshMainframe()

        padx = 330
        font = ('TkDefaultFont', 15)
        # label.config(font=("Courier", 44))

        self.labelCat = tk.Label(self.mainframe, text="Kategoria", font=font).grid(row=0, column=0, padx=(padx, 20), pady=(0, 10))
        self.catCombo = ttk.Combobox(self.mainframe, values=[Category.cat1, Category.cat2, Category.cat3], state='readonly', font=font)
        self.catCombo.grid(row=0, column=1, columnspan=2, sticky=tk.W + tk.E, pady=(0, 10))
        self.catCombo.current(0)

        self.labelName = tk.Label(self.mainframe, text="Nazwa", font=font).grid(row=1, column=0, padx=(padx, 20), pady=(0, 10))
        self.nameEntry = tk.Entry(self.mainframe, font=font)
        self.nameEntry.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E, pady=(0, 10))

        self.labelValue = tk.Label(self.mainframe, text="Cena", font=font).grid(row=2, column=0, padx=(padx, 20), pady=(0, 10))
        self.valueEntry = tk.Entry(self.mainframe, font=font)
        self.valueEntry.grid(row=2, column=1, columnspan=2, sticky=tk.W + tk.E, pady=(0, 10))

        self.labelDate = tk.Label(self.mainframe, text="Data", font=font).grid(row=3, column=0, padx=(padx, 20), pady=(0, 10))
        self.dateEntry = tk.Entry(self.mainframe, font=font)
        self.dateEntry.grid(row=3, column=1, columnspan=2, sticky=tk.W + tk.E, pady=(0, 10))

        self.addBtn = tk.Button(self.mainframe, text="Dodaj", font=font, command=self.dodajwydatek).grid(row=4, column=1, pady=20)

    def historiaFrame(self):
        self.printHistoryFrame()

    def dodajwydatekFrame(self):
        self.printAddingFrame()

    def dodajwydatek(self):
        name = self.nameEntry.get()
        category = self.catCombo.get()
        try:
            value = self.valueEntry.get()
            check_value = float(value)  # tu może wywalać errora
            value_rounded = str(round(check_value))
            date = self.dateEntry.get()
            datetime.strptime(date, "%Y-%m-%d")     # tu może wywalać errora
            self.controller.tryAddExpense(name, category, value_rounded, date)
        except ValueError as err:
            showinfo("Niepoprawne dane!", "Wprowadź datę w formacie RRRR-MM-DD!\n""Wprowadź wartość w formacie #.##")

    def wykresyFrame(self):
        self.printChartsFrame()

    def infoboxAddingOK(self):
        showinfo("Dodano wydatek", "Pomyślnie dodano nowy wydatek!")

    def printHistoryFrame(self):
        self.refreshMainframe()
        monthyearsdict = self.controller.getmonthyeardict()

        def configTreeview1():
            treeview.treeview.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))
            treeview.sb_treeview.pack(side=tk.LEFT, fill=tk.Y)
            treeview.treeview.heading('#0', text='Wybierz miesiąc lub dzień')
            treeview.treeview.insert('', 'end', '<wszystko>', text='<wszystko>')

            # dodawanie elementów do treeview z dniami
            for monthyear in monthyearsdict.keys():
                treeview.add_values(monthyearsdict[monthyear].keys(), monthyear)

        def configTreeview2():
            treeviewResults.treeview['columns'] = ("#1", "#2", "#3", "#4")
            treeviewResults.treeview.heading('#0', text='Data')
            treeviewResults.treeview.heading('#1', text='Kategoria')
            treeviewResults.treeview.heading('#2', text='Nazwa')
            treeviewResults.treeview.heading('#3', text='Wydatek')
            treeviewResults.treeview.heading('#4', text='ID')
            treeviewResults.treeview.column('#0', width=70, anchor='center')
            treeviewResults.treeview.column('#1', width=70, anchor='center')
            treeviewResults.treeview.column('#2', width=100, anchor='center')
            treeviewResults.treeview.column('#3', width=70, anchor='center')
            treeviewResults.treeview.column('#4', width=10, anchor='center')

        def usuwanko():
            item = treeviewResults.treeview.focus()
            if item != '':
                msgbox = tk.messagebox.askyesno('Usuwanie wydatku', 'Czy na pewno chcesz usunąć zaznaczony wydatek?')
                if msgbox:
                    self.controller.deleteExpense(self.zaznaczony_wpis)
                    self.printHistoryFrame()

        def zaznacz_wpis(event):
            curItem = treeviewResults.treeview.focus()
            self.zaznaczony_wpis = treeviewResults.treeview.item(curItem)

        def on_tv_select(event):  # metoda podpięta pod zdarzenie wywoływane po kliknięciu jakiegoś elementu na liście
            treeviewResults.treeview.delete(*treeviewResults.treeview.get_children())
            curItem = treeview.treeview.focus()  # element, który otrzymał fokus
            if str(curItem) == '<wszystko>':
                for m_y in monthyearsdict.keys():
                    for d in monthyearsdict[m_y]:
                        expList = monthyearsdict[m_y][d]
                        for exp in expList:
                            treeviewResults.treeview.insert('', 'end', text=d, values=(
                            exp.getCategory, exp.getName, exp.getAmount, exp.getID))  # wyświetl jego składowe w treeviewResults

            elif curItem in monthyearsdict.keys():        # jeśli wybrany element to cały miesiąc
                for date in monthyearsdict[curItem]:     # to dla każdego dnia w miesiącu
                    expList = monthyearsdict[curItem][date]
                    for exp in expList:
                        treeviewResults.treeview.insert('', 'end', text=date, values=(exp.getCategory, exp.getName, exp.getAmount, exp.getID))   # wyświetl jego składowe w treeviewResults
            else:
                for monthyear in monthyearsdict.keys():
                    tmp1 = monthyearsdict[monthyear]
                    tmp2 = tmp1.keys()
                    actualDate = datetime.strptime(curItem, "%Y-%m-%d").date()
                    if actualDate in tmp2:     # jeśli wybrany element to któryś z dni
                        expList = monthyearsdict[monthyear][actualDate]
                        for exp in expList:
                            treeviewResults.treeview.insert('', 'end', text=str(actualDate), values=(
                            exp.getCategory, exp.getName, exp.getAmount, exp.getID))  # wyświetl jego składowe w treeviewResults

        treeview = TV(self.mainframe)
        configTreeview1()

        treeviewResults = TV(self.mainframe)
        configTreeview2()

        font = ('TkDefaultFont', 15)
        deleteFrame = tk.Frame(self.mainframe)
        deleteFrame.pack(side=tk.BOTTOM, expand=True, fill=tk.X, padx=(0, 27))
        deleteBtn = tk.Button(deleteFrame, text='Usuń zaznaczone', command=usuwanko, font=font)
        deleteBtn.pack(side=tk.RIGHT)

        treeviewResults.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        treeviewResults.sb_treeview.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        treeview.treeview.bind("<<TreeviewSelect>>",
                           on_tv_select)  # podpinam zdarzenie, wywoływane, gdy kliknięto jakiś element drzewa
        treeviewResults.treeview.bind("<<TreeviewSelect>>", zaznacz_wpis)

    def printMainPlot(self, twoja_srednia_miesieczna, srednia_miesieczna_innych, ileRekordow=-1):
        if self.barchart is not None:
            self.barchart.get_tk_widget().destroy()
        monthYearToSumDict = self.controller.getMonthYearToSumDict()
        monthYearToSumDict = dict(sorted(monthYearToSumDict.items()))
        msc_list = list(monthYearToSumDict.keys())
        wydatki_list = list(monthYearToSumDict.values())
        if ileRekordow == -1:
            ileRekordow = 12
        msc_list = msc_list[-ileRekordow:]
        wydatki_list = wydatki_list[-ileRekordow:]

        data1 = {'Miesiące': msc_list,
                 'Wydatki': wydatki_list
                 }
        data2 = {'Twoja średnia': twoja_srednia_miesieczna}
        data3 = {'Średnia innych': srednia_miesieczna_innych}
        df1 = DataFrame(data1, columns=['Miesiące', 'Wydatki'])
        df2 = DataFrame(data2, index=msc_list)
        df3 = DataFrame(data3, index=msc_list)
        # print(df1)

        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.mainframe)
        self.barchart = bar1
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))
        df1 = df1[['Miesiące', 'Wydatki']].groupby('Miesiące').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        df2.plot(kind='line', legend=True, ax=ax1, color={'Twoja średnia': 'green'})
        df3.plot(kind='line', legend=True, ax=ax1, color={'Średnia innych': 'red'})
        box = ax1.get_position()
        ax1.set_position([box.x0, box.y0 + box.height * 0.1, box.width * 0.75, box.height * 0.9])
        ax1.legend(title='Legenda', loc='center left', bbox_to_anchor=(1, 0.5))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

        ax1.set_title('Wydatki w miesiącach')
        ax1.set_ylabel('Wydatki [zł]')

        for p in ax1.patches:
            number = int(p.get_height())
            ax1.annotate(number,
                        (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
                        va='center', xytext=(0, 4), textcoords='offset points')

    def printPieChart(self):
        catToAmountDict = self.controller.getCategoryToAmountDict()
        figure1 = plt.Figure(figsize=(4, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.mainframe)
        bar1.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 10))
        data1 = {'Wydatki': catToAmountDict.values()}
        df1 = DataFrame(data1, index=catToAmountDict.keys())
        df1.plot.pie(y='Wydatki', figsize=(4, 5), ax=ax1, autopct='%1.1f%%', legend=False)
        ax1.set_title('Kategorie wydatków w tym miesiącu')
        ax1.set_ylabel('')

    def printAvgTexts(self, labeltexts):
        textFrame = tk.Frame(self.mainframe)
        for text in labeltexts:
            label = tk.Label(textFrame, text=text, font=('Calibri', 15))
            label.pack(side=tk.TOP)
        textFrame.pack(side=tk.TOP, fill=tk.X, expand=True, pady=10)

    def printChartsFrame(self):
        if self.controller.userHasNoHistory():
            self.refreshMainframe()
            text1 = 'Nie masz żadnych wydatków, na podstawie których można utworzyć wykresy!'
            self.printAvgTexts([text1])
        else:
            nrDniaDzisiaj = datetime.today().day
            wydatki_ten_miesiac = round(self.controller.getExpensesToToday(), 2)
            srednio_do_dnia = round(self.controller.getAvgToDay(nrDniaDzisiaj), 2)
            srednia_miesieczna_innych = round(self.controller.getAvgOfOthers(), 2)
            twoja_srednia_miesieczna = round(self.controller.getAvgOverall(), 2)
            # print((wydatki_ten_miesiac, srednio_do_dnia, srednia_miesieczna_innych))

            self.refreshMainframe()
            text1 = 'Twoje wydatki w tym miesiącu: ' + str(wydatki_ten_miesiac)
            text2 = 'Średnio do ' + str(nrDniaDzisiaj) + '. dnia miesiąca wydajesz: ' + str(srednio_do_dnia)
            text3 = 'Twoje średnie miesięczne wydatki: ' + str(twoja_srednia_miesieczna)
            text4 = 'Średnia miesięcznych wydatków pozostałych użytkowników: ' + str(srednia_miesieczna_innych)
            self.printAvgTexts([text1, text2, text3, text4])

            def command1():
                self.printMainPlot(twoja_srednia_miesieczna, srednia_miesieczna_innych, 3)
            def command2():
                self.printMainPlot(twoja_srednia_miesieczna, srednia_miesieczna_innych, 6)
            def command3():
                self.printMainPlot(twoja_srednia_miesieczna, srednia_miesieczna_innych, 12)

            btnsFrame = tk.Frame(self.mainframe)
            btnsText = 'Ile miesięcy chcesz zobaczyć?'
            btnsLabel = tk.Label(btnsFrame, text=btnsText)
            btn3 = tk.Button(btnsFrame, text='3', command=command1)
            btn6 = tk.Button(btnsFrame, text='6', command=command2)
            btn12 = tk.Button(btnsFrame, text='12', command=command3)
            btnsLabel.pack(side=tk.LEFT, padx=10)
            btn3.pack(side=tk.LEFT, padx=5)
            btn6.pack(side=tk.LEFT, padx=5)
            btn12.pack(side=tk.LEFT, padx=5)
            btnsFrame.pack(side=tk.TOP, fill=tk.X, expand=True, pady=10)

            self.printMainPlot(twoja_srednia_miesieczna, srednia_miesieczna_innych)
            self.printPieChart()







