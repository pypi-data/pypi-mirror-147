import datetime
class Sys:
    def __init__(self):
        self.mydate = datetime.datetime.now()
    def now(self):
        res = str(self.mydate)
        return (res[0:19])
    def time(self):
        res = str(self.mydate)
        return (res[11:19])
    def date(self):
        res = str(self.mydate.date())
        return(res)
    def year(self):
        res = str(self.mydate.year)
        return(res)
    def month(self):
        res = str(self.mydate.month)
        return (res)
    def day(self):
        res = str(self.mydate.day)
        return (res)
    def hour(self):
        res = str(self.mydate.hour)
        return (res)
    def minute(self):
        res = str(self.mydate.minute)
        return (res)
    def second(self):
        res = str(self.mydate.second)
        return (res)



if __name__ =='__main__':
    print(Sys().now())
    print(Sys().time())
    print(Sys().date())
    print(Sys().year())
    print(Sys().month())
    print(Sys().day())
    print(Sys().hour())
    print(Sys().minute())
    print(Sys().second())
