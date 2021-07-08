import os
import socket
import tkinter as tk
import kivy #owo
import wmi

#ngl i think using kivy would be more ni1cer for the ui than tkinter coz it looks more modern, besides,
#its wat i use for ma fyp too :D -jul sux hehehe omg, its u (only old ppl know this reference)
#master programmer, use what you want. imma just do the functions that i was ASSigned




def processlist():
  while True:
    f = wmi.WMI() #initialize wmi constructor
    print("pid  Process name") #print header
    for process in f.Win32_Process(): #iterate through running processes
      print(f"{process.ProcessId:<10} {process.Name}") #display name and id of process
  break

  
