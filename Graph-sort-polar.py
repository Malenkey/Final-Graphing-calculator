###################################################################################
#     ######      #        #    #   #      #  ##     ##       #####      ######   #
#     #          # #       #    #    #   #    #  # #  #      #     #     #        #
#     ###       ####       #    #      #      #   #   #      #     #     ######   #
#     #        #    #      #    #    #   #    #       #      #     #         #    #
#     #       #      #     ######  #       #  #       #       ####      ######    #
###################################################################################


################################importing libraries##########################


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, TextBox, Slider
from subprocess import call


#################################sorting equation###################################
def sorting(equation):
    temp = ['', '', '']  # creates a temporary store for the user input
    # temp has blanks spaces in order to help with indexing
    tempEquation = []  # temp equation is a revisited variable that hold processed data

    equation = str(equation)
    for i in equation:
        temp.append(i)
    temp.append('')  # creates an array of characters that make up the entered equation

    for i in range(len(temp)):
        tempcharacters = []  # used for two part indice processing

        match temp[i]:  # sorts through basic mathematical notation
            case '+':
                tempEquation.append(temp[i])
            case '-':
                tempEquation.append(temp[i])
            case '/':
                tempEquation.append(temp[i])
            case '*':
                tempEquation.append(temp[i])

            case 'e':  # sees if Euler's constant is being used
                match temp[i + 1]:
                    case '^':  # checks if e is set to the power of something
                        tempcounter = 2  # preset to iterate through equation

                        while temp[i + tempcounter] != 'x':  # checks for every integer before e
                            tempcounter = tempcounter + 1
                        tempstring = ''.join(temp[i + 2: i + tempcounter])  # temporary store for everything before x
                        tempnumber = i + tempcounter  # needed a secondary counter to reference at finalising
                        while temp[i + tempcounter + 1] != ')':
                            tempcounter = tempcounter + 1  # goes until the end of the function
                        tempEquation.append(
                            'np.exp(' + tempstring + '*' + ''.join(temp[tempnumber: i + tempcounter + 1]) + ')')
                        # tempstring is everything before x and then tempnumber is just after the x
            case 'x':  # searches for x to be a character
                match temp[i - 1]:
                    case ')':
                        tempEquation.append('x')
                match temp[i + 1]:
                    case '^':  # searches whether it is x with an indice
                        tempcounter = 2
                        tempcounter2 = 1
                        trig = False  # makes sure x in a trig function isn't appened twice
                        bracket = False  # initialises bracket loop
                        while not bracket:
                            if temp[i - tempcounter2] == '^':  # checks whether its x raised to the x power
                                bracket = True
                            if temp[i - tempcounter2] == '':  # checks if x is at the start
                                bracket = True
                            if temp[i - tempcounter2] == '(':  # checks whether it's the start of a function
                                bracket = True
                            if temp[i - tempcounter2] == ')':  # checks if it is in front of a function
                                bracket = True
                            tempcounter2 = tempcounter2 + 1

                        if temp[i - tempcounter2] == 'n':  # n would only be present if it is inside sin or tan
                            trig = True
                        if temp[i - tempcounter2] == 's':  # s would only be present if it is inside cos
                            trig = True
                        if temp[i - tempcounter2] == 'e':  # would only be present if Eulers constant is in use
                            trig = True


                        else:

                            while temp[i + tempcounter].isdigit():  # sorts through the power of x till ')' is found
                                tempcounter = tempcounter + 1
                        if not trig:  # appends the power joined with x**
                            tempEquation.append('x**' + ''.join(temp[i + 2: i + tempcounter]))
                    case _:
                        tempEquation.append('x')

        match ''.join(temp[i:i + 3]):
            case 'sin':  # checks whether the first 3 letters is sin
                match temp[i + 3]:  # checks whether the next letter is a bracket
                    case '(':  # if the next letter is a bracket
                        bracket = True
                        tempcounter = 1
                        while bracket:
                            while tempcounter != 0:
                                if temp[i + 3 + tempcounter] == ')':
                                    tempEquation.append('np.sin(' + ''.join(tempcharacters) + ')')
                                    bracket = False  # exits bracket loop
                                    tempcounter = 0  # exits tempcounter loop
                                else:
                                    tempcharacters.append(temp[i + 3 + tempcounter])  # appends next character along
                                    tempcounter = tempcounter + 1  # increments counter so next character is processed

                    case _:
                        print('error')

            case 'cos':  # match case changed from sin to cos
                match temp[i + 3]:
                    case '(':
                        bracket = True
                        tempcounter = 1
                        while bracket:
                            while tempcounter != 0:
                                if temp[i + 3 + tempcounter] == ')':
                                    tempEquation.append('np.cos(' + ''.join(tempcharacters) + ')')
                                    bracket = False
                                    tempcounter = 0
                                else:
                                    tempcharacters.append(temp[i + 3 + tempcounter])
                                    tempcounter = tempcounter + 1

                    case _:
                        print('error')

            case 'tan':
                match temp[i + 3]:
                    case '(':
                        bracket = True
                        tempcounter = 1
                        while bracket:
                            while tempcounter != 0:
                                if temp[i + 3 + tempcounter] == ')':
                                    tempEquation.append('np.tan(' + ''.join(tempcharacters) + ')')
                                    bracket = False
                                    tempcounter = 0
                                else:
                                    tempcharacters.append(temp[i + 3 + tempcounter])
                                    tempcounter = tempcounter + 1

                    case _:
                        print('error')

    equation = []

    tempEquation = ['(' + x + ')' for x in tempEquation]  # surrounds every element with parenthesis
    for i in range(len(tempEquation)):
        equation.append(tempEquation[i])  # takes the element from temp
        equation.append('*')  # multiplies it by the next element

    equation.pop()  # removes the final '*'
    final = ''.join(equation)  # converts equation into a string

    ydata = eval(final)  # copied from old submit function
    l.set_ydata(ydata)
    ax.set_ylim(np.min(ydata), np.max(ydata))
    plt.draw()


