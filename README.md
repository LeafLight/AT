---
title: AddToday
tags: ['doc tool'] 
date: 2024-02-18 18:50:31
---
![icon](icon.svg)

# Abstract

A CLI tool help you with templates(often daily templates that are supposed to be appended to diary-like recording markdown file **frequently**). The name __At__ comes from Add Today, Add Templates, Arrange Templates or anything else.

It's aimed to:

- add templates for specified markdown files like diary
- manage those templates

Its advantages:

- Other than static template, templates can be generated by the script you write. At the `example/example_tplt`,  it contains  local date and time. 

- It can freely interact with your editor(default: vim), just:

  ```export EDITOR=YOUREDITOR ```

# Quick Start

1. install the requirements:

   ``` pip install --requirement requirements.txt ```

2. Add notes

   ```python ./at.py addnote [your note's brief name] [/your/note/path]```

3. Add template

   ```python ./at.py addtplt [your addded name] [template name]```

4. Edit template(here is an example, all you need to do is to generate a importable string variable `tplt` )
```
   #!/bin/python3
   #-*-coding:UTF-8-*-
   #Author: LeafLight
   #Date: 2024-02-18 16:03:40
   #---
   from datetime import datetime

   now = datetime.now()
   # Reference:
   # [format codes of datetime](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
   
   ################################
   # this variable below is vital #
   ################################
   tplt = """
   ## %s
   - Day: %s, %s 
   - Week: %s
   - Fullfilling:
   - Keywords: 
   - Next Week Plan:
     """ % (
           now.date(), 
           now.strftime("%a"),
           now.strftime("%p"),
           now.strftime("%W")
           )
```
5. Edit the note with the template having been appended to it

   ```python ./at.py n [note] [template]```

   

   

# Extra

- The `{note: path/to/note}` json file is named `note.json`, edit it if you have changed the location of the notes, or just `addnote` again with new location using the same name.

- command `list`
```
# Print note.json in module rich
python ./at.py list
# Print the templates of specified note name
python ./at.py list --name=YourNoteNameHere
```
