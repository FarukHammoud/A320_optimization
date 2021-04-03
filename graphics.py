import numpy as np
from processing_py import *
import time

class Airbus320:
    
    def __init__(self):

        self.app = App(1709,500)    
        self.reset_background()
        self.color = np.random.choice(range(256), size=(181,3))

        self.p_matrix = None
        self.order = None
        self.compatible = None

        self.bx = None
        self.by = None
    
    def reset_background(self):
        back_image = self.app.loadImage('C:\\Users\\Faruk\\Desktop\\code\\A320_optimization\\A320.jpg')
        self.app.image(back_image,0,0)
        self.app.redraw()

    def load_dynamic(self, filename):
        
        def load_obj(filename):
            import pickle
            with open(filename, 'rb') as f:
                return pickle.load(f)
        
        result = load_obj(filename)
        self.p_matrix = result['p_matrix']
        self.order = result['order']
        self.compatible = result['compatible']

        self.find_barycenter()
    
    def load_static(self, filename):
        
        def load_obj(filename):
            import pickle
            with open(filename, 'rb') as f:
                return pickle.load(f)
        
        result = load_obj(filename)
        self.p_matrix = result['p_matrix']

        self.find_barycenter()

    def draw_passenger(self,row, column, color, category, shadow = False):

        # Fill with group color
        if shadow:
            self.app.fill(color[0],color[1],color[2],100)
        else:
            self.app.fill(color[0],color[1],color[2])
        # Stroke with caterory color
        
        self.app.stroke(0,0,0)
        # Find x,y in the drawing
        if row <= 9:
            x = 352+row*30
        elif row == 10:
            x = 363+row*30
        elif row <= 15:
            x = 372+row*30
        else:
            x = 374+row*30
        if column <=2:
            y = 146+column*20
        else:
            y = 176+column*20

        if category == 'Child':
            self.app.ellipse(x,y,10,10)
        else:
            self.app.ellipse(x,y,15,15)

    def draw_groups(self, groups = [], shadow = False):

        for row in range(30):
            for column in range(6):
                passenger = self.p_matrix[row][column]
                if not passenger is None:
                    if passenger['group'] in groups:
 
                        category = ''
                        if passenger['weight'] == '35':
                            category = 'Child'

                        group = passenger['group']
                        color = self.color[group]

                        self.draw_passenger(row,column,color,category,shadow)

        self.app.redraw()

    def draw_center_of_gravity(self):

        self.app.fill(255,0,0)
        self.app.noStroke()
        self.app.ellipse(372+self.bx*30,161+self.by*20,5,5)
        self.app.text('CG',380+self.bx*30,161+self.by*20)
        self.app.redraw()

    def find_barycenter(self):
       
        total_weight = 0
        bx, by = 0, 0
        for row in range(30):
            for column in range(6):
                passenger = self.p_matrix[row][column]
                if not passenger is None:
                    bx += passenger['weight']*row
                    by += passenger['weight']*column
                    total_weight += passenger['weight'] 
        by /= total_weight
        bx /= total_weight
        self.bx, self.by = bx, by

    def show_static(self):
        for row in range(30):
            for column in range(6):
                passenger = self.p_matrix[row][column]
                if not passenger is None:
 
                    category = ''
                    if passenger['weight'] == '35':
                        category = 'Child'

                    group = passenger['group']
                    color = self.color[group]

                    self.draw_passenger(row,column,color,category)
                    self.app.redraw()

        if not ((self.bx is None) or (self.by is None)):
            self.draw_center_of_gravity()
        
        self.app.redraw()

    def show_dynamic(self):

        self.reset_background()
        import time
        
        for group in self.order:
            shadow_groups = self.compatible[group]
            self.draw_groups(shadow_groups,shadow = True)
            time.sleep(0.5)
            self.draw_groups([group])
            time.sleep(0.5)
            self.reset_background()
        
        self.show_static()
    