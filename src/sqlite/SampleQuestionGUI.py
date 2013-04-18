'''
Created on Nov 1, 2012

@author: davidchen
'''
from Tkinter import *

class App:
  def __init__(self, master):
    #add a child widget frame to the master
      self.frame = Frame(master)
      self.frame.pack()
      w = Label(root, text="Hello, world!")
      w.pack()
      self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
      self.button.pack(side=LEFT)
      self.hi_there = Button(self.frame, text="Hello", command=self.say_hi)
      self.hi_there.pack(side=LEFT)

  def say_hi(self):
      print "hi there, everyone!"
      
if __name__ == '__main__':
  root=Tk()
  #add a label to the main window
#  w = tk.Label(root, text="Hello, world!")
#  w.pack()
  app = App(root)
  root.mainloop()