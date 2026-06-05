import datetime
import functools



class Logger:
    def __init__(self):
        self.logstring = ""
    def append(self,string:str):
        self.logstring += (string + " ")

    def to_file(self,filename:str|None= None):
        if filename is None:
            time = str(datetime.datetime.now().timestamp())
            filename = "notation_" + time + ".txt"
        with open("notations/"+filename,"w") as f:
            f.write(self.logstring)
            return


def log_move(func):

    @functools.wraps(func)
    def wrapper(self, string: str, *args, **kwargs):
        was_successful = func(self, string, *args, **kwargs)

        if was_successful:
            if not hasattr(self, 'logstring'):
                self.logstring = ""

            self.logger.append(string)

        return was_successful

    return wrapper
