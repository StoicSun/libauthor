import concurrent.futures
import requests
from libgen_api import LibgenSearch
from console import console, md
import os


def searcher(s, author, match="F", lang="English", ext="pdf"):
    title_filters = {"Language": f"{lang}", "Extension": f"{ext}"}
    if match == 'Y':
        titles = s.search_author_filtered(
            f"{author}", title_filters, exact_match=True)
    else:
        titles = s.search_author_filtered(
            f"{author}", title_filters, exact_match=False)
    try:
        item_to_download = titles[0]
    except IndexError as e:
        console.print(
            "Either no exact match found or there's no book uploaded in provided format :(", justify="left")
    return titles


def downloader(titles):
		s = LibgenSearch()
		download_links = s.resolve_download_links(titles)
		title = titles['Title']
		with console.status("[i deep_pink2]Sneaking into the library[/i deep_pink2]\n", spinner="aesthetic", spinner_style='blue_violet',speed=0.5):
			r = requests.get(download_links['IPFS.io'])
		with open(f'{title}.pdf', 'wb') as f:
			f.write(r.content)		
		console.print(f"[dark_turquoise]Stole {title} for you[/dark_turquoise] 🦝")

s = LibgenSearch()  # instantiate the Search object
console.print(md)
author = input("Enter the author's name whose books you want to download: ")
author.capitalize
choice = input(
    "Do you want to change the search criteria? Type Y/N, (Default is N): ")
if choice == "Y":
		console.rule("[bold red]Config", style='dark_orange')
		lang = input("Which language do you want those books in?, (Default is English): ")
		lang.capitalize
		ext = input(
        "What format[pdf,epub,djvu,cbz,etc.] do you want the books in?, (Default is pdf): ")
		ext.lower
		match = input("Would like an exact match? Type Y/N, (Default is N): ")
		t = searcher(s, author, match, lang, ext)
else:
    t = searcher(s, author)
path = f'{os.getcwd()}' + f"/{t[0]['Author']}"
os.mkdir(path)
os.chdir(path)		
with concurrent.futures.ProcessPoolExecutor() as executor:
        for books in t:
            executor.submit(downloader, books)
console.print("[b chartreuse2]Got the books [/b chartreuse2]✔️", justify="left")						