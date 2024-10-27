
import datetime
from wattbot_2.wattbot_utilities import CONN
import matplotlib.pyplot as plotter
def main():
    for id in [book['id'] for book in CONN['Books'].find()]:
        reads_dict = {}
        likes_dict = {}
        instances = CONN['instances'].find({'bookid':id}, {'reads':1, 'date':1,'likes':1})
        instances = instances.sort('reads', 1)
        for instance in instances: 
            date = instance['date']
            date = datetime.date(day=int(date[0:2]),month=int(date[2:4]),year=int(date[4:]))
            reads_dict[date] = instance['reads'] 
            likes_dict[date] = instance['likes'] 

        plot(reads_dict, 'Reads')
        plot(likes_dict, 'Likes')
    return True

def plot(dict, ylab):
    x, y = zip(*sorted(dict.items()))
    plotter.plot(x, y)
    plotter.ylabel(ylab)
    plotter.xlabel('Dates')
    plotter.show()
main()