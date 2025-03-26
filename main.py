from turtle import *

##### FUNCTIONS AND CLASS DEFINITIONS ############
class Block(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.speed(0)
        self.shape('square')
        self.color('yellow')
        self.penup()
        self.goto(x, y)

    def delete(self, blocks):
        self.hideturtle()
        self.clear()
        if self in blocks:
            blocks.remove(self)
        self.goto(1000, 1000)
        self.clear()
        screen.tracer(0)

    def strike(self, blocks):
        if self.color()[0] == 'yellow':
            self.color('orange')
        elif self.color()[0] == 'orange':
            self.color('red')
        elif self.color()[0] == 'red':
            self.delete(blocks)

class Player(Turtle):
    def __init__(self, x, y, score, rounds, left, right, fire, col):
        super().__init__()
        self.speed(0)
        self.shape('turtle')
        self.color(col)
        self.penup()
        self.goto(x, y)

        self.keys = [left, right, fire]
        self.score = score
        self.rounds = rounds
        self.bullets = []

    def turn_right(self):
        self.right(5)

    def turn_left(self):
        self.left(5)
         
    def fire(self):
        if len(self.bullets) < 5:
            screen.tracer(0)
            bullet = Bullet(self)
            self.bullets.append(bullet)
        else:
            print('Too many bullets')

class Bullet(Turtle):
    def __init__(self, player):
        super().__init__()
        screen.tracer(0)
        self.player = player
        self.speed(0)
        self.shapesize(.5,.5)
        self.shape('triangle')
        self.color(player.color()[0])
        self.penup()
        self.setheading(player.heading())
        self.goto(player.xcor(), player.ycor())
        self.veloc = 10
        screen.update()
        screen.tracer(1)
    
    def delete(self):
        self.hideturtle()
        self.clear()
        if self in self.player.bullets:
            self.player.bullets.remove(self)
        screen.tracer(0)
        self.clear()
        screen.update()
    def move(self):
        if self.xcor() > 110 or self.xcor() < -110:
            self.setheading(180-self.heading())
        if self.ycor() < -200 or self.ycor() > 200:
            self.delete()
        self.forward(self.veloc)

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.scores = {players[0]: 0, players[1]: 0}
        self.goto(0, 250)
        self.clear_score()

    def increase_score(self, player, points):
        if player in self.scores:
            self.scores[player] += points
        self.clear_score()

    def clear_score(self):
        self.clear()
        self.write(f"Player 1: {self.scores[players[0]]}  |  Player 2: {self.scores[players[1]]}", 
                   align="center", font=("Arial", 16, "bold"))

def key_down(key):
    keys_pressed[key] = True

def key_up(key):
    keys_pressed[key] = False

def upd():
    screen.tracer(0)
    if keys_pressed.get("a", False):
        players[0].turn_left()
    if keys_pressed.get("d", False):
        players[0].turn_right()
    if keys_pressed.get("j", False):
        players[1].turn_left()
    if keys_pressed.get("l", False):
        players[1].turn_right()

    for player in players:
        for bullet in player.bullets[:]:
            bullet.move()
            for block in blocks[:]:
                if bullet.distance(block) < 15:
                    block.strike(blocks)
                    score_display.increase_score(player, 10)
                    bullet.delete()
                    break

    screen.update()
    screen.tracer(1)
    screen.ontimer(upd, 16)

def draw_border():
    p = Turtle()
    p.speed(0)
    p.ht()
    p.pu()
    p.width(10)
    p.color("grey")
    p.goto(-110, 200)
    p.pendown()
    p.begin_fill()
    for _ in range(2):
        p.forward(220)
        p.right(90)
        p.forward(400)
        p.right(90)
    p.end_fill()

####### PROGRAM #############
screen = Screen()
screen.title("Shooting Gallery")
screen.bgcolor("black")
screen.tracer(0)

draw_border()
keys_pressed = {}

players = [Player(-50, -180, 0, 0, 'a', 'd', 'w','blue'),
           Player(50, -180, 0, 0, 'j', 'l', 'i','green')]

blocks = [Block(x, y) for y in (190, 170, 150) for x in range(100, -120, -20)]
score_display = Score()
for p in players:
    for i in p.keys:
        keys_pressed[i] = False

screen.listen()
for i in keys_pressed.keys():
    screen.onkeypress(lambda key=i: key_down(key), i)
    screen.onkeyrelease(lambda key=i: key_up(key), i)
screen.onkeypress(lambda: players[0].fire(),players[0].keys[2])
screen.onkeypress(lambda: players[1].fire(),players[1].keys[2])
screen.update()
screen.tracer(1)
upd()
screen.mainloop()
