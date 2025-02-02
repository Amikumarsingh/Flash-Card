BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50,bg=BACKGROUND_COLOR)
current_card = {}
to_learn = {}
# ----------------------- extracting data---------------------------
try:
    data = pandas.read_csv(r"flash card/data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv(r"flash card/data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:    
    to_learn = data.to_dict(orient="records")

# ----------------------- functions ---------------------------
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background,image=card_front_image)
    flip_timer = window.after(3000,func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background,image=card_back_image)
    window.after(3000,func=flip_card)

def is_known():
    to_learn.remove(current_card)    
    data = pandas.DataFrame(to_learn)
    data.to_csv(r"flash card/data/words_to_learn.csv",index=False)
    
    next_card()

# ------------------------------------------------------------------
flip_timer=window.after(3000,func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file=r"flash card\images\card_front.png")
card_back_image= PhotoImage(file=r"flash card\images\card_back.png")
card_background=canvas.create_image(400, 263, image=card_back_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title=canvas.create_text(400,150,text="",font=("Arial",40,"italic"))
card_word=canvas.create_text(400,263,text="",font=("Arial",60,"bold"))
canvas.grid(row=0, column=0,columnspan=2)

#------------------------ buttons-------------------------------------
my_image1 = PhotoImage(file=r"flash card\images\right.png")
write_button = Button(image=my_image1,highlightthickness=0,bg=BACKGROUND_COLOR,command=next_card)
write_button.grid(row=1, column=1)

my_image3 = PhotoImage(file=r"flash card\images\wrong.png")
wrong_button = Button(image=my_image3,highlightthickness=0,bg=BACKGROUND_COLOR,command=is_known)
wrong_button.grid(row=1, column=0)

# --------------------------------------------------------------------

next_card()

window.mainloop()
