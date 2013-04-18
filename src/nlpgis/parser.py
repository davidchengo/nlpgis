'''
Created on Nov 26, 2012

@author: davidchen
'''
from Tkinter import *
from tkFont import *
from nltk import *
from nltk.tag.stanford import POSTagger
from nltk.corpus import conll2000
import nltk.chunk
import glob
import os, time
import csv
import codecs
from psycopg2 import connect 
import pprint
from nltk.stem.wordnet import WordNetLemmatizer
from class_spatial_query import *

class ParserGUI():
    def __init__(self, root):
        # self.spatial_relations=self.load_spatial_relations("")
        
        small_font = Font(family="Helvetica", size=8)
        medium_font = Font(family="Helvetica", size=10)
        big_font = Font(family="Helvetica", size=12)
        
        self.sample_question = "Where is Columbus?"
        
        # The question
        self.question_var = StringVar()        
        self.question_var.set(self.sample_question)
        w = Entry(root, textvariable=self.question_var, width=80, font=medium_font).grid(row=1, sticky=NW)
        
#        w=Button(root, text="Sample question",font=medium_font)
#        w.grid(row=1,sticky=NW)
#        w.bind("<Button-1>", self.load_sample_question)
        
        w = Button(root, text="Answer", command=self.answer_question, font=small_font)
        w.grid(row=1, column=2, sticky=NW)
        w.bind('<Return>', self.answer_question)
        
        self.answer_var = StringVar()        
        self.answer_var.set('Answer will show here.')
        w = Label(root, textvariable=self.answer_var, anchor=NW, justify=LEFT, wraplength=800, font=small_font).grid(row=3, sticky=NW)
        
    def load_sample_question(self, *args):
        self.question_var.set(self.sample_question)

    def answer_question(self, *args):
        print self.question_var.get()
        sq = SpatialQuery(self.question_var.get())
        result = sq.query()
        self.answer_var.set(result)
        

        
if __name__ == '__main__':

    root = Tk()
    # width x height + x_offset + y_offset:
    WIDTH = 800; HEIGHT = 300; X_OFFSET = 300; Y_OFFSET = 200;
    root.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, X_OFFSET, Y_OFFSET)) 
    root.title("NLP GIS")
    new_gui = ParserGUI(root)
    root.mainloop()
