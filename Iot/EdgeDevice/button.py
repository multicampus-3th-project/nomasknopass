from gpiozero import Button
button = Button(21)
state = 1
def changestate():
    global state
    print("state changed!")
    if state == 1:
        state = 0
    else :
        state = 1
    print("state is ",state)


while True:
    button.when_pressed = changestate