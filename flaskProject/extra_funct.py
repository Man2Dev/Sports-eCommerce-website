from database import *


def getdrop():
    sport = Sport.query.all()
    sport_list = [each_sport.name for each_sport in sport]
    return sport_list