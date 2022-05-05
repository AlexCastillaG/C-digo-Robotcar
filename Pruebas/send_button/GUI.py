import PySimpleGUI as sg

layout = [[sg.Checkbox('My Checkbox', default=False)]]
window = sg.Window("5G RobotCar", layout,size=(900,700),element_justification='c',background_color="white")

while True:
    event, values = window.read()
    window.Refresh()


    if event == sg.WIN_CLOSED:
        break
window.close()