##############################defining functions and routines##############################


def grid(this_text_needs_to_be_here):
    ax.grid()  # updates grid state
    fig.canvas.draw()  # redraws canvas with updated data


def colorfunc(label):
    l.set_color(label)  # sets colour to
    plt.draw()


def stylefunc(label):
    l.set_linestyle(label)
    plt.draw()


def polar_toggle(text):
    call(["python", "PolarGraph.py"])


#######################################defining variables###########################################################

x_startValue = 100

initial_text = ""

x = np.arange(-(float(x_startValue)), float(x_startValue), 0.01)
y = x

fig, ax = plt.subplots()
ax.grid(True)
l, = ax.plot(x, y, lw=2, color='red')  # (x axis increments, y axis increments , line width, line color)
fig.subplots_adjust(left=0.3, right=0.99)

Widget_colour = 'lightgoldenrodyellow'

####################################################creating interactive widgets###################################
ax_grid = plt.axes([0.1, 0.75, 0.07, 0.05])

ax_box = plt.axes([0.05, 0.6, 0.2, 0.06])

ax_line_option = fig.add_axes([0.1, 0.8, 0.07, 0.15], facecolor=Widget_colour)

ax_color = fig.add_axes([0.02, 0.7, 0.08, 0.25], facecolor=Widget_colour)

ax_polar_button = plt.axes([0.1, 0.7, 0.07, 0.05])

grid_button = Button(ax_grid, 'Grid', color=Widget_colour, hovercolor='grey')

polar_button = Button(ax_polar_button, 'Polar', color=Widget_colour, hovercolor='grey')

color_button = RadioButtons(ax_color, ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'))

line_option = RadioButtons(ax_line_option, ('-', '--', '-.', ':'))

text_box = TextBox(ax_box, 'Evaluate', initial=initial_text)

################################## when interacted with ###################################################

text_box.on_submit(sorting)

grid_button.on_clicked(grid)

color_button.on_clicked(colorfunc)

line_option.on_clicked(stylefunc)

polar_button.on_clicked(polar_toggle)

plt.show()
