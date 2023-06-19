from tkinter import *
from tkinter import messagebox
from random import choice
import pandas
import os

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE = "Spanish"
SECONDS = 3

current_card = {}
words_to_learn = {}
card_front = True

try:
    words_df = pandas.read_csv("data\words_to_learn.csv")
except FileNotFoundError:
    words_df_org = pandas.read_csv(f"data\{LANGUAGE}_words.csv")
    words_to_learn = words_df_org.to_dict(orient="records")
else:
    words_to_learn = words_df.to_dict(orient="records")

def next_card():
    global current_card, flip_timer, card_front
    try:
        current_card = choice(words_to_learn)
    except IndexError:
        messagebox.showinfo(title="Congratulations!", \
            message="You have completed studying all cards!")
        if(os.path.isfile("data\words_to_learn.csv")):
            os.remove("data\words_to_learn.csv")
            print("\nEmpty 'words_to_learn.csv' file deleted\n")
        window.destroy()
    else:
        card_front = True
        flip_card(button_pressed = False)
        window.after_cancel(flip_timer)
        flip_timer = window.after(ms=SECONDS*1000, func=flip_to_back)

def flip_to_back():
    global card_front
    card_front = False
    flip_card(button_pressed = False)

def flip_card(button_pressed = True):
    global card_front
    if button_pressed:
        card_front = not card_front
        window.after_cancel(flip_timer)
    if card_front:
        canvas.itemconfig(card_title, text=LANGUAGE, fill="black")
        canvas.itemconfig(card_word, text=current_card[LANGUAGE], fill="black")
        canvas.itemconfig(card_background, image=img_card_front)
    else:
        canvas.itemconfig(card_title, text="English", fill="white")
        canvas.itemconfig(card_word, text = current_card["English"], fill="white")
        canvas.itemconfig(card_background, image=img_card_back)

def update_learned():
    words_to_learn.remove(current_card)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("data\words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
img_card_front = PhotoImage(file=r"images\card_front.png")
card_background = canvas.create_image(400, 263, image=img_card_front)
card_title = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

img_card_back = PhotoImage(file=r"images\card_back.png")

img_right = PhotoImage(file=r"images\right.png")
right_button = Button(image=img_right, highlightthickness=0, command=update_learned)
right_button.grid(row=1, column=1)

img_wrong = PhotoImage(file=r"images\wrong.png")
wrong_button = Button(image=img_wrong, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

flip_button = Button(text="Flip Card", font=("Arial", 14), \
    highlightthickness=0, command=flip_card, width=20)
flip_button.grid(row=2, column=0, columnspan=2)

flip_timer = window.after(ms=SECONDS*1000, func=flip_to_back)
next_card()
window.mainloop()