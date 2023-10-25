# classes.py

from datetime import datetime

class Book_Instance:
    def __init__(self, title, id, date, reads, likes, chapters):
        self.id = id
        self.title = self.get_strip(title)
        self.date = date
        self.reads = self.get_strip(reads)
        self.likes = self.get_strip(likes)
        self.chapters = self.get_strip(chapters)
        
        self.avglpc = round(self.likes/self.chapters, 1)
        self.avgrpl = round(self.reads/self.likes) 
        self.interaction = round((self.likes*self.likes)/(self.reads*self.chapters),2)

    def get_stats(self):
        instance = {
            'bookid':self.id,
            'date':self.date,
            'reads':self.reads,
            'likes': self.likes,
            'chapters': self.chapters,
            'avglpc': self.avglpc,
            'readsperlike': self.avgrpl,
            'interaction': self.interaction
        }
        return instance
    
    def get_strip(self, spanval):
        strippedval = str(spanval).replace('<span class="sr-only">', '').replace(',','').replace('</span>','')
        try: strippedval = int(strippedval)
        except ValueError: pass
        return strippedval
    
    def print_today(self):
        print(self.title)
        print('  Reads:',self.reads,'\n  Likes:',self.likes,'\n  Chapters:', self.chapters)
        print('  Average Likes Per Chapter:', self.avglpc)
        print('  Reads per Like:', self.avgrpl)
        print('  Interaction Score:', self.interaction)
        print('')
    
    
class Compare:
    def __init__(self, today, yesterday):
        self.days = self.compare_dates(today.date, yesterday.date)
        self.reads = self.calculate(today.reads, yesterday.reads)
        self.likes = self.calculate(today.likes, yesterday.likes)
        self.chapters = self.calculate(today.chapters, yesterday.chapters)
        self.lpc = self.calculate(today.avglpc, yesterday.avglpc)
        self.rpl = self.calculate(today.avgrpl, yesterday.avgrpl)
        self.int = self.calculate(today.interaction, yesterday.interaction)
    
    def calculate(self, tv, yv):
        minus = tv-yv
        if minus == 0:
            return '0'
        if type(minus) == float:
            minus = round(minus, 1)
        if minus>0:
            return '+'+str(minus)
        else:
            return minus
        
    def compare_dates(self, t, y):
        td = datetime(int(t[4:8]),int(t[2:4]),int(t[0:2]), 0, 0)
        yd = datetime(int(y[4:8]),int(y[2:4]),int(y[0:2]), 0, 0)
        return (str(td-yd).split(','))[0]

    def print_comparison(self):
        print('Differences over the last', self.days)
        print('  Reads:',self.reads,'\n  Likes:',self.likes,'\n  Chapters:', self.chapters)
        print('  Average LpC:', self.lpc)
        print('  Reads per Like:', self.rpl)
        print('  Interaction Score:', self.int)
        print('')