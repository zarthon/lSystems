
def Lindenmayer(axiom,rules):

    rules = rules.items()
    def apply_rule(axiom,(symbol,replacement)):    
        return axiom.replace(symbol,replacement.lower())

    while True:
        # Create a generator function
        yield axiom
        #get the next iteration of the system
        axiom = reduce(apply_rule,rules,axiom).upper()

class GenerateList(object):
    def __init__(self,generator):
        self.__generator = generator
        self.__list = []

    #to store the previous iterations
    def __getitem__(self,index):
        for i in range(index-len(self.__list) +1):
            self.__list.append(self.__generator.next())
        return self.__list[index]

class L_System(GenerateList):
    """
    Sample class to manipulate the L String generated by Lindenmayer function defined above.

    It is expected that the user follows the following convention to define the rules, Source
    http://en.wikipedia.org/wiki/L-system

    'F': Draw a Line
    '+': Turn Right by predefined angle i.e. objects angle
    '-': Turn Left by predefined angle
    'G': Move forward without drawing
    ']': Restore previously saved states
    '[': Save current state

    """
    def __init__(self,turtle,start,rules,angle,heading=0):
        self.turtle = turtle
        self.states = []
        self.angle = angle
        self.heading = heading
        self.actions = {
            'F': self.forward,
            '+': self.right,
            '-': self.left,
            'G': self.go,
            '[': self.save,
            ']': self.restore,
        }
        super(L_System, self).__init__(Lindenmayer(start, rules))

    def forward(self):
        self.turtle.forward(self.size)

    def right(self):
        self.turtle.right(self.angle)

    def left(self):
        self.turtle.left(self.angle)

    def go(self):
        self.turtle.up()
        self.turtle.forward(self.size)
        self.turtle.down()

    def save(self):
        x, y = self.turtle.xcor(), self.turtle.ycor()
        h, c = self.turtle.heading(), self.turtle.pencolor()
        self.states.append((x, y, h, c))

    def restore(self):
        turtle.up()
        x, y, h, c = self.states.pop()
        turtle.setx(x)
        turtle.sety(y)
        turtle.setheading(h)
        turtle.pencolor(c)
        turtle.down()

    def update(self):
        pass

    def draw(self, index, size=8):
        self.turtle.setheading(self.heading)
        self.size = size
        for char in self[index]:
            if char in self.actions:
                self.update()
                self.actions[char]()

 

if __name__=='__main__':
    import sys
    from turtle import Turtle
    turtle = Turtle()
    turtle.hideturtle()
    turtle.speed('fastest')
    turtle.screen.colormode(255)
    turtle.up()
    turtle.setposition(-200, 200)
    turtle.down()

    fractals = {
        'snowflake': L_System(turtle, 'F++F++F', {'F': 'F-F++F-F'}, 60),
        'dragon': L_System(turtle, 'FX', {'X': 'X+YF', 'Y': 'FX-Y'}, 90),
        'plant': L_System(turtle, 'FX', {'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'}, 25),
        'sierpinsky': L_System(turtle, 'FA', {'FA': 'FB-FA-FB', 'FB': 'FA+FB+FA'}, 60),
        'koch':L_System(turtle,'F',{'F':'F+F-F-F+F'},90)
    }

    name,num = sys.argv[1], int(sys.argv[2])
    fractals[name].draw(num)

    turtle.screen.exitonclick()


