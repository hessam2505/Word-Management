from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, messagebox
import json
import os
import vlc  
import os
from nltk.corpus import wordnet as wn
from googletrans import Translator
import time
from tkinter import scrolledtext
from nltk.corpus import wordnet as wn
# 
FILENAME = "vocabulary.json"



def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_word():
    word = wordValue.get().strip()
    meaning = meenValue.get().strip()
    synonyms = synonymValue.get().strip()
    antonyms = AntonymValue.get().strip()
    part1 = Part1.get().strip()
    part2 = Part2.get().strip()

    if not word:
        return  

    data[word] = {
        "meaning": meaning,
        "synonyms": synonyms,
        "antonyms": antonyms,
        "part1": part1,
        "part2": part2
    }
    save_data(data)
    update_treeview()
    clear_entries()

def delete_word():
    selected_item = wordtable.selection()
    if not selected_item:
        return  

    item_id = selected_item[0]
    word = wordtable.item(item_id, 'values')[0]
    if word in data:
        del data[word]
        save_data(data)
        update_treeview()
    else:
        return  


def load_word_details(event):
    selected_item = wordtable.selection()
    if not selected_item:
        return

    item_id = selected_item[0]
    word = wordtable.item(item_id, 'values')[0]

    if word in data:
        details = data[word]
        wordValue.set(word)
        meenValue.set(details.get('meaning', ''))
        synonymValue.set(details.get('synonyms', ''))
        AntonymValue.set(details.get('antonyms', ''))
        Part1.set(details.get('part1', ''))
        Part2.set(details.get('part2', ''))

# 
def update_word_details():
    selected_item = wordtable.selection()
    if not selected_item:
        return  # 

    item_id = selected_item[0]
    word = wordValue.get().strip()
    meaning = meenValue.get().strip()
    synonyms = synonymValue.get().strip()
    antonyms = AntonymValue.get().strip()
    part1 = Part1.get().strip()
    part2 = Part2.get().strip()

    if word in data:
        data[word] = {
            "meaning": meaning,
            "synonyms": synonyms,
            "antonyms": antonyms,
            "part1": part1,
            "part2": part2
        }
        save_data(data)
        update_treeview()
        clear_entries()

# 
def update_treeview():
    for item in wordtable.get_children():
        wordtable.delete(item)

    for word, details in data.items():
        wordtable.insert('', 'end', values=(
            word,
            details.get('meaning', ''),
            details.get('synonyms', ''),
            details.get('antonyms', ''),
            details.get('part1', ''),
            details.get('part2', '')
        ))

def clear_entries():
    wordValue.set('')
    meenValue.set('')
    synonymValue.set('')
    AntonymValue.set('')
    Part1.set('')
    Part2.set('')

# جستجو کلمات
def search_words():
    search_term = sentry.get().lower()
    filtered_data = {word: details for word, details in data.items() if search_term in word.lower()}
    update_treeview_with_filter(filtered_data)

def update_treeview_with_filter(filtered_data):
    for item in wordtable.get_children():
        wordtable.delete(item)

    for word, details in filtered_data.items():
        wordtable.insert('', 'end', values=(
            word,
            details.get('meaning', ''),
            details.get('synonyms', ''),
            details.get('antonyms', ''),
            details.get('part1', ''),
            details.get('part2', '')
        ))

# 
win = Tk()
win.geometry('1950x700+0+0')
win.title('Words Management')
win.config(bg='#4ac79d',relief=GROOVE,bd=10)
win.resizable(False, False)

f7=Frame(win,bg='#13ad7a',width=550,height=600,bd=10,relief=GROOVE)
f7.place(x=1360,y=70)
fp=Frame(win,bg='#13ad7a',width=1931,height=62,bd=10,relief=GROOVE)
fp.place(x=0,y=0)
lfp=Label(fp,text='Word Management : ',fg='yellow',bg='#13ad7a',font='arial 20 bold')
lfp.place(x=850,y=2)
lfp2=Label(fp,text='H.A',fg='yellow',bg='#13ad7a',font='arial 9')
lfp2.place(x=1,y=2)


#dic#################################################################################################################################
translations = {
    "noun": "اسم",
    "verb": "فعل",
    "adjective": "صفت",
    "adverb": "قید"
}

