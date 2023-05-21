import os
import re
import sys
import subprocess
from itertools import repeat
import concurrent.futures as cf


try:
    import tkinter as tk
except ImportError:
    print('Instalando dependência...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pytube'])
    import tkinter as tk
finally:
    from tkinter import filedialog, messagebox

try:
    from pytube import YouTube
except ImportError:
    print('Instalando dependência...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pytube'])
    from pytube import YouTube

try:
    from tqdm import tqdm
except ImportError:
    print('Instalando dependência...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tqdm'])
    from tqdm import tqdm


file = None
save_path = None


def download_music(link, dest):
    result = re.match('^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]{11}(&\S*)?$', link)
    if not result:
        print(f'O link {link} não é válido! Insira um link do YouTube.')
        return

    content = YouTube(link).streams.filter(only_audio = True).first()
    out_file = content.download(output_path = dest)

    base, _ = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(f'Arquivo {new_file} baixado com sucesso!')


def browse_file():
    global file
    file = filedialog.askopenfilename(filetypes=(('Text Files', '*.txt'),))

    if file:
        file_label["text"] = "Arquivo selecionado: " + file
    else:
        file_label["text"] = "Nenhum arquivo selecionado"


def browse_folder():
    global save_path
    save_path = filedialog.askdirectory()

    if save_path:
        folder_label["text"] = "Diretório selecionado: " + save_path
    else:
        folder_label["text"] = "Nenhum diretório selecionado"


def main():
    global file, save_path
    if not file or not save_path:
        messagebox.showinfo("Erro", "Selecione o arquivo e o diretório de destino!")
        return
    
    with open(file, 'r') as file:
        links = file.readlines()

    print('Download iniciado...')
    with cf.ThreadPoolExecutor() as executor, tqdm(total=len(links)) as pbar:
        for _ in executor.map(download_music, links, repeat(save_path)):
            pbar.update(1)

    print('Download completo!')


window = tk.Tk()
window.title("Musify - YouTube Music Downloader")
window.minsize(400, 200)
window.maxsize(400, 200)


file_button = tk.Button(window, text="Procurar Arquivo", command=browse_file)
file_button.pack(pady=10)

file_label = tk.Label(window, text="Nenhum arquivo selecionado")
file_label.pack()

folder_button = tk.Button(window, text="Salvar em", command=browse_folder)
folder_button.pack(pady=10)

folder_label = tk.Label(window, text="Nenhuma pasta selecionada")
folder_label.pack()

run_button = tk.Button(window, text="Baixar Músicas", command=main)
run_button.pack(pady=10)

window.mainloop()
