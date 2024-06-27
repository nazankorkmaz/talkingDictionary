import tkinter as tk
from PIL import Image, ImageTk
import json
from difflib import get_close_matches
from tkinter import messagebox
import pyttsx3
from googletrans import Translator


translator = Translator()

engine = pyttsx3.init()
voices = engine.getProperty('voices') #Sesleri Alma
engine.setProperty('voice',voices[0].id)


def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = bg_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_container, image=photo)
    canvas.photo = photo # Güncellenen resmi kaydedin


def arama():
    data = json.load(open('data.json'))
    kelime= kelimeEntry.get()
    kelime = kelime.lower()
    anlamText.delete("1.0", tk.END) #temizle
    if kelime in data :
        anlamText.config(state='normal')
        anlam = data[kelime]
        print(kelime)
        for item in anlam:
            anlamText.insert(tk.END, u'\u2022'+item+"\n\n") # basina nokta koy

    #en yakin tahminlerden vermesi
    elif len(get_close_matches(kelime,data.keys()))>0:  #difflib.get_close_matches(word, possibilities, n=3, cutoff=0.6)
        close_match = get_close_matches(kelime,data.keys())[0]  # bi tanesini versin
        print(close_match)
        cevap = messagebox.askyesno("Onayla","Bunu mu demek istediniz:\n"+close_match)

        if cevap :
            anlamText.delete("1.0", tk.END)  # temizle
            kelimeEntry.delete(0,tk.END)
            kelimeEntry.insert(tk.END,close_match)
            anlam = data[close_match]
            for item in anlam :
                anlamText.insert(tk.END, u'\u2022' + item + "\n\n")
        else:
            messagebox.showerror("Hata", "Kelime bulunamadı. Lütfen tekrar kontrol ediniz!")
            kelimeEntry.delete(0, tk.END)
            anlamText.delete("1.0", tk.END)  # temizle
    else:
        messagebox.showinfo("Bilgi","Kelime bulunmuyor")
        kelimeEntry.delete(0, tk.END)
        anlamText.delete("1.0", tk.END)  # temizle
    anlamText.config(state='disabled')


def sesVer_kelime():
    engine.say(kelimeEntry.get())
    engine.runAndWait()

def sesVer_anlam():
    engine.say(anlamText.get(1.0,tk.END))
    engine.runAndWait()

def temizle():
    anlamText.config(state='normal')
    kelimeEntry.delete(0, tk.END)
    anlamText.delete("1.0", tk.END)
    anlamText.config(state='disabled')

def temizle2():
    anlamEntry2.config(state='normal')
    kelimeEntry2.delete(0, tk.END)
    anlamEntry2.delete("1.0", tk.END)
    anlamEntry2.config(state='disabled')

def cikis():
    cevap = messagebox.askyesno("Onayla","Çıkmak mı istiyorsunuz?")
    if cevap:
        app.destroy()
    else:
        pass

# Tkinter uygulamasını başlat
app = tk.Tk()
app.geometry("1500x750+10+20")
app.title("Çeviri Uygulamam")
app.resizable(True,True)

# Tkinter penceresine ikonu
icon2 = Image.open("photo/icon_dictionary.png")
icon2 = ImageTk.PhotoImage(icon2)

####################################################

bg_image_path = "photo/bg.jpg"
bg_image = Image.open(bg_image_path)
bg_photo = ImageTk.PhotoImage(bg_image)

# Canvas widget'ını oluşturun ve pencereye yerleştirin
canvas = tk.Canvas(app)
canvas.pack(fill="both", expand=True)

# Resmi Canvas'a yerleştirin
image_container = canvas.create_image(20, 20, anchor="nw", image=bg_photo)
#####################################

frame1 = tk.Frame(app, background="whitesmoke",bd=5, relief="ridge")
frame1.place(relx=0.7, rely=0.45, anchor='center',relwidth=0.4,relheight=0.8)


