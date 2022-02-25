import os
import typing
from datetime import datetime

templates_path = os.path.join(os.getcwd(), "templates")

class Generator:
    PHY_FILE: str = os.path.join(templates_path, "no_burn")
    PHY_BURN_FILE: str = os.path.join(templates_path, "burn")
    GEO_FILE: str = os.path.join(templates_path, "geom_be_tvs_6layer")

    data: list[str] = []
    def __init__(self, *args, **kwargs):
        if not kwargs.get("temperature") is None:
            self.temperature = kwargs.get("temperature")+273
        self.kcs = kwargs.get("kcs") #* if in mm --> func to convert to cm

    def __repr__(self):
        return f"<Date - {self.date}>"
     
    def date_formatter(self, str_date):
        formatted_date = datetime.strptime(str_date, '%Y-%m-%dT%M:%S')
        return formatted_date.strftime("%d.%M.%Y")

    def open(self, filename):
        with open(filename, "r", encoding="ISO-8859-1") as f:
            self.data = f.readlines()

class Burn(Generator):
    DPOW: str = "DPOW"
    DSTP: str = "DSTP"
    POWER: float = 7190
    REST: float = 0
    # days = [10.78, 2.5, 5.75, 3, 4.81, 3]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.days = kwargs.get("days")
        # self.days = [10.78, 2.5, 5.75, 3]

    def write(self):
        to_write_pow = f"{self.DPOW}  "
        to_write_stp = f"{self.DSTP}  "
        self.open(self.PHY_BURN_FILE)
        written_pow, written_stp  = self.appending_lines(to_write_pow, to_write_stp)
        indexes = [i for i, v in enumerate(self.data) if self.DPOW in v or self.DSTP in v]
        self.data[indexes[0]] = written_pow
        self.data[indexes[1]] = written_stp 
        return self.data

    def appending_lines(self, pw, stp):
        for i,v in enumerate(self.days):
            if i%2 == 0:
                pw += f" {self.POWER} {v},"
            else:
                 pw += f" {self.REST} {v},"
            stp += f" {v} 1,"
        return pw, stp


class NoBurn(Generator):
    TEMPR: str = "TEMPR"
    hkc: str = "SET hkc"
    kc1: str = "hkc1"
    kc2: str = "hkc2"
    kc3: str = "hkc3"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def writePHY(self):
        to_write = f'{self.TEMPR}   {self.temperature}'
        self.open(self.PHY_FILE)
        index = [i for i, v in enumerate(self.data) if self.TEMPR in v] 
        self.data[index[0]] = to_write
        return self.data

    def writeGEO(self):
        # to_write
        self.open(self.GEO_FILE)
        indexes = [i for i,v in enumerate(self.data) if self.hkc in v]
        for i in indexes:
            interests_part = self.data[i][:-1]
            if self.kc1 in self.data[i]:
                self.data[i] = interests_part + f"-{self.kcs.get('kc1')}" + "\n"
            elif self.kc2 in self.data[i]:
                self.data[i] = interests_part + f"-{self.kcs.get('kc2')}" + "\n"
            elif self.kc3 in self.data[i]:
                self.data[i] = interests_part + f"-{self.kcs.get('kc3')}" + "\n"
        return self.data

    def splitted(self, line, symbol):
        return line.split(symbol)[0]

    