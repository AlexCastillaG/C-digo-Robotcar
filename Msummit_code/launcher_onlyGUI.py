import GUI_module
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Titlebar, Window


car_GUI = GUI_module.car_Interface("GUI_netinfo.txt")
car_GUI.start_GUI()