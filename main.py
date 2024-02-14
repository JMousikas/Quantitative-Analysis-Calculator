import numpy as np
from tkinter import *


# molmasse
def molmasse(Produkt, molare_masse=0):
    molare_massen = {'C': 12.011, 'O': 15.999, 'H': 1.0078, 'N': 14.007}
    for Element in Produkt:
        molare_masse += molare_massen.get(Element)
    return molare_masse


# Teilchenanzahl ausrechnen
def teilchenzahl(masse, molare_masse):
    return masse / molare_masse  # round(masse / molare_masse, 1)


# mol der einzelnen Elemente ausrechnen
def molElemente(molProdukte, Produkte, molO):
    Elemente = {'C': 0, 'O': 0, 'H': 0, 'N': 0}
    for i in range(0, len(Produkte)):
        for j in Produkte[i]:
            Elemente[j] += molProdukte[i]
    Elemente['O'] -= molO
    return Elemente


def Rechner():
    Interface = Tk()
    Interface.title('Quantitative Elementeranalyse Rechner')
    mProdukte = []


    def reset():
        Interface.destroy()
        Rechner()


    def getInputProd(event=None):
        global Produkte
        Produkte = [list(char.upper()) for string in
                    np.array(ProduktEingabe.get().split()).reshape(-1, 1).tolist() for char in
                    string]
        ProduktEingabe.config(state="disabled")
        ProduktConfirm.config(state="disabled")
        createInputmProd(1)

    def createInputmProd(i):
        nonlocal mProdukte

        def getInputmProd(event=None):
            nonlocal mProdukte
            mProdukte.append(float(mProduktEingabe.get()))
            mProduktEingabe.config(state="disabled")
            mProduktConfirm.config(state="disabled")

        mProduktLabel = Label(Interface, text=("Masse an " + ''.join([str(elem) for elem in Produkte[i-1]]) + ":")).grid(row=i)
        mProduktEingabe = Entry(Interface, width=20)
        mProduktEingabe.grid(row=i, column=1)
        if i == len(Produkte):
            mProduktConfirm = Button(Interface, text=u'\u2714', command=lambda: [getInputmProd(), createInputmOrg(i)])
            mProduktConfirm.grid(row=i, column=2)
        else:
            mProduktConfirm = Button(Interface, text=u'\u2714', command=lambda: [createInputmProd(i+1), getInputmProd()])
            mProduktConfirm.grid(row=i, column=2)

    def createInputmOrg(i):

        def getInputmOrg(event=None):
            global mOrgBindung
            mOrgBindung = float(mOrgEingabe.get())
            mOrgEingabe.config(state="disabled")
            mOrgConfirm.config(state="disabled")

        mOrgLabel = Label(Interface, text="Masse der Organischen Bindung:").grid(row=i+1)
        mOrgEingabe = Entry(Interface, width=20)
        mOrgEingabe.grid(row=i+1, column=1)
        mOrgConfirm = Button(Interface, text=u'\u2714', command=lambda: [getInputmOrg(), outputBindung(i)])
        mOrgConfirm.grid(row=i+1, column=2)

    def outputBindung(i):
        global Produkte
        Produkte = [[int(char) if char.isdigit() else char for char in sublist] for sublist in
                    Produkte]  # Zahlen zu Integer konvertieren
        for sublist in range(len(Produkte)):
            j = 0
            while j < len(Produkte[sublist]):
                if isinstance(Produkte[sublist][j], int):
                    if Produkte[sublist][j] == 1:
                        Produkte[sublist].pop(j)
                    else:
                        Produkte[sublist][j] -= 1
                        Produkte[sublist].insert(j, Produkte[sublist][j - 1])
                j += 1
        # molare Masse ermitteln
        molmProdukte = [molmasse(Produkt) for Produkt in Produkte]  # molare Massen der Produkte
        molmO2 = molmasse(['O', 'O'])  # molare Masse von Sauerstoff

        # Masse an O2 ermitteln
        mO2 = sum(mProdukte) - mOrgBindung

        # mol Anzahl ausrechnen
        molProdukte = [teilchenzahl(mProdukte[i], molmProdukte[i]) for i in range(0, len(Produkte))]
        molOedukt = teilchenzahl(mO2, molmO2) * 2

        # Atomanzahlen einzelne Elemente bestimmen
        Bindung = molElemente(molProdukte, Produkte, molOedukt)
        Bindung = {x: y for x, y in Bindung.items() if y != 0}
        minBindung = min(Bindung.values())
        for j, k in Bindung.items():
            Bindung[j] = k / minBindung
        BindungKeys = list(Bindung.keys())
        BindungKeys.sort()
        Bindung = {i: Bindung[i] for i in BindungKeys}

        BindungLabel = Label(Interface, text="Verhältnisse:").grid(row=i+2)
        BindungText = Label(Interface, text=Bindung).grid(row=i+2, column=1)

        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        Verhaeltnisformel = str()
        for l in Bindung:
            Verhaeltnisformel += l + str(round(Bindung[l]))
        Verhaeltnisformel = "(" + Verhaeltnisformel + ")" + "ₙ"
        Verhaeltnisformel = Verhaeltnisformel.translate(SUB)

        VerhaeltnisLabel = Label(Interface, text="Verhältnisformel:").grid(row=i+3)
        VerhaeltnisText = Label(Interface, text=Verhaeltnisformel).grid(row=i+3, column=1)


    ProduktLabel = Label(Interface, text="Produkte (Bsp: H2O CO2):").grid(row=0)
    ProduktEingabe = Entry(Interface, width=20)
    ProduktEingabe.grid(row=0, column=1)
    ProduktConfirm = Button(Interface, text=u'\u2714', command=getInputProd)
    ProduktConfirm.grid(row=0, column=2)

    menubar = Menu(Interface)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Zurrücksetzen", command=reset)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=Interface.quit)
    menubar.add_cascade(label="Datei", menu=filemenu)

    Interface.config(menu=menubar)
    Interface.mainloop()
