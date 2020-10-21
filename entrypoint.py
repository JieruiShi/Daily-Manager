#!/usr/bin/env python
# -*- coding: utf-8 -*-
import diaryWritter
import webBrowser.emailBrowser
import myPlans.TODOs

while True:
    choice = input('What would you like to do?\n---web (shortcut: email)\n---diary\n---todo\n')
    if 'diary' in choice:
        print(20 * '-' + 'enter diary section' + 20 * '-')
        diaryWritter.main()
        print (20*'-' + 'exit diary section' + 20*'-')

    if choice[:5] == 'email':
        print(20 * '-' + 'enter email section' + 20 * '-')
        webBrowser.emailBrowser.main(choice)
        print(20 * '-' + 'exit email section' + 20 * '-')

    if 'web' in choice:
        print(20 * '-' + 'enter web section' + 20 * '-')
        webBrowser.emailBrowser.main()
        print(20 * '-' + 'exit web section' + 20 * '-')

    if 'todo' in choice:
        print(20 * '-' + 'enter todo section' + 20 * '-')
        myPlans.TODOs.main('myPlans/todo.json','myPlans/archieve.json')
        print(20 * '-' + 'exit todo section' + 20 * '-')

    if input('terminate(y/n): ') == 'y':
        break
