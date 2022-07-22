import easy_get_set
import time

port = '1.3.6.1.2.1.2.2.1.7.'
port1 = '1.3.6.1.2.1.2.2.1.7.1'
port2 = '1.3.6.1.2.1.2.2.1.7.2'
port3 = '1.3.6.1.2.1.2.2.1.7.3'

if __name__ == "__main__":
    s = easy_get_set.snMPP()
    s.set(port2, 1)
    for i in range(15):
        print(s.get(port+str(i+1)))

    print('ok')