Rechner()

"""
# Eingaben
Produkte = [list(char.upper()) for string in
                    np.array(input('Produkte (Bsp: H2O CO2): ').split()).reshape(-1, 1).tolist() for char in
                    string]
mProdukte = [float(input('Masse an ' + ''.join(elem) + ': ')) for elem in Produkte]
mOrgBindung = float(input('Masse der Organischen Bindung: '))
Produkte = [[int(char) if char.isdigit() else char for char in sublist] for sublist in
            Produkte]  # Zahlen zu Integer konvertieren

# Umschreiben von Bindungen (z.B CO2 -> COO)
for sublist in range(len(Produkte)):
    i = 0
    while i < len(Produkte[sublist]):
        if isinstance(Produkte[sublist][i], int):
            if Produkte[sublist][i] == 1:
                Produkte[sublist].pop(i)
            else:
                Produkte[sublist][i] -= 1
                Produkte[sublist].insert(i, Produkte[sublist][i - 1])
        i += 1

# molare Masse ermitteln
molmProdukte = [molmasse(Produkt) for Produkt in Produkte]  # molare Massen der Produkte
molmO2 = molmasse(['O', 'O'])  # molare Masse von Sauerstoff

# Masse an O2 ermitteln
mO2 = sum(mProdukte) - mOrgBindung

# mol Anzahl ausrechnen
molProdukte = [teilchenzahl(mProdukte[i], molmProdukte[i]) for i in range(0, len(Produkte))]
molOedukt = teilchenzahl(mO2, molmO2) * 2

# Atomanzahlen einzelne Elemente bestimmen
Bindung = molElemente(molProdukte, Produkte, molOedukt)
Bindung = {x: y for x, y in Bindung.items() if y != 0}
minBindung = min(Bindung.values())
for j, i in Bindung.items():
    Bindung[j] = i / minBindung

print('-----------------------------')
print("Verhältnisse:", Bindung)
print('-----------------------------')
print("Produkte:", Produkte)

print("mO2:", mO2)
print("molmO2:", molmO2)
print("molOedukt:", molOedukt)

print("mProdukte:", mProdukte)
print("molmProdukte:", molmProdukte)
print("molProdukte:", molProdukte)
"""
