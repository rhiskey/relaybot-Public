from tkinter import *
from tkinter import messagebox


def show_message():
    messagebox.showinfo("GUI Python", message.get())


clicks = 0


def click_button():
    global clicks
    clicks += 1
    message_button.config(text="Clicks {}".format(clicks))


root = Tk()
root.title("GUI на Python")
root.geometry("300x250")

# TextBox
message = StringVar()

message_entry = Entry(textvariable=message)
message_entry.place(relx=.5, rely=.6, anchor="c")

# Button
message_button = Button(text="Click Me", command=show_message)
message_button.place(relx=.5, rely=.1, anchor="c")
# btn = Button(text="Clicks 0", background="#555", foreground="#ccc",
#              padx="20", pady="8", font="16", command=click_button)
# btn.pack()

# Label
poetry = "Вот мысль, которой весь я предан,\nИтог всего, что ум скопил.\nЛишь тот, кем бой за жизнь изведан," \
         "\nЖизнь и свободу заслужил. "
label2 = Label(text=poetry, justify=LEFT)
label2.place(relx=.2, rely=.3)

# Checkbox
insta = IntVar()
insta_checkbutton = Checkbutton(text="Instagram", variable=insta,
                                onvalue=1, offvalue=0, padx=15, pady=10)
insta_checkbutton.grid(row=0, column=0, sticky=W)

discord = IntVar()
discord_checkbutton = Checkbutton(text="Discord", variable=discord,
                                  onvalue=1, offvalue=0, padx=15, pady=10)
discord_checkbutton.grid(row=1, column=0, sticky=W)

# Main Menu
main_menu = Menu()

file_menu = Menu()
file_menu.add_command(label="New")
file_menu.add_command(label="Save")
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Exit")

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Edit")
main_menu.add_cascade(label="View")

root.config(menu=main_menu)

# ListBox
languages = ["Python", "JavaScript", "C#", "Java", "C/C++", "Swift",]
#              "PHP", "Visual Basic.NET", "F#", "Ruby", "Rust", "R", "Go",
#              "T-SQL", "PL-SQL", "Typescript"]
# #scrollbar = Scrollbar(root)
# #scrollbar.pack(side=RIGHT, fill=Y)
#
# languages_listbox = Listbox(yscrollcommand=scrollbar.set, width=40)
#
# for language in languages:
#     languages_listbox.insert(END, language)
#
# languages_listbox.pack(side=LEFT)
# #scrollbar.config(command=languages_listbox.yview)



# languages_listbox = Listbox()
#
# for language in languages:
#     languages_listbox.insert(END, language)
#
# languages_listbox.pack()

root.mainloop()
