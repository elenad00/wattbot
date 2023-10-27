
from utils import CONN
import matplotlib.pyplot as plotter
def main():
    for id in [book['id'] for book in CONN['Books'].find()]:
        reads_dict = {}
        likes_dict = {}
        instances = CONN['instances'].find({'bookid':id}, {'reads':1, 'date':1,'likes':1})
        for instance in instances: 
            date = instance['date']
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