# د
meanings_translations = {
    "A person, place, thing, or idea": "شخص، مکان، چیز یا ایده",
    "An action or state": "عمل یا حالت",
    "Describing a noun": "توصیف یک اسم",
    "Describing how, when, or where": "توصیف چگونگی، زمان یا مکان",
    "A quality or characteristic": "یک ویژگی یا خاصیت",
    "A process of doing something": "فرایند انجام دادن چیزی",
    "A group of people": "یک گروه از مردم",
    "An effect or influence": "اثر یا تأثیر",
}

def translate_pos(pos):
    return translations.get(pos, pos)

def translate_meaning(meaning):
    return meanings_translations.get(meaning, "No translation available.")

def search_word():
    word = entry.get().strip()
    
    if not word:
        result_text.delete(1.0, END)
        result_text.insert(END, "Please enter a word")
        return
    
    synsets = wn.synsets(word)
    
    if not synsets:
        result_text.delete(1.0, END)
        result_text.insert(END, "The word was not found in the dictionary !")
        return

    details = f"Word: {word}\n"
    
    for idx, synset in enumerate(synsets, 1):
        meaning = synset.definition()
        translated_meaning = translate_meaning(meaning)
        
        details += f"\nmeaning{idx} (english): {meaning}\n"
        details += f"part of speech: {translate_pos(synset.pos())}\n"
        
        synonyms = {lemma.name() for lemma in synset.lemmas()}
        details += f"synonyms: {', '.join(synonyms)}\n"
        
        antonyms = {lemma.antonyms()[0].name() for lemma in synset.lemmas() if lemma.antonyms()}
        details += f"antonyms: {', '.join(antonyms) if antonyms else 'none'}\n"
        
        examples = synset.examples()
        details += f"examples: {', '.join(examples[:2]) if examples else 'none'}\n"

    result_text.delete(1.0, END)
    result_text.insert(END, details)

# ر

title_label = Label(win, text="Dictionary Search", font=("Helvetica", 18), bg="#13ad7a", fg="yellow")
title_label.place(x=1530,y=90)

entry = Entry(win, width=40, font=("Helvetica", 14), justify='center')
entry.insert(0, "")
entry.place(x=1410,y=150)

search_button = Button(win, text="Search", font=("Helvetica", 14), command=search_word, bg="green", fg="white")
search_button.place(x=1590,y=220)

result_text = scrolledtext.ScrolledText(win, wrap=WORD, width=50, height=18, font=("Helvetica", 12))
result_text.place(x=1400,y=310)
# ف
#l1 = Label(win, text='Words Management:', bg='#13ad7a', fg='yellow', font='NPIMina 30', bd=5, relief=RAISED)
#l1.pack(side=TOP, fill=X)

f1 = LabelFrame(win, text='Enter Details', font='arial 8', bd=10, bg='#13ad7a', fg='yellow', relief=GROOVE)
f1.place(x=20, y=70, width=420, height=600)

f2 = Frame(win, bd=10, bg='#13ad7a', relief=GROOVE)
f2.place(x=500, y=70, width=810, height=600)

f4 = Frame(win, bd=10, bg='#13ad7a', relief=GROOVE)
f4.place(x=40, y=500, width=380, height=120)

# دکمه‌ها در فریم f4
uB = Button(f4, text='Update', bg='#0dffaf', font='arial 15', bd=5, width=15, relief=RAISED, command=update_word_details)
uB.place(x=175, y=4)

ab = Button(f4, text='Add', bg='#0dffaf', font='arial 15', bd=5, width=15, relief=RAISED, command=add_word)
ab.place(x=175, y=50)

db = Button(f4, text='Delete', bg='#0dffaf', font='arial 15', bd=5, width=15, relief=RAISED, command=delete_word)
db.place(x=4, y=50)

cb = Button(f4, text='Clear', bg='#0dffaf', font='arial 15', bd=5, width=15, command=clear_entries, relief=RAISED)
cb.place(x=4, y=4)

# مقادیر ورودی
wordValue = StringVar()
meenValue = StringVar()
AntonymValue = StringVar()
synonymValue = StringVar()
Part1 = StringVar()
Part2 = StringVar()
#cl
def update_clock():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=current_time)  
    clock_label.after(1000, update_clock)  