kelimeLabel = tk.Label(frame1,text="   Kelime Girin   ",font=('castellar','29','bold'),fg="skyblue3", bg="snow3")
kelimeLabel.pack(pady=15)

kelimeEntry = tk.Entry(frame1,font=('arial',22), justify="center",bd=8,relief="ridge")
kelimeEntry.pack()

####################################

frame_icon1 = tk.Frame(frame1, background="whitesmoke",bd=5, relief="ridge")
frame_icon1.pack(pady=10)

icon_arama = "photo/icon_search.png"
iconSearch = Image.open(icon_arama)
iconSearch = iconSearch.resize((35, 35))
icon_image_ara = ImageTk.PhotoImage(iconSearch)
aramaButon = tk.Button(frame_icon1,image=icon_image_ara, bd=0, cursor="hand2",command=arama)
aramaButon.pack(side="left", padx=10, pady=5)

####################################

icon_mik = "photo/icon_microphone.png"
iconMic = Image.open(icon_mik)
iconMic = iconMic.resize((35, 35))
icon_image_mic = ImageTk.PhotoImage(iconMic)
microfonButon = tk.Button(frame_icon1,image=icon_image_mic, bd=0, cursor="hand2",command=sesVer_kelime)
microfonButon.pack(side="left", padx=10, pady=5)


#####################################

anlamLabel = tk.Label(frame1,text="   Anlam   ",font=('castellar','29','bold'),fg="skyblue3", bg="snow3")
anlamLabel.pack(pady=10)

anlamText = tk.Text(frame1,font=('arial',18), bd = 8,height=8, width=28, background="whitesmoke", relief="ridge", state='disabled')
anlamText.pack()

####################################
frame_icon2 = tk.Frame(frame1, background="whitesmoke",bd=5, relief="ridge")
frame_icon2.pack(pady=10)

iconMic2 = Image.open(icon_mik)
iconMic2 = iconMic2.resize((35, 35))
icon_image_mic2 = ImageTk.PhotoImage(iconMic2)
microfonButon2 = tk.Button(frame_icon2,image=icon_image_mic2, bd=0, cursor="hand2",command=sesVer_anlam)
microfonButon2.pack(side="left", padx=10, pady=5)

####################################

icon_clear = "photo/icon_clear.png"
iconClear = Image.open(icon_clear)
iconClear = iconClear.resize((35, 35))
icon_image_clear = ImageTk.PhotoImage(iconClear)
clearButon = tk.Button(frame_icon2,image=icon_image_clear, bd=0, cursor="hand2",command=temizle)
clearButon.pack(side="left", padx=10, pady=5)


###################################


def arama_sozluk():
    anlamEntry2.delete(0, tk.END)
    # Türkçeden İngilizceye çeviri
    result = translator.translate(kelimeEntry2.get(), src='en', dest='tr')
    print(result.text)
    anlamEntry2.insert(tk.END,result.text)

def arama_sozluk_tr():
    anlamEntry2.delete(0, tk.END)
    # Türkçeden İngilizceye çeviri
    result = translator.translate(kelimeEntry2.get(), src='tr', dest='en')
    print(result.text)
    anlamEntry2.insert(tk.END,result.text)

def sesVer_sozluk():
    engine.say(kelimeEntry2.get())
    engine.runAndWait()

# Bir Frame oluştur ve ana pencereye yerleştir
frame = tk.Frame(app, background="whitesmoke",bd=5, relief="ridge")
frame.place(relx=0.2, rely=0.4, anchor='center',relwidth=0.3,relheight=0.6)

kelimeLabel2 = tk.Label(frame,text="   Çeviri   ",font=('castellar','20','bold'),fg="skyblue3", bg="snow3")
kelimeLabel2.pack(pady=15)

kelimeEntry2 = tk.Entry(frame,font=('arial',20), justify="center",bd=8,relief="ridge")
kelimeEntry2.pack()

