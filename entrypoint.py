#!/usr/bin/env python
# -*- coding: utf-8 -*-
import diaryWritter
import webBrowser.emailBrowser
import myPlans.TODOs
import finance.overhead
import config

dailyManagerModules = {
    'diary': (diaryWritter.main, None),
    'todo' : (myPlans.TODOs.main,(config.ACTIVE_FILEPATH, config.ARCHIEVE_FILEPATH)),
    'overhead': (finance.overhead.main,(config.OVERHEAD_FILEPATH,))
}
#the dict above uses module name: (function, parameters) to record the information for each function,
#use None if the funcion doesn't require a parameter and string 'userinput' to pass the command as a parameter

def main():
    inputPrompt = 'What would you like to do?' #entrypoint prompt for input
    for module in dailyManagerModules:
        inputPrompt += '\n---' + module # include the modules for the entrypoint
    inputPrompt += '\nYour input:'
    while True:
        choice = input(inputPrompt)
        for module in dailyManagerModules:
            if module in choice:
                print(20 * '-' + 'entering ' + module + ' section' + 20 * '-')

                func, para = dailyManagerModules[module][0], dailyManagerModules[module][1]
                if para:
                    if para == 'userinput':
                        # the case where the parameter is the userinput
                        func(choice)
                    else:
                        # the case where there are parameters passed into the function
                        func(*para)
                else:
                    # the case where the parameter is None
                    func()

                print (20*'-' + 'exiting ' + module + ' section' + 20*'-')
                break #stop looking for other modules (only one modules can be used with one command in entry point)
        else:
            print('command is not understood.')

        if input('terminate(y/n): ') == 'y':
            break #ask whether to end the whole loop after each command

if __name__ == '__main__':
    main()