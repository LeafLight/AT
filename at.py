#!/usr/bin/python3
#-*-coding:UTF-8-*-
#Author: LeafLight
#Date: 2024-02-18 15:29:26
#---
import os
import typer
from rich import print, inspect
import importlib
import json
import tempfile
from subprocess import call
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
    note_json[name] = path
    with open('note.json', 'w') as f:
        json.dump(note_json, f)


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

if __name__ == "__main__":
    app()

