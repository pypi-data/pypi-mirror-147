
from ptick_ptock import ptick_ptock

if __name__ == "__main__":
    obj = ptick_ptock()
    print(obj.isTicked())
    obj.ptick()
    print(obj.isTicked())
    print(obj.datetime_ptock())
    obj.print_ptock()