clock_label =Label(fp, font=('arial', 10), bg='#13ad7a', fg='yellow')
clock_label.place(x=0,y=20)

update_clock()
# ورودی‌ها و برچسب‌ها
wordL = Label(f1, text='Word:', bg='#13ad7a', fg='black', font='arial 14')
wordL.place(x=50, y=50)
wordE = Entry(f1, bd=7, font='arial 15', relief=SUNKEN, textvariable=wordValue)
wordE.place(x=140, y=50)

MeenL = Label(f1, text='Meaning:', bg='#13ad7a', fg='black', font='arial 14')
MeenL.place(x=50, y=120)
MeenE = Entry(f1, bd=7, font='arial 15', relief=SUNKEN, textvariable=meenValue)
MeenE.place(x=140, y=120)

SynonymL = Label(f1, text='Synonym:', bg='#13ad7a', fg='black', font='arial 14')
SynonymL.place(x=35, y=190)
SynonymE = Entry(f1, bd=7, font='arial 15', relief=SUNKEN, textvariable=synonymValue)
SynonymE.place(x=140, y=190)

AntonymL = Label(f1, text='Antonym:', bg='#13ad7a', fg='black', font='arial 14')
AntonymL.place(x=35, y=260)
AntonymE = Entry(f1, bd=7, font='arial 15', relief=SUNKEN, textvariable=AntonymValue)
AntonymE.place(x=140, y=260)

# Combobox‌ها
wordL = Label(win, text='Part Of Speech:', bg='#13ad7a', fg='black', font='arial 14')
wordL.place(x=40, y=420)
c1 = ttk.Combobox(win, font='arial 11', values=['Noun', 'Adjective', 'Verb', 'Pronoun', 'Adverb', 'Preposition', 'Conjunction', 'Interjection'], width=15, textvariable=Part1)
c1.place(x=180, y=425, width=100)

c2 = ttk.Combobox(win, font='arial 11', values=['Noun', 'Adjective', 'Verb', 'Pronoun', 'Adverb', 'Preposition', 'Conjunction', 'Interjection'], width=15, textvariable=Part2)
c2.place(x=305, y=425, width=100)

# جستجو
sf4 = Frame(win, bg='#0dffaf', bd=10, width=790, height=55, relief=GROOVE)
sf4.place(x=510, y=80)

Shb = Button(win, text='Search', bg='#4ac79d', width=10, font='arial 10', bd=5, relief=RAISED, command=search_words)
Shb.place(x=1190, y=89)
sentry = Entry(win, width=105)
sentry.place(x=540, y=93, height=26)

# Treeview و اسکرول بار
Yscroll = ttk.Scrollbar(win, orient=VERTICAL)
Xscroll = ttk.Scrollbar(win, orient=HORIZONTAL)

wordtable = ttk.Treeview(win, columns=('Word', 'Meaning', 'Synonym', 'Antonym', 'Part Of Speech_1', 'Part Of Speech_2'),
                        yscrollcommand=Yscroll.set, xscrollcommand=Xscroll.set)

wordtable.place(x=520, y=140, width=770, height=500)

Yscroll.config(command=wordtable.yview)
Xscroll.config(command=wordtable.xview)

Yscroll.place(x=1291, y=140, height=500)
Xscroll.place(x=520, y=640, width=770)

wordtable.heading('Word', text='Word')
wordtable.heading('Meaning', text='Meaning')
wordtable.heading('Synonym', text='Synonym')
wordtable.heading('Antonym', text='Antonym')
wordtable.heading('Part Of Speech_1', text='Part Of Speech 1')
wordtable.heading('Part Of Speech_2', text='Part Of Speech 2')
wordtable['show'] = 'headings'
wordtable.column('Word', width=150)
wordtable.column('Meaning', width=150)
wordtable.column('Synonym', width=150)
wordtable.column('Antonym', width=150)
wordtable.column('Part Of Speech_1', width=150)
wordtable.column('Part Of Speech_2', width=150)

# بارگذاری داده‌ها و به‌روزرسانی Treeview
data = load_data()
update_treeview()

# اتصال رویداد کلیک روی Treeview
wordtable.bind('<ButtonRelease-1>', load_word_details)

win.mainloop()
