#!/usr/bin/python3
#-*-coding:UTF-8-*-
#Author: LeafLight
#Date: 2024-02-18 15:29:26
#---
import os
import typer
from rich import print, print_json, inspect
import importlib
import json
import tempfile
from subprocess import call

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# In Brief:
# - Get Time
# - Write Template
# - Open Vim
app = typer.Typer()

@app.command()
def addNote(name:str, path: str):
    """Add key-value to note.json\n
    name: the name of the notebook
    path: the path of the notebook
    note.json: the json file to store the config

    """
    with open('note.json', 'r') as f:
        note_json = json.load(f)
    if name not in note_json.keys():
        os.mkdir(os.path.join("tplt", name))

    note_json[name] = path
    with open('note.json', 'w') as f:
        json.dump(note_json, f, indent=2)



@app.command()
def addTplt(name:str, tplt: str, o: bool = False):
    """Add script that contains the variable `tplt` in path mentioned below\n
    name: the name of the notebook
    tplt: the name of the template
    o: open the script file with vim  after this command 

    This command will generate a python scrtipt named `[name_of_tplt].py` in the filefold named `[name_of_the_notebook]`(create if not exist)
    """

    default_content = """#!/bin/python3

tplt = 
"""
    tgt_folder = os.path.join("./tplt", name)
    tgt_tplt = os.path.join(tgt_folder, tplt + ".py")
    # create the folder if not exists
    if not os.path.exists(tgt_folder):
        os.mkdir(tgt_folder)
    # create an empty file
    with open(tgt_tplt, "w") as f:
        f.write(default_content)

    print("New Template Created!(%s)" % name)
    print("Template Script Location: %s" % tgt_folder)
    print("[bold green]Don't Forget to Edit it!")

    if o:
        EDITOR = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'vim'
        call([EDITOR, tgt_tplt])
        print("...")
        print("[bold green]tplt editted")
        def test():
            try:
                tplt_module = importlib.import_module('.'.join(['tplt', name, tplt]))
                inspect(tplt_module.tplt)
            except:
                with open(tgt_tplt, 'r') as f:
                    print(f.read())
                print("[bold red]Error In the tplt!Make sure there is an string variable named `tplt` in the python script")
                print("[bold yellow]Edit this tplt[Y/n]?") 
                edit_flag = input(">")
                if edit_flag in ['Y', 'y']:
                    call([EDITOR, tgt_tplt])
                    test()
        test()



        

        
@app.command()
def n(name:str, tplt: str, o: bool = True):
    """Append template to the notebook and open it with vim \n
    name: the name of the notebook
    tplt: the name of the template
    o: open the notebook if True
    """
    with open("note.json", "r") as f:
        note_json = json.load(f)

    tgt_note = note_json[name]
    tplt_module = importlib.import_module('.'.join(['tplt', name, tplt]))

    with open(tgt_note, 'a') as f:
        f.write(tplt_module.tplt)

    if o:
        EDITOR = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'vim'
        call([EDITOR, tgt_note])

@app.command()
def list(name:str = None):
    """List the key-value pair in note.json, or list templates of specified note if name was given
    name: name of the note of which templates you want to inspect
    """
    if not name:
        with open('note.json', 'r') as f:
            note_json = json.load(f)
        print_json(data=note_json)
    else:
        try:
            tplt_list = os.listdir(os.path.join("tplt", name))
            print("[bold green]" + name + ":")
            for t in tplt_list:
                print("- " + t[:-3])
        except:
            print("[bold red]" + "Not found, Check Your Note Name")
            with open('note.json', 'r') as f:
                note_json = json.load(f)
            print(note_json)

@app.command()
def check(t:bool = False):
    """check if all the key-value pairs in note.json are available\n
    t: also check if the templates are available
    """

    # get all the names and paths stored in note.json
    with open('note.json', 'r') as f:
        note_json = json.load(f)
    names = note_json.keys()
    paths = [note_json[n] for n in names]
    names_available = [n for n in names if os.path.exists(note_json[n])]
    paths_available = [p for p in paths if os.path.exists(p)]
    names_unavailable = [n for n in names if not os.path.exists(note_json[n])]
    paths_unavailable = [p for p in paths if not os.path.exists(p)]
    for na in names_available:
        print(
                "[bold green] %s [/bold green]: [green]available[green]" % (
                    na
                    )
                )
        tms = os.listdir(os.path.join("./tplt", na))
        if t:
            for tm in tms:
                try:
                    tplt = importlib.import_module('.'.join(['tplt', na, tm]))
                    print("\t%s: %s" % (
                        "[bold blue]" + tm,
                        "[green]" + "available"
                        )
                          )
                except:
                    print("\t%s: %s" % (
                        "[bold orange]" + tm,
                        "[red]" + "unavailable"
                        )
                          )

    for nu in names_unavailable:
        print(
                "[bold red] %s [/bold red]: [orange]%s[/orange] [red]unavailable[red]" %(
                    nu,
                    note_json[nu]
                    )
                )


if __name__ == "__main__":
    app()
