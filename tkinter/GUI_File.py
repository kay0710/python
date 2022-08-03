from tkinter import Tk, ttk, Label, Button, Text, END
import json

list_stationFares = []
with open('GUI_File.json', 'r') as stationfares_file:
    list_stationFares = json.load(stationfares_file)

idx_selected_list = 0

def stationfares_selected(event):
    global idx_selected_list
    for item in treeStationFares.selection():
        idx_selected_list = int(treeStationFares.item(item, 'text'))
    tmp_stationFares = list_stationFares[idx_selected_list]
    destination = tmp_stationFares['destination']
    fare = str(tmp_stationFares['fare'])
    txt_station.delete("1.0", END)
    txt_station.insert("end", destination)
    txt_fare.delete("1.0", END)
    txt_fare.insert("end", fare)

def setTreeItems():
    treeStationFares.delete(*treeStationFares.get_children()) # 기존에 treeStatioFares 에 있는 값들을 지워서 저장했던 내용들을 불러서 저장
    for idx, tmp_stationFares in enumerate(list_stationFares):
        destination = tmp_stationFares['destination']
        fare = tmp_stationFares['fare']
        treeStationFares.insert("", 'end', iid=None, text=str(idx), values=[destination, fare])

def insert_content():
    destination = txt_station.get("1.0", END)
    fare = int(txt_fare.get('1.0', END))
    dict_stationFares = {'destination':destination.rstrip(), 'fare':fare}   # rstrip(): 계획문자의 입력을 방지 (ex \n)
    list_stationFares.append(dict_stationFares)
    setTreeItems()

def update_content():
    global idx_selected_list
    destination = txt_station.get('1.0', END)
    fare = int(txt_fare.get('1.0', END))
    selectedItem = list_stationFares[idx_selected_list]
    selectedItem['destination'] = destination.rstrip()
    selectedItem['fare'] = fare
    setTreeItems()

def delete_content():
    global idx_selected_list
    list_stationFares.pop(idx_selected_list)
    setTreeItems()

def save_content():
    with open('GUI_File.json', 'w',) as f:  ## 한글 표현 시: endcoding='UTF-8'
        jsonString = json.dumps(list_stationFares, ) ## 한글 표현 시: ensure_ascii=False
        f.write(jsonString)
    f.close() # 꼭 해줄 것!!

 
window = Tk()
window.title("Station Fare Management")
window.geometry("600x600")
window.resizable(0,0) # 0,0 >> unresizable
title="Management System"
lbl_title = Label(window, text=title, font=('consolas', 20))
lbl_title.pack(padx=5, pady=15)

treeStationFares = ttk.Treeview(window)
treeStationFares['column'] = ['destination', 'fare']
treeStationFares.column("#0", width=50)
treeStationFares.column("destination", width=200)
treeStationFares.column("fare", width=150)
treeStationFares.heading("#0", text='Num')
treeStationFares.heading("destination", text='Station Name')
treeStationFares.heading("fare", text='Fare')
treeStationFares.place(x=100, y=100, width=400, height=250)
treeStationFares.bind("<<TreeviewSelect>>", stationfares_selected) # <<TreeviewSelect>> 라는 triger event 발새 시 stationfares_selected 라는 함수에 bind

lbl_station = Label(window, text='Station')
lbl_station.place(x=100, y=450, width=50, height=25)
lbl_fare = Label(window, text="Fare")
lbl_fare.place(x=100, y=500, width=50, height=25)

txt_station = Text(window, width=30, height=1)
txt_station.place(x=200, y=450)
txt_fare = Text(window, width=30, height=1)
txt_fare.place(x=200, y=500)

btn_insert = Button(window, text="Insert", command=insert_content, font=('consolas',14))
btn_insert.place(x=100, y=400, width=100, height=30)
btn_update = Button(window, text="Update", command=update_content, font=('consolas', 14))
btn_update.place(x=200, y=400, width=100, height=30)
btn_delete = Button(window, text="Delete", command=delete_content, font=('consolas', 14))
btn_delete.place(x=300, y=400, width=100, height=30)
btn_save = Button(window, text="Save", command=save_content, font=('consolas',14))
btn_save.place(x=400, y=400, width=100, height=30)

setTreeItems()

window.mainloop()


