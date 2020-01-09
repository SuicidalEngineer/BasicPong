import turtle
import sys
from turtle import Turtle, Screen, Shape
from random import randint
import platform
if (platform.system() ==  "Windows"):
    import winsound

limit=int(input("Lütfen bir hedef skor giriniz"))


screen = Screen()
screen.setup(750, 500)
if (platform.system() ==  "Windows"):
    winsound.PlaySound('hello.wav', winsound.SND_FILENAME)
screen.tracer(0)

play_top    = screen.window_height() / 2 - 100
play_bottom = -screen.window_height() / 2 + 100
play_left   = -screen.window_width() / 2 + 50
play_right  = screen.window_width() / 2 - 50
area = Turtle()
area.hideturtle()
area.penup()
area.goto(play_right, play_top)
area.pendown()
area.goto(play_left, play_top)
area.goto(play_left, play_bottom)
area.goto(play_right, play_bottom)
area.goto(play_right, play_top)

L = Turtle()
R = Turtle()
L.penup()
R.penup()

paddle_w_half = 10 / 2
paddle_h_half = 40 / 2
paddle_shape = Shape("compound")
paddle_points = ((-paddle_h_half, -paddle_w_half),
                 (-paddle_h_half, paddle_w_half),
                 (paddle_h_half, paddle_w_half),
                 (paddle_h_half, -paddle_w_half))
paddle_shape.addcomponent(paddle_points, "black")
screen.register_shape("paddle", paddle_shape)
L.shape("paddle")
R.shape("paddle")

L.setx(play_left + 10)
R.setx(play_right - 10)
paddle_L_move_direction = 0
paddle_R_move_direction = 0
paddle_move_vert   = 4
def paddle_is_allowed_to_move_here (new_y_pos) :
    if (play_bottom > new_y_pos - paddle_h_half) :
        return False
    if (new_y_pos + paddle_h_half > play_top) :
        return False
    return True
def update_paddle_positions () :
    L_new_y_pos = L.ycor() + (paddle_L_move_direction * paddle_move_vert)
    R_new_y_pos = R.ycor() + (paddle_R_move_direction * paddle_move_vert)
    if paddle_is_allowed_to_move_here (L_new_y_pos):
        L.sety( L_new_y_pos )
    if paddle_is_allowed_to_move_here (R_new_y_pos):
        R.sety( R_new_y_pos )
def L_up() :
    global paddle_L_move_direction
    paddle_L_move_direction = 1.75
def L_down() :
    global paddle_L_move_direction
    paddle_L_move_direction = -1.75
def L_off() :
    global paddle_L_move_direction
    paddle_L_move_direction = 0
def R_up() :
    global paddle_R_move_direction
    paddle_R_move_direction = 1.75
def R_down() :
    global paddle_R_move_direction
    paddle_R_move_direction = -1.75
def R_off() :
    global paddle_R_move_direction
    paddle_R_move_direction = 0
screen.onkeypress(L_up, "w")
screen.onkeypress(L_down, "s")
screen.onkeypress(R_up, "Up")
screen.onkeypress(R_down, "Down")
screen.onkeyrelease(L_off, "w")
screen.onkeyrelease(L_off, "s")
screen.onkeyrelease(R_off, "Up")
screen.onkeyrelease(R_off, "Down")
screen.listen()

score_turtle = Turtle()
score_turtle.penup()
score_turtle.hideturtle()
score_L = 0
score_R = 0
def write_scores() :
    score_turtle.clear()
    score_turtle.goto(-screen.window_width()/4, screen.window_height()/2 - 80)
    score_turtle.write(score_L, align="center", font=("Arial", 32, "bold"))
    score_turtle.goto(screen.window_width()/4, screen.window_height()/2 - 80)
    score_turtle.write(score_R, align="center", font=("Arial", 32, "bold"))
    if score_L == limit or score_R == limit :
        if (platform.system() == "Windows"):
            winsound.PlaySound('win.wav', winsound.SND_FILENAME)
        print("Hadi yine iyisin, çorba parası çıktı")
        turtle.bye()
        sys.tracebacklimit = 0
def check_if_someone_scores() :
    global score_L, score_R
    if (ball.xcor() + ball_radius) >= play_right :   # right of ball at right of field
        score_L += 1
        if (platform.system() == "Windows"):
            winsound.PlaySound('goal.wav', winsound.SND_FILENAME)
        write_scores()
        reset_ball()
    elif play_left >= (ball.xcor() - ball_radius) :  # left of ball at left of field
        score_R += 1
        if (platform.system() == "Windows"):
            winsound.PlaySound('goal.wav', winsound.SND_FILENAME)
        write_scores()
        reset_ball()

ball = Turtle()
ball.penup()
ball.shape("circle")
ball.shapesize( 0.5, 0.5)
ball_radius = 10 * 0.5
ball_move_horiz = 12
ball_move_vert  = 8
def ball_collides_with_paddle (paddle) :
    x_distance = abs(paddle.xcor() - ball.xcor())
    y_distance = abs(paddle.ycor() - ball.ycor())
    overlap_horizontally = (ball_radius + paddle_w_half >= x_distance)
    overlap_vertically   = (ball_radius + paddle_h_half >= y_distance)
    return overlap_horizontally and overlap_vertically
def update_ball_position () :
    global ball_move_horiz, ball_move_vert
    if ball.ycor() + ball_radius >= play_top :
        ball_move_vert *= -1
    elif play_bottom >= ball.ycor() - ball_radius :
        ball_move_vert *= -1
    if ball_collides_with_paddle(R) or ball_collides_with_paddle(L) :
        if (platform.system() == "Windows"):
            winsound.PlaySound('hit.wav', winsound.SND_FILENAME)
        ball_move_horiz *= -1
    ball.setx(ball.xcor() + ball_move_horiz)
    ball.sety(ball.ycor() + ball_move_vert)

def reset_ball() :
    global ball_move_vert, ball_move_horiz
    ball.setpos(0, 0)
    speed_horiz = int (12)
    speed_vert = int (8)
    direction_horiz = 1
    direction_vert = 1
    if randint(0,100) > 50 :
        direction_horiz = -1
        direction_vert = -1
    ball_move_horiz = direction_horiz * speed_horiz
    ball_move_vert  = direction_vert * speed_vert

def frame () :
    check_if_someone_scores()
    update_paddle_positions()
    update_ball_position()
    screen.update()
    screen.ontimer(frame, framerate_ms)
write_scores()
framerate_ms = 50
frame()
turtle.mainloop()
