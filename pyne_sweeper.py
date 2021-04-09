#!/usr/bin/env python

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from random import random as rnd

COLORS = ('#000000','#ffffff','#0100fe','#017f01','#fe0000','#010080','#810102','#008081','#000000','#808080')
DELTAS = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))

class Combobox(ttk.Combobox):
    def __init__(self,root,command,**kwargs):
        kwargs['state'] = 'readonly'
        super().__init__(root,**kwargs)
        self.root = root
        self.command = command
        self.bind('<<ComboboxSelected>>',self.sel_clear)

    def sel_clear(self,event):
        self.selection_clear()
        self.root.focus()
        self.command()

class PyneSweeper:
    def __init__(self):
        self.mine_prob = 0.1
        self.game_over = False
        self.solving = False
        self.create_window()
        self.create_size()
        self.create_field()
        self.root.mainloop()

    def create_window(self):
        self.root = tk.Tk()
        self.root.title('PyneSweeper')
        self.title_label = tk.Label(self.root,text='PyneSweeper',font=(None,30))
        self.title_label.pack(side=tk.TOP)
        self.subtitle_label = tk.Label(self.root,text='A Python MineSweeper Solver',font=(None,20))
        self.subtitle_label.pack(side=tk.TOP)

    def create_size(self):
        self.size_frame = tk.Frame(self.root)
        self.size_frame.pack(side=tk.TOP)
        self.size_label = tk.Label(self.size_frame,text='Size')
        self.size_label.grid(row=0,column=0)
        self.size_combobox = Combobox(self.size_frame,self.resize_field,values=['10x10','20x20','40x20'])
        self.size_combobox.current(0)
        self.size_combobox.grid(row=0,column=1)

    def create_field(self):
        self.field_frame = tk.Frame(self.root)
        self.field_frame.pack(side=tk.TOP)
        self.buttons = []
        self.field = None
        self.solve_button = tk.Button(self.root,text='Solve',font=(None,20),command=self.solve)
        self.solve_button.pack(side=tk.TOP)
        self.resize_field()

    def resize_field(self):
        self.game_over = False
        for col in self.buttons:
            for b in col:
                b.destroy()
                del b
        del self.buttons
        del self.field
        self.x, self.y = (int(v) for v in self.size_combobox.get().split('x'))
        self.buttons = [[tk.Button(self.field_frame,width=1,font='bold') for y in range(self.y)]for x in range(self.x)]
        for x in range(self.x):
            for y in range(self.y):
                self.buttons[x][y].x = x
                self.buttons[x][y].y = y
                self.buttons[x][y].state = True
                self.buttons[x][y].bind('<Button-1>',self.left_click)
                self.buttons[x][y].bind('<Button-2>',self.right_click)
                self.buttons[x][y].bind('<Button-3>',self.right_click)
                self.buttons[x][y].grid(column=x,row=y)
        self.gen_mines()

    def gen_mines(self):
        self.field = np.zeros((self.x,self.y),dtype=np.int16)
        for x in range(self.x):
            for y in range(self.y):
                if rnd()<self.mine_prob:
                    self.field[x,y] = -1
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            if x+dx>-1 and x+dx<self.x and y+dy>-1 and y+dy<self.y and self.field[x+dx,y+dy]>-1:
                                self.field[x+dx,y+dy] += 1

    def left_click(self,event):
        if not self.game_over:
            b = event.widget
            self.open(b)

    def right_click(self,event):
        if not self.game_over:
            b = event.widget
            if b.state:
                if b['text']:
                    b['text'] = ''
                else:
                    b['text'] = 'X'

    def open(self,b):
        if b.state:
            self.display(b)
            if self.field[b.x,b.y]==-1:
                self.over()
            elif self.field[b.x,b.y]==0:
                for dx,dy in DELTAS:
                    if b.x+dx>-1 and b.x+dx<self.x and b.y+dy>-1 and b.y+dy<self.y:
                        self.open(self.buttons[b.x+dx][b.y+dy])

    def display(self,b):
        b.state = False
        b['state'] = 'disabled'
        n = self.field[b.x,b.y]
        b['text'] = n if n>0 else '' if n==0 else '@'
        b['disabledforeground'] = COLORS[n+1]
        b['relief'] = 'sunken'

    def over(self):
        self.game_over = True
        for col in self.buttons:
            for b in col:
                if b.state and self.field[b.x,b.y]==-1:
                    self.display(b)

    def solve(self):
        self.solving = True
        self.probs = np.zeros((self.x,self.y),dtype=np.float32)
        #self.solve_one()

    def solve_one(self):
        self.root.after(500,solve_one)

def main():
    ps = PyneSweeper()

if __name__ == '__main__':
    main()
