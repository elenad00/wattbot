
import datetime
from typing import Dict
from wattbot_utilities import database_connect
import matplotlib.pyplot as plotter

def main() -> None:
    for id in [book['id'] for book in database_connect()['Books'].find()]:
        reads_dict = dict()
        likes_dict = dict()
        instances = database_connect()['instances'].find({'bookid':id}, {'reads':1, 'date':1,'likes':1})
        instances = instances.sort('reads', 1)
        for instance in instances: 
            date = instance['date']
            date = datetime.date(day=int(date[0:2]),month=int(date[2:4]),year=int(date[4:]))
            reads_dict[date] = instance['reads'] 
            likes_dict[date] = instance['likes'] 
        plot(reads_dict, 'Reads')
        plot(likes_dict, 'Likes')

def plot(dict: Dict[str, int], y_axis_label: str) -> None:
    x, y = zip(*sorted(dict.items()))
    plotter.plot(x, y)
    plotter.ylabel(y_axis_label)
    plotter.xlabel('Dates')
    plotter.show()

main()