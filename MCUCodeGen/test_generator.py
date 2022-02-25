import pytest
from .generator import *


class TestGenerator:
    date = "2022-02-12T13:44"

    def test_date_formatter(self):
        formatted_date = Generator(date=self.date)
        print(formatted_date)
        # pytest.fail(f"{formatted_date}")
        assert 0

class TestBurn(TestGenerator):
    DPOW = "DPOW"
    DSTP = "DSTP"
    days = [10.78, 2.5, 5.75, 3, 4.81, 3]

    def test_appending_lines(self):
        to_write_pow = f"{self.DPOW}  "
        to_write_stp = f"{self.DSTP}  "    
        pw, st = Burn(days=self.days).appending_lines(to_write_pow, to_write_stp)
        assert len(pw) > 5
        assert len(st) > 5

# if __name__ == "__main__":
# test_Burn(Burn.days).write()
