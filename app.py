from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter import messagebox
import threading
import yt_dlp


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
    
    'ignoreerrors': True
}

def progress_hook(d):

    if d['status'] == 'downloading':
        
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        
        if total:
            percent = (d['downloaded_bytes'] / total) * 100
            bar['value'] = percent

            window.update_idletasks()

def start():
    url = entry_url.get()
    path = btn_path['text']

    if path == "Select Folder":
        path = ""
    
    threading.Thread(target=download,args=(url,path,)).start()


def download(url,path):
    current_opts = ydl_opts.copy()
    if path:
        current_opts['paths'] = {'home': path} 

    current_opts['progress_hooks'] = [progress_hook]
    try:
        lbl_download['text'] = 'Download Started'
        with yt_dlp.YoutubeDL(current_opts) as ydl:
            ydl.download([url])
            lbl_download['text'] = 'Download Finished'
            messagebox.showinfo('Success','Download Completed')
            
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")       

def select_path():
    path = filedialog.askdirectory()
    btn_path.config(text=path)

window = Tk()
icon = PhotoImage(file='icon.png')
window.iconphoto(True,icon) 
window.geometry("500x400")
window.title("Youtube MP3 Downloader")
window.config(background="grey")

window.columnconfigure((0,1,2,3),weight=1)
window.columnconfigure(3,weight=2)
window.rowconfigure((0,1,2),weight=1)

window.resizable(width=False,height=False)

lbl_url = Label(window,text='Video or Playlist URL:',bg='grey')
lbl_path = Label(window,text='Path:',bg='grey')
lbl_download = Label(window,bg='grey')
btn_path = Button(window,text='Select Folder',command=select_path)
btn_download = Button(window,text='Download',command=start) 
entry_url = Entry(window)
bar = Progressbar(window, length=300, mode='determinate')


lbl_url.grid(row=0, column= 0,sticky='nsew')
lbl_path.grid(row=1, column= 0,sticky='ne')
lbl_download.grid(row=2,column=1,sticky='nw')
entry_url.grid(row=0,column=1,sticky='we')
btn_path.grid(row=1,column=1,sticky='nw')
btn_download.grid(row=2,column=0,sticky='n',pady=12)

bar.grid(row=2,column=1,sticky='wn',pady=20)

window.mainloop()