####################################
frame_icon3 = tk.Frame(frame, background="whitesmoke",bd=5, relief="ridge")
frame_icon3.pack(pady=10)

iconMic3 = Image.open(icon_mik)
iconMic3 = iconMic3.resize((35, 35))
icon_image_mic3 = ImageTk.PhotoImage(iconMic3)
microfonButon22 = tk.Button(frame_icon3,image=icon_image_mic3, bd=0, cursor="hand2",command=sesVer_sozluk)
microfonButon22.pack(side="left", padx=10, pady=5)

iconSearch2 = Image.open("photo/tr-en.png")
iconSearch2 = iconSearch2.resize((60, 20))
icon_image_ara2 = ImageTk.PhotoImage(iconSearch2)
aramaButon22 = tk.Button(frame_icon3,image=icon_image_ara2, bd=0, cursor="hand2",command=arama_sozluk_tr)
aramaButon22.pack(side="left", padx=10, pady=5)

iconSearch3 = Image.open("photo/en-tr.png")
iconSearch3 = iconSearch3.resize((60, 20))
icon_image_ara3 = ImageTk.PhotoImage(iconSearch3)
aramaButon33 = tk.Button(frame_icon3,image=icon_image_ara3, bd=0, cursor="hand2",command=arama_sozluk)
aramaButon33.pack(side="left", padx=10, pady=5)

####################################

anlamLabel2 = tk.Label(frame,text="   Anlam   ",font=('castellar','20','bold'),fg="skyblue3", bg="snow3")
anlamLabel2.pack(pady=30)

anlamEntry2 = tk.Entry(frame,font=('arial',22), justify="center",bd=8,relief="ridge")
anlamEntry2.pack()

####################################

frame_icon4 = tk.Frame(frame, background="whitesmoke",bd=5, relief="ridge")
frame_icon4.pack(pady=10)

iconClear2 = Image.open(icon_clear)
iconClear2 = iconClear2.resize((35, 35))
icon_image_clear2 = ImageTk.PhotoImage(iconClear2)
clearButon2 = tk.Button(frame_icon4,image=icon_image_clear2, bd=0, cursor="hand2",command=temizle2)
clearButon2.pack( padx=10, pady=5)

#################################

icon_exit = "photo/icon_exit.png"
iconExit = Image.open(icon_exit)
iconExit = iconExit.resize((35, 35))
icon_image_exit = ImageTk.PhotoImage(iconExit)
exitButon = tk.Button(app,image=icon_image_exit, bd=0, cursor="hand2", command=cikis)
exitButon.pack(pady=30)

def enterFunc(event):  #olay işlevleri (event handlers)
    aramaButon.invoke()
    # programatik | buton tıklanmış gibi olur ve butona bağlı  komut çalışır.

app.bind('<Return>',enterFunc) # olay baglama enter basinca sagdaki calisir

# Pencere boyutları değiştiğinde resmi yeniden boyutlandırın
app.bind("<Configure>", resize_image)
app.tk.call('wm', 'iconphoto', app._w, icon2)


app.mainloop()

#sayfalara ayır
#tr-in seçeneği
#çıktılarını alsınlar

#https://www.youtube.com/watch?v=ofwJDREUr64
#https://drive.google.com/file/d/1wwVep1WNB39UZQopx6FZowJhL7jsw-VU/view
#https://www.youtube.com/watch?v=Kmlgbv3qVZA&list=PLUgFQtEcQLl8FhnV-AlmpvQO-jYXdChQm&index=3
#https://www.youtube.com/watch?v=TE2lXUXgFmg&list=PLUgFQtEcQLl_TmkNjA-UHg-PNABqTuXPb&index=12
#https://www.youtube.com/watch?v=tuvBW0AHIho&list=PLv5gvG08kLQenCfeJAglvSHhg5caqxlcQ&index=16
