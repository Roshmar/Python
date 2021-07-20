# imports
from termcolor import colored
from tkinter import *
from tkmacosx import Button
from tkinter import messagebox



# defines
SIZE = 4
POINT = 0
FIRST_X = 0
FIRST_Y = 0
LAST_TYPED_X = 1
LAST_TYPED_Y = 1
SUCCESS = True
BUTTON_SIZE = 400/SIZE
RESET = False
STEPS = 0
LEVEL = 0
LEVEL_COUNTER = 0



master = Tk()
master.title("Flow free")
master.minsize(width=700, height=400)
# master.attributes("-fullscreen", True)
master.config(bg='black')


button_map = [[Button()] * SIZE for i in range(SIZE)]

def create_button_map(field):
    global SIZE, button_map
    button_map = [[Button()] * SIZE for i in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            button_map[i][j] = Button(master, text='',padx=0, bg=field.get_color_of_cell(i, j), fg='black', height = BUTTON_SIZE, width = BUTTON_SIZE, borderless=50 ,border = 0, borderwidth=0, command =lambda: choose_mode(field,SIZE-i,j+1))
            button_map[i][j] .grid(row=i+1, column=j+1) 


OUTPUT = StringVar()
OUTPUT_COLOR = 'green'

output = Label(master, bg='black',anchor='w')
occupancy = Label(master, bg='black')
step_count = Label(master, bg='black',anchor='w')
level = Label(master, bg='black',anchor='w')


# master.wm_attributes("-transparent", 'grey')


# labelText = StringVar()

class Cell:
    value = 0
    color = ''

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    #не використовувати!!! присвоює значення всьому рядку а не тільки одній клітиці!!!
    def set_value(self, value):
        self.value = value

    def get_color(self):
        if self.value == 1:
            self.color = '#ffff7a'
        elif self.value == 2:
            self.color = 'yellow'
        elif self.value == 3:
             self.color = '#4d4dff'
        elif self.value == 6:
            self.color = 'blue'
        elif self.value == 5 :
            self.color = '#3bff3b'
        elif self.value == 10:
            self.color = 'green'
        elif self.value == 7 :
            self.color = '#ff4d4d'
        elif self.value == 14:
            self.color = 'red'
        elif self.value == 11 :
            self.color = '#ff0080'
        elif self.value == 22:
            self.color = 'magenta'
        elif self.value == 13 :
            self.color = '#CCFFFF'
        elif self.value == 26:
            self.color = 'cyan'
        else:
            self.color = 'black'
        return self.color


# перевірка вступів
def check_int(message):
    while True:
        test = [[Cell(0)] * SIZE for i in range(SIZE)]
        var = input(message)
        success = True

        try:
            var = int(var)
            test[SIZE - var][var - 1] = Cell(1)
        except IndexError:
            print(colored('"' + str(var) + '"' + ' is an invalid input! Please repeat! ', 'red'))
            success = False
        except ValueError:
            print(colored('"' + str(var) + '"' + ' is an invalid input! Please repeat! ', 'red'))
            success = False
        except Exception as exception:
            print(colored(exception, 'red'))
            success = False

        if not success:
            continue
        return var


# todo core
# Карта
class Map:
    global SIZE, OUTPUT
    maps = [[Cell(0)] * SIZE for i in range(SIZE)]

    def clean_map(self):
        self.maps = [[Cell(0)] * SIZE for i in range(SIZE)]

    def level_with_two_points(self,_first_pos_X1,_first_pos_Y1,_second_pos_X1,_second_pos_Y1, _first_pos_X2,_first_pos_Y2,_second_pos_X2,_second_pos_Y2):
        global SIZE
        self.maps[SIZE - _first_pos_X1][_first_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _second_pos_X1][_second_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _first_pos_X2][_first_pos_Y2 - 1] = Cell(6)
        self.maps[SIZE - _second_pos_X2][_second_pos_Y2 - 1] = Cell(6)
        return self.maps

    def level_with_three_points(self,_first_pos_X1,_first_pos_Y1,_second_pos_X1,_second_pos_Y1, _first_pos_X2,_first_pos_Y2,_second_pos_X2,_second_pos_Y2,   _first_pos_X3,_first_pos_Y3,_second_pos_X3,_second_pos_Y3):
        global SIZE
        self.maps[SIZE - _first_pos_X1][_first_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _second_pos_X1][_second_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _first_pos_X2][_first_pos_Y2 - 1] = Cell(6)
        self.maps[SIZE - _second_pos_X2][_second_pos_Y2 - 1] = Cell(6)
        self.maps[SIZE - _first_pos_X3][_first_pos_Y3 - 1] = Cell(10)
        self.maps[SIZE - _second_pos_X3][_second_pos_Y3 - 1] = Cell(10)
        return self.maps

    def level_with_four_points(self,_first_pos_X1,_first_pos_Y1,_second_pos_X1,_second_pos_Y1, _first_pos_X2,_first_pos_Y2,_second_pos_X2,_second_pos_Y2,   _first_pos_X3,_first_pos_Y3,_second_pos_X3,_second_pos_Y3, _first_pos_X4,_first_pos_Y4,_second_pos_X4,_second_pos_Y4):
        global SIZE
        self.maps[SIZE - _first_pos_X1][_first_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _second_pos_X1][_second_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _first_pos_X2][_first_pos_Y2 - 1] = Cell(6)
        self.maps[SIZE - _second_pos_X2][_second_pos_Y2 - 1] = Cell(6)
        self.maps[SIZE - _first_pos_X3][_first_pos_Y3 - 1] = Cell(10)
        self.maps[SIZE - _second_pos_X3][_second_pos_Y3 - 1] = Cell(10)
        self.maps[SIZE - _first_pos_X4][_first_pos_Y4 - 1] = Cell(14)
        self.maps[SIZE - _second_pos_X4][_second_pos_Y4 - 1] = Cell(14)
        return self.maps

    def level_with_five_points(self,_first_pos_X1,_first_pos_Y1,_second_pos_X1,_second_pos_Y1, _first_pos_X2,_first_pos_Y2,_second_pos_X2,_second_pos_Y2,   _first_pos_X3,_first_pos_Y3,_second_pos_X3,_second_pos_Y3, _first_pos_X4,_first_pos_Y4,_second_pos_X4,_second_pos_Y4 ,_first_pos_X5,_first_pos_Y5,_second_pos_X5,_second_pos_Y5):
        global SIZE
        self.maps[SIZE - _first_pos_X1][_first_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _second_pos_X1][_second_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _first_pos_X2][_first_pos_Y2 - 1] = Cell(6)
        self.maps[SIZE - _second_pos_X2][_second_pos_Y2 - 1] = Cell(6)
        self.maps[SIZE - _first_pos_X3][_first_pos_Y3 - 1] = Cell(10)
        self.maps[SIZE - _second_pos_X3][_second_pos_Y3 - 1] = Cell(10)
        self.maps[SIZE - _first_pos_X4][_first_pos_Y4 - 1] = Cell(14)
        self.maps[SIZE - _second_pos_X4][_second_pos_Y4 - 1] = Cell(14)
        self.maps[SIZE - _first_pos_X5][_first_pos_Y5 - 1] = Cell(22)
        self.maps[SIZE - _second_pos_X5][_second_pos_Y5 - 1] = Cell(22)
        return self.maps

    def level_with_six_points(self,_first_pos_X1,_first_pos_Y1,_second_pos_X1,_second_pos_Y1, _first_pos_X2,_first_pos_Y2,_second_pos_X2,_second_pos_Y2,   _first_pos_X3,_first_pos_Y3,_second_pos_X3,_second_pos_Y3, _first_pos_X4,_first_pos_Y4,_second_pos_X4,_second_pos_Y4 ,_first_pos_X5,_first_pos_Y5,_second_pos_X5,_second_pos_Y5, _first_pos_X6,_first_pos_Y6,_second_pos_X6,_second_pos_Y6):
        global SIZE
        self.maps[SIZE - _first_pos_X1][_first_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _second_pos_X1][_second_pos_Y1 - 1] = Cell(2)
        self.maps[SIZE - _first_pos_X2][_first_pos_Y2 - 1] = Cell(6)
        self.maps[SIZE - _second_pos_X2][_second_pos_Y2 - 1] = Cell(6)
        self.maps[SIZE - _first_pos_X3][_first_pos_Y3 - 1] = Cell(10)
        self.maps[SIZE - _second_pos_X3][_second_pos_Y3 - 1] = Cell(10)
        self.maps[SIZE - _first_pos_X4][_first_pos_Y4 - 1] = Cell(14)
        self.maps[SIZE - _second_pos_X4][_second_pos_Y4 - 1] = Cell(14)
        self.maps[SIZE - _first_pos_X5][_first_pos_Y5 - 1] = Cell(22)
        self.maps[SIZE - _second_pos_X5][_second_pos_Y5 - 1] = Cell(22)
        self.maps[SIZE - _first_pos_X6][_first_pos_Y6 - 1] = Cell(26)
        self.maps[SIZE - _second_pos_X6][_second_pos_Y6 - 1] = Cell(26)
        return self.maps
        
    def first_level(self):
        global LEVEL, SIZE, BUTTON_SIZE, LEVEL_COUNTER
        LEVEL = 1
        SIZE = 5
        LEVEL_COUNTER = LEVEL_COUNTER + 1
        BUTTON_SIZE = 400/SIZE
        self.clean_map()
        create_button_map(self)
        self.level_with_four_points(1,1,2,5,2,4,4,4,3,2,3,4,5,1,3,5)

    def second_level(self):
        global LEVEL, SIZE, BUTTON_SIZE, LEVEL_COUNTER
        LEVEL = 2
        LEVEL_COUNTER = LEVEL_COUNTER + 1
        BUTTON_SIZE = 400/5
        destroy_table(self)

        SIZE = 5
        self.clean_map()
        create_button_map(self)
        print(colored('Second Level has been started', 'green'))
        OUTPUT.set('Second Level')
        self.level_with_five_points(5,1,1,2,2,2,5,3,1,3,4,3,2,4,5,5,1,4,4,5)

    def third_level(self):
        global LEVEL, SIZE, BUTTON_SIZE, LEVEL_COUNTER
        LEVEL = 3
        LEVEL_COUNTER = LEVEL_COUNTER + 1
        BUTTON_SIZE = 400/8
        destroy_table(self)

        SIZE = 8
        self.clean_map()
        create_button_map(self)
        print(colored('Third Level has been started', 'green'))
        OUTPUT.set('Third Level')
        self.level_with_six_points(1,2,8,5,7,5,6,8,6,5,7,7,6,6,7,8,5,4,4,5,3,5,5,5)
        
    def fourth_level(self):
        global LEVEL, SIZE, BUTTON_SIZE, LEVEL_COUNTER
        LEVEL = 4
        LEVEL_COUNTER = LEVEL_COUNTER + 1
        BUTTON_SIZE = 400/SIZE
        destroy_table(self)

        SIZE =  8
        self.clean_map()
        create_button_map(self)
        print(colored('Fourth Level has been started', 'green'))
        OUTPUT.set('Fourth Level')
        self.level_with_six_points(1,4,8,2,2,3,6,6,1,8,5,7,2,6,2,8,4,4,6,5,4,5,3,8)

    def fifth_level(self):
        global LEVEL, SIZE, BUTTON_SIZE, LEVEL_COUNTER
        LEVEL = 2
        LEVEL_COUNTER = LEVEL_COUNTER + 1
        BUTTON_SIZE = 400/5
        destroy_table(self)

        SIZE = 5
        self.clean_map()
        create_button_map(self)
        print(colored('Second Level has been started', 'green'))
        OUTPUT.set('Second Level')
        self.level_with_five_points(5,1,1,2,2,2,5,3,1,3,4,3,2,4,5,5,1,4,4,5)

    

    def print_map(self):
        for i in range(len(self.maps)):
            for j in range(len(self.maps[i])):
                if self.maps[i][j].get_color() != 'black' and  self.maps[i][j].get_color() != '#ffff7a' and  self.maps[i][j].get_color() != '#4d4dff' and self.maps[i][j].get_color() != '#3bff3b' and self.maps[i][j].get_color() !='#ff4d4d' and self.maps[i][j].get_color() != '#ff0080' and self.maps[i][j].get_color() != '#CCFFFF':
                    print(colored(self.maps[i][j].get_value(), self.maps[i][j].get_color()), end=' ')
                elif self.maps[i][j].get_color() == 'black':
                    print(colored(self.maps[i][j].get_value(), 'grey'), end=' ')
                elif self.maps[i][j].get_color() == '#ffff7a':
                    print(colored(self.maps[i][j].get_value(), 'yellow'), end=' ')
                elif self.maps[i][j].get_color() == '#4d4dff':
                    print(colored(self.maps[i][j].get_value(), 'blue'), end=' ')
                elif self.maps[i][j].get_color() == '#3bff3b':
                    print(colored(self.maps[i][j].get_value(), 'green'), end=' ')
                elif self.maps[i][j].get_color() == '#ff4d4d':
                    print(colored(self.maps[i][j].get_value(), 'red'), end=' ')
                elif self.maps[i][j].get_color() == '#ff0080':
                    print(colored(self.maps[i][j].get_value(), 'magenta'), end=' ')
                elif self.maps[i][j].get_color() == '#CCFFFF':
                    print(colored(self.maps[i][j].get_value(), 'cyan'), end=' ')
            print()


    def is_win(self):
        for i in range(len(self.maps)):
            for j in range(len(self.maps[i])):
                if self.maps[i][j].get_value() == 0:
                    return False
        OUTPUT.set('YOU WIN!!!')
        OUTPUT_COLOR = 'green'
        print(colored('YOU WIN!!!', 'green'))


        return True

    def get_color_of_cell(self, _pos_X, _pos_Y):
        return self.maps[_pos_X][_pos_Y].get_color()
    
    def get_level(self):
        return self.LEVEL


# перший крок
def make_first_step(_map, _pos_X, _pos_Y):
    global POINT, FIRST_X, FIRST_Y, LAST_TYPED_X, LAST_TYPED_Y, SUCCESS, STEPS, OUTPUT, OUTPUT_COLOR
    STEPS = STEPS + 1
    SUCCESS = True
    FIRST_X = _pos_X
    FIRST_Y = _pos_Y
    
    print(colored('First pick', 'yellow'))
    print(colored('Type X: ', 'yellow') + str(_pos_X))
    print(colored('Type Y: ', 'yellow') + str(_pos_Y))
    LAST_TYPED_X = _pos_X
    LAST_TYPED_Y = _pos_Y
    if _map.maps[SIZE - FIRST_X][FIRST_Y - 1].get_value() % 2 == 0 and _map.maps[SIZE - FIRST_X][FIRST_Y - 1].get_value() != 0:
        POINT = _map.maps[SIZE - FIRST_X][FIRST_Y - 1].get_value()
        clean_map(_map)
        _map.print_map()
        update_table(_map)
        print(FIRST_X,FIRST_Y)
        print(colored('You picked: ' + str(_map.get_color_of_cell(SIZE - _pos_X,_pos_Y - 1)) +  ' color', 'green'))
        OUTPUT.set('You picked: ' + str(_map.get_color_of_cell(SIZE - _pos_X,_pos_Y - 1)) + ' color')
        OUTPUT_COLOR = str(_map.maps[SIZE - _pos_X][_pos_Y - 1].get_color())
        print(colored('=================', 'yellow'))
        print(colored('\n=================', 'yellow'))
    else:
        SUCCESS = False
        print(colored('This is not a start point! Please repeat! ', 'red'))
        OUTPUT.set('This is not a start point!')
        OUTPUT_COLOR = 'red'
        POINT = 0


# Кроки
def make_step(_map, _pos_X, _pos_Y):
    global STEPS, OUTPUT, POINT, FIRST_X, FIRST_Y, LAST_TYPED_Y, LAST_TYPED_X, SUCCESS, OUTPUT_COLOR
    STEPS = STEPS + 1
    print(colored('Type X: ', 'yellow') + str(_pos_X))
    print(colored('Type Y: ', 'yellow') + str(_pos_Y))
    if (_map.maps[SIZE - _pos_X][_pos_Y - 1].get_value() == 0 and POINT != 0 and (((LAST_TYPED_X - 1 <= _pos_X <= LAST_TYPED_X + 1 and _pos_Y == LAST_TYPED_Y) or (_pos_X == LAST_TYPED_X and LAST_TYPED_Y - 1 <= _pos_Y <= LAST_TYPED_Y + 1)))) :
        _map.maps[SIZE - _pos_X][_pos_Y - 1] = Cell(int(POINT / 2))
        LAST_TYPED_X = _pos_X
        LAST_TYPED_Y = _pos_Y

    elif POINT != 0 and _map.maps[SIZE - _pos_X][_pos_Y - 1].get_value() == POINT and _map.maps[SIZE - _pos_X][_pos_Y - 1].get_value() % 2 == 0 and ( not (FIRST_X == _pos_X and FIRST_Y == _pos_Y)) and ((LAST_TYPED_X - 1 <= _pos_X <= LAST_TYPED_X + 1 and _pos_Y == LAST_TYPED_Y) or (_pos_X == LAST_TYPED_X and LAST_TYPED_Y - 1 <= _pos_Y <= LAST_TYPED_Y + 1)):
        print(colored('success', 'green'))
        OUTPUT.set('Success!')
        OUTPUT_COLOR = 'green'
        POINT = 0
        FIRST_X = 0
        FIRST_Y = 0
        clean_map(_map)
        
    elif POINT != 0 :
        print(colored('Map has been cleared','red'))
        OUTPUT.set('Map has been cleared')
        OUTPUT_COLOR = 'red'
        clean_map(_map)
        POINT = 0
        # FIRST_X = 0
        # FIRST_Y = 0

    _map.print_map()
    print(calculate_percents(_map))
    print(calculate_steps(STEPS))
    print(colored('=================', 'yellow'))
    print(colored('\n=================', 'yellow'))

def calculate_percents(_field):
    temp = 0
    count_point = 0
    for i in range(len(_field.maps)):
        for j in range(len(_field.maps[i])):
            if _field.maps[i][j].get_value() != 0 and _field.maps[i][j].get_value()%2 == 1: 
                temp = temp + 1
            elif _field.maps[i][j].get_value() != 0 and _field.maps[i][j].get_value()%2 == 0:
                count_point = count_point + 1
    return 'Occupancy: ' + str(int((temp/((SIZE*SIZE) - count_point))*100) )+'%'

def calculate_steps(_steps):
    return 'Steps: ' + str(STEPS)

# Очистка карти
def clean_map(_map):
    global FIRST_X, FIRST_Y, OUTPUT
    for i in range(len(_map.maps)):
        for j in range(len(_map.maps[i])):
            if _map.maps[i][j].get_value() == POINT / 2:
                _map.maps[i][j] = Cell(0)
                FIRST_X = 0
                FIRST_Y = 0

    
def choose_mode(_field, _pos_X, _pos_Y):
    global POINT, LEVEL, STEPS, OUTPUT 
    if not _field.is_win():
        update_table(_field)
        if POINT == 0:
            make_first_step(_field, _pos_X, _pos_Y)
        
        else:
            make_step(_field, _pos_X, _pos_Y)
        update_table(_field)
    else:
        
        print()
        STEPS = 0
        POINT = 0
        if LEVEL == 1:
            _field.second_level()
        elif LEVEL == 2:
            _field.third_level()
        elif LEVEL == 3:
            _field.fourth_level()
        elif LEVEL == 4:
            _field.fifth_level()
        else:
            _field.second_level()
        
        update_table(_field)



def update_table(_field):
    global button_map, OUTPUT, BUTTON_SIZE, SIZE,LEVEL_COUNTER
    for i in range(SIZE):
        for j in range(SIZE):
            button_map[i][j].config(text='',padx=0, bg=_field.get_color_of_cell(i, j), fg='black', height = BUTTON_SIZE, width = BUTTON_SIZE, borderless=50 ,border = 0, borderwidth=0, command = lambda i=i, j=j: choose_mode(_field,SIZE-i,j+1))
            button_map[i][j].grid(row=i+1,column=j+1)

    step_count.grid(row=1, column=(SIZE+1))
    step_count.config(text=calculate_steps(STEPS), fg='green')
    output.grid(row=int(SIZE/2), column=(SIZE+1))
    output.config(text=OUTPUT.get(), fg=OUTPUT_COLOR)
    occupancy.grid(row=SIZE, column=(SIZE+1))
    occupancy.config(text=calculate_percents(field), fg='green')
    level.grid(row=int((SIZE/2)+1),column=(SIZE+1))
    level.config(text='Level: ' + str(LEVEL_COUNTER), fg='green')
    
    

def destroy_table(_field):
    global button_map, OUTPUT, BUTTON_SIZE, SIZE
    for i in range(len(_field.maps)):
        for j in range(len(_field.maps[i])):
            button_map[i][j].destroy()




# todo int main()
# todo КОНСОЛЬ
print(colored('=================', 'yellow'))
field = Map()
field.first_level()


        
field.print_map()
# create_button_map(field)
print(colored('=================', 'yellow'))

update_table(field)


master.mainloop()





