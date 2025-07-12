import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    curses.echo()  # Allow typed characters to be shown on screen
    stdscr.clear()
    stdscr.addstr("Welcome to the SPEED TYPiNG TEST!\n")
    stdscr.addstr("Enter ur name pls:")
    stdscr.refresh()
    name = stdscr.getstr().decode("utf-8")  # Read input and decode from bytes to string
    stdscr.addstr("\nhello "+ name +" press any key to start the game") 
    stdscr.getkey()  # Wait for user to press a key
    return name

def load_text():
    with open("C:/Users/Suhas Sreenath/Desktop/PYTHON PROJETCS/wpm test/text.txt", "r") as file:

        lines = file.readlines()
        target= random.choice(lines).strip()  # Randomly select a line from the file
    return target

def previous_plays(name,wpm):
    with open("C:/Users/Suhas Sreenath/Desktop/PYTHON PROJETCS/wpm test/previousplay.txt",'a') as f:
            f.write(name + ":"+str(wpm)+'\n')  # Append the name to the file

def display_text(stdscr, target,current,wpm=0):
    stdscr.clear() 
    stdscr.addstr(target)
    stdscr.addstr(1,0,f"WPM: {wpm}")
        
    for i,char in enumerate(current):
        current_text=target[i]
        color=curses.color_pair(1)
        if char!= current_text:
            color=curses.color_pair(2)
        stdscr.addstr(0,i,char,color)

def wpm_test(stdscr):
    Target_text=load_text()  # Load the target text from the file
    Current_text=[]
    wpm=0

    stdscr.clear() 
    stdscr.addstr(Target_text)
    stdscr.refresh()
    start_time = time.time()

    while True:
        elapsed_time = max(time.time() - start_time,1) # Avoid division by zero
        wpm=round((len(Current_text)/(elapsed_time/60))/5)  # Calculate WPM (words per minute) by taking avg word to be 5 characters long
        stdscr.nodelay(True)
        stdscr.clear() 
        display_text(stdscr, Target_text, Current_text,wpm)
        stdscr.refresh()

        if "".join(Current_text)== Target_text:
            stdscr.nodelay(False)
            break

        try:
            key= stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # Escape key to exit
            break
        if key in ("Key_Backspace", "Key_Delete",'\b', '\x7f'):
            if len(Current_text)>0:
                Current_text.pop()
        elif len(Current_text) < len(Target_text):
            Current_text.append(key)
    return wpm



    
    

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) #COLOUR INITIALIZATION#
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)

    while True:
        name=start_screen(stdscr)
        wpm=wpm_test(stdscr)
        previous_plays(name,wpm)
        stdscr.addstr(2, 0, "Test completed! Press esc to exit or any other key to play again or wanna see ur previous plays press P.")
        key=stdscr.getkey()  # Wait for user to press a key before exiting
        if ord(key) == 27:
            break
        elif ord(key)== 80:
            stdscr.clear()
            stdscr.addstr("Previous Players:\n")
            with open("C:/Users/Suhas Sreenath/Desktop/PYTHON PROJETCS/wpm test/previousplay.txt", 'r') as f:
                plays = f.readlines()
                for play in plays:
                    stdscr.addstr(play) 

            stdscr.addstr("\nPress any key to return to the main menu.")
            stdscr.getkey()


wrapper(main)  



