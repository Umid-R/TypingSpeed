from tkinter import *
import tkmacosx
import random
import time 
import math
from tkinter import messagebox


window=Tk()
window.title("Typing Speed")
window.minsize(1200,800)



# ----- Createst text for user from random words -----
def get_text():
    
    with open('basic_english_words.txt') as file:
        lines=file.readlines()
        output=''
        for word in random.choices(lines,k=60):
            output+=word.replace('\n',' ')
        return output


#----- Global Variables -----
text=get_text()
start_time=0
end_time=0
mistakes=0
corrects=0
characters=0
wpm=0
accuracy=0
running=False

with open('highest_score.txt') as file:
            temp=int(file.read())
highest=temp


def main():
    
    #Destroy other widgets
    for widget in window.winfo_children():
        widget.destroy()
    #----- Main functions -----

    # Highlights the letters whether correct or wrong
    def highlight_letters(event=None):
        global characters, mistakes, start_time, corrects, running, end_time
        
        typed = entry_area.get("1.0", END).strip().rstrip('\n')
        # start timer on first key typed
        if start_time == 0 and len(typed) > 0:
            start_time = time.time()
            running = True
            calculate_results()

        characters = len(typed)
        text_label.config(state=NORMAL)  # enable editing to change tags
        text_label.tag_remove("correct", "1.0", END)  # remove old tags
        text_label.tag_remove("wrong", "1.0", END)

        mistakes = 0
        corrects = 0
        
        for i, char in enumerate(text):
            if i < len(typed):
                if typed[i] == char:
                    text_label.tag_add("correct", f"1.0+{i}c", f"1.0+{i+1}c")
                    corrects += 1
                else:
                    text_label.tag_add("wrong", f"1.0+{i}c", f"1.0+{i+1}c")
                    mistakes += 1
            
        # check is the text is over
        if len(typed)>=(len(text.strip())):
            
            end_time=time.time()
            # Update the highest score if user hits the record
            if wpm>highest:
                with open('highest_score.txt','w') as file:
                    file.write(str(wpm))
                highest_label.config(text=f"Highest Score:{wpm}")
            result=messagebox.showinfo('Your Score',message=f'Time:{math.floor(end_time-start_time)}\nWPM:{wpm}\nAccuracy:{accuracy}')
            if result=='ok':
                restart()
                return
    

        text_label.config(state=DISABLED)  # prevent editing again

        

    # WPM and Accuracy
    def calculate_results(event=None):
        global wpm, accuracy, end_time, running
        if not running:
            return # if not running, stop updating
        # track the current time while the user typing
        end_time=time.time()
        
        # Net WPM = (Total characters typed / 5 - Mistakes) / Minutes
        if end_time-start_time > 0:
            wpm = math.floor((characters/5 - mistakes) / ((end_time-start_time)/60))
            wpm=max(0,wpm)
        else:
            wpm = 0
        wpm_label.config(text=f'WPM:{wpm}')
        time_label.config(text=f'Time:{math.floor(end_time-start_time)}')
    
        
        # Acuracy=(Total correct chars/ all chars)*100
        if characters > 0:
            accuracy = math.floor((corrects/characters) * 100)
        else:
            accuracy = 0

        accuracy_label.config(text=f'Accuracy:{accuracy}%')
        window.after(1000,calculate_results)
        

    def restart():
        global  text, start_time, end_time, mistakes, corrects, characters, wpm, accuracy, running
        text=get_text()
        start_time=0
        end_time=0
        mistakes=0
        corrects=0
        characters=0
        wpm=0
        accuracy=0
        running = False
        # Reset text area
        text_label.config(state=NORMAL)
        text_label.delete("1.0", END)
        text_label.insert(END, text)
        text_label.config(state=DISABLED)

        # Reset entry area
        entry_area.delete("1.0", END)

        # Reset labels
        wpm_label.config(text=f"WPM:{wpm}")
        accuracy_label.config(text=f"Accuracy:{accuracy}%")
        time_label.config(text=f"Time:{start_time}")

        # Focus on entry
        window.after(100, entry_area.focus_set)
        
    
    #----- Main Page -----

    window.config(bg='#FFC107')
    # User Typing Infos
    time_label=Label(text=f'Time:{end_time-start_time}',font=('Arial',14),bg='#FFC107')
    wpm_label=Label(text=f'WPM:{wpm}',font=('Arial',14),bg='#FFC107')
    accuracy_label=Label(text=f'Accuracy:{accuracy}',font=('Arial',14),bg='#FFC107')
    highest_label=Label(text=f'Highest Score:{highest}',font=('Arial',14),bg='#FFC107')

    time_label.grid(row=0 ,column=0, padx=100, pady=30)
    wpm_label.grid(row=0, column=1,padx=100)
    accuracy_label.grid(row=0, column=2,padx=100)
    highest_label.grid(row=0, column=3,padx=100)


    # Text for  user
    text_label=Text( font=('Arial',18),bg="#FFFFFF",height=7,wrap='word',width=70)
    text_label.insert(END,text)

    # Define color tags
    text_label.tag_configure("correct", foreground="green")
    text_label.tag_configure("wrong", foreground="red")


    text_label.config(state=DISABLED)
    text_label.grid(row=1, column=0, columnspan=4, padx=20, pady=(50,0))


    # Input Area for the user

    entry_area=Text(bg='#FF6F3C', width=50,height=5,font=('Arial',20), borderwidth=0,highlightthickness=0, wrap='word')
    entry_area.grid(row=2, column=0 ,columnspan=4, pady=20)
    entry_area.bind("<KeyRelease>", highlight_letters,add="+")
    window.after(100, entry_area.focus_set)



    
    # Restart Button 

    restart_button=tkmacosx.Button(text='Restart', font=('Arial',20,'bold'), bg='#347433', borderless=1, fg="#FFFFFF",width=200, height=60,command=restart)
    restart_button.grid(row=3, column=1, sticky='w', pady=20)



    

#----- Home Page -----
def home():
    home_label=Label(text='Welcome To The Typing Speed App!', font=('Arial',20, 'bold'),bg='#347433', fg="#FFFFFF")
    home_button=tkmacosx.Button(text='Start', width=140,height=50,font=('Arial',14, 'bold'), bg='#FFC107', borderless=1, fg="#FFFFFF",command=main)
    window.config(bg='#347433')
    home_label.grid(column=0, row=0, pady=(300,20), padx=350)
    home_button.grid(column=0, row=1)
    

   


home()
window.mainloop()