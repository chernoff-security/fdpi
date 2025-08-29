# Импорт модулей
from pytubefix.file_system import file_system_verify
from pytubefix.helpers import safe_filename
from simple_term_menu import TerminalMenu
from pytubefix.cli import on_progress
from rich.console import Console
from pytubefix import Playlist
from pytubefix import YouTube
import sys
import os


console = Console()


proxies={"http": "http://127.0.0.1:8881", "https": "http://127.0.0.1:8881"}


#ffmpeg объединение аудио с видео
def combine(audio: str, video: str, output: str) -> None:

    if os.path.exists(output):
        os.remove(output)
    code = os.system("ffmpeg -i '" + video +  "' -i '" + audio +  "' -c copy '" + output + "'")
    os.remove(audio)
    os.remove(video)
    if code != 0:
        raise SystemError(code)



# Главное меню
def main_menu():
    # Действия
    options = ["[1] Скачать видео (360p)", "[2] Скачать видео (высокое разрешение)",
               "[3] Скачать аудио (m4a)", "[e] Выход"]
    terminal_menu = TerminalMenu(options, shortcut_key_highlight_style=("bold", "fg_red"), menu_highlight_style=("bold", "bg_red", "fg_black"), title="\n\nВыберите действие:")
    menu_entry_index = terminal_menu.show()


    # Скачиваение видео 360p
    if menu_entry_index == 0:
        url = console.input(" \n\nВведите URL: ")
        os.system("clear")
        
        try:
            video = YouTube(
                proxies=proxies,
                url=url,
                on_progress_callback=on_progress,
            )

            console.print("ИНФОРМАЦИЯ О ВИДЕОРОЛИКЕ:", style="bold red")
            console.print("\tНАЗВАНИЕ:", video.title, style="italic magenta")
            console.print("\tАВТОР:", video.author , style="italic magenta")
            console.print("\tДАТА:", video.publish_date , style="italic magenta")
            console.print("\tПРОСМОТРОВ:", video.views , style="italic magenta")
            console.print("\tПРОДОЛЖИТЕЛЬНОСТЬ:", round(video.length/60), "minutes", style="italic magenta")

            stream = video.streams.get_highest_resolution()
            stream.download()
        except Exception as e:
            console.print(e, style="bold red")


    # Скачивание видео в высоком разрешении
    elif menu_entry_index == 1:
        url = console.input(" \n\nВведите URL: ")
        os.system("clear")
        try:
            yt = YouTube(
                proxies=proxies,

                url=url,
                on_progress_callback=on_progress,
            )

            video_stream = yt.streams.\
            filter(type='video').\
            order_by('resolution').\
            desc().first()

            audio_stream = yt.streams.\
                filter(mime_type='audio/mp4').\
                order_by('filesize').\
                desc().first()
            console.print("ИНФОРМАЦИЯ О ВИДЕОРОЛИКЕ:", style="bold red")
            console.print("\tНАЗВАНИЕ:", yt.title, style="italic magenta")
            console.print("\tАВТОР:", yt.author , style="italic magenta")
            console.print("\tДАТА:", yt.publish_date , style="italic magenta")
            console.print("\tРАЗРЕШЕНИЕ:", video_stream.resolution, style="italic magenta")
            console.print("\tПРОСМОТРОВ:", yt.views , style="italic magenta")
            console.print("\tПРОДОЛЖИТЕЛЬНОСТЬ:", round(yt.length/60), "minutes", style="italic magenta")
            console.print("\tИМЯ ФАЙЛА:", video_stream.default_filename, style="italic magenta")
            console.print("\tРАЗМЕР ФАЙЛА:", round(
                video_stream.filesize / 1000000), "MB", style="italic magenta")

            console.print("\nСкачивание видео...", style="bold red")
            video_stream.download()
            console.print("\nСкачивание аудио...", style="bold red")
            audio_stream.download()

            combine(audio_stream.default_filename, video_stream.default_filename,
                    f'{yt.title}_convert.mp4')
        except Exception as e:
            console.print(e, style="bold red")


    # Скачивание аудио    
    elif menu_entry_index == 2:
        try:
            url = console.input(" \n\nВведите URL: ")
            os.system("clear")
            yt = YouTube(
                proxies=proxies,

                url=url,
                on_progress_callback=on_progress,
            )

            audio_stream = yt.streams.\
                filter(mime_type='audio/mp4').\
                order_by('filesize').\
                desc().first()

            audio_stream.download()
        except Exception as e:
            console.print(e, style="bold red")

    # Завершение программы
    elif menu_entry_index == 3:
        os.system("clear")
        sys.exit(0)


os.system("clear")

while True:
    main_menu()