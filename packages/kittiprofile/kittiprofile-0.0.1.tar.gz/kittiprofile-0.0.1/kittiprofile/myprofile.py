
class Profile():
    '''
    Example:

    my = Profile('Kong')
    my.company = 'PSU'
    my.hobby = ['Fishing ','Running','Sleeping']
    print(my.name)
    my.show_email()
    my.show_myart()
    my.show_hobby()
    
    '''
    def __init__(self,name):
        self.name = name
        self.company = ''
        self.hobby = []
        self.art = '''
            |\_/|                  
            | @ @   Woof! 
            |   <>              _  
            |  _/\------____ ((| |))
            |               `--' |   
        ____|_       ___|   |___.' 
        /_/_____/____/_______|
        '''

    def show_email(self):
        if self.company != '':
            print('{}@{}.com'.format(self.name.lower(),self.company.lower()))
        else:
            print('{}@gmail.com'.format(self.name.lower()))

    def show_myart(self):
        print(self.art)

    def show_hobby(self):
        if len(self.hobby) != 0:
            print('-------my hobby-------')
            for i,h in enumerate(self.hobby,start=1):
                print(i,h)
            print('----------------------')
        else:
            print('No hobby')

if __name__ == '__main__':
    my = Profile('Kong')
    my.company = 'PSU'
    my.hobby = ['Fishing ','Running','Sleeping']
    print(my.name)
    my.show_email()
    my.show_myart()
    my.show_hobby()
    # help(my)
