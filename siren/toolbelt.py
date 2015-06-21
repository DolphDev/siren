# This Document handles usefull tools that do not need outside 
#
#
#
#
#
#
#


def sort_cap(cap):
    return sorted(cap, time_scoring)

def city2list(c):
    if not type(c) is str:
        raise ValueError("Argument was "+str(type(c))+" , instead of str")
    return c.split("; ")

def pretty_time(t): 
    if not type(t) is str:
        raise ValueError("Argument was "+str(type(t))+" instead of str")
    time = t.split("T")
    return {"date": time[0], "time":""}

def _score_date(arg):
    timev = arg.split("-")
    for x in range(len(timev)):
        timev[x] = int(timev[x])
    timev[0],timev[1],timev[2] = timev[0]*1000, timev[1]*100, timev[2]*10
    return sum(timev)   

def _score_time(arg):
    timev = arg.split(":")
    timev[0],timev[1] = int(timev[0])*1000, timev[1]*100
    return sum(timev[:1])

def time_scoring(arg, _):
    date = arg["effective"].split("T")
    date_score = _score_date(date[0])
    time_score = _score_time(date[1])
    return date_score + time_score
