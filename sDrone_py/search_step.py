import math as m


def min_pid_coefficient(value):
    counter = 0
    while 1:
        tmp = float(format(value, '10f'))
        o = tmp - m.modf(tmp)[1]
        c = tmp - m.modf(tmp)[0]
        # print(o, c)
        if c < 1:
            value *= 10
            # print(value)
            if o == 0 and c == 0:
                # print(counter)
                return counter
            counter += 1
        elif o < 1:
            value = o
            # print("count")
            continue


def processing(**kwargs):
    args = kwargs
    p_min = 0
    i_min = 0
    d_min = 0
    out_value = ""
    for k, v in args.items():
        if k == "p":
            p_min = min_pid_coefficient(v)
            out_value += "p=" + str(p_min) + ":" + str(v) + ";"
        elif k == "i":
            i_min = min_pid_coefficient(v)
            out_value += "i=" + str(i_min) + ":" + str(v) + ";"
        else:
            d_min = min_pid_coefficient(v)
            out_value += "d=" + str(d_min) + ":" + str(v)
            print("p:%s\ti:%s\td:%s" % (p_min, i_min, d_min))
    return out_value
