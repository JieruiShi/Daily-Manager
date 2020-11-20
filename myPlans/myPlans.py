#this module aims to record my long-term and short-term plans
#they should be stored in an external .txt document within the same folder
#they are in a stack like structure, though I don't have to do the last plan first

import datetime
#note datetime is a module, within it there's a datetime class

def main():
    def contentFormat(myContent):
        """Defines how each content should be formatted, timestamp is added"""
        currenttimestamp = round(datetime.datetime.timestamp(datetime.datetime.now()))
        return myContent + '  ' + str(currenttimestamp) + '\n'

    completed = False
    while not completed:
        choice = input('what would you like to do?\n--read(r)\n--write short-term(s) or long-term(l)\n')
        if choice and choice[0:1] == 'td':
            if len(choice) > 1 and choice[1] == ' ' and choice[1:].strip():
            #condition: longer than single character, have at least one space separating and content exists
                planwrite = choice[1:].strip()
            else:
                planwrite = input('input short term plan: ')

            with open('short-term.txt', 'r') as b:
                _ = b.read()
            with open('short-term.txt', 'w') as a:
                a.write(contentFormat(planwrite) + _)

        elif choice and choice[0] == 'l':
            if len(choice) > 1 and choice[1] == ' ' and choice[1:].strip():
            # condition: longer than single character, have at least one space separating and content exists
                planwrite = choice[1:].strip()
            else:
                planwrite = input('input long term plan: ')

            with open('long-term.txt', 'r') as b:
                _ = b.read()
            with open('long-term.txt', 'w') as a:
                a.write(contentFormat(planwrite) + _)

        elif choice and choice[0] == 'r':
            pass

        if input('write another (y/n)?: ') != 'y':
            completed = True

    print('ending')


if __name__ == '__main__':
    main()