import code

def dominate(obj1, obj2, dimensi):
    code.interact(local=dict(globals(), **locals()))
    dominate_status = 0
    for i in range(0, dimensi):
        if obj1[i] > obj2[i]:
            if dominate_status == -1:
                dominate_status = 0
                break
            dominate_status = 1
        elif obj1[i] < obj2[i]:
            if dominate_status == 1:
                dominate_status = 0
                break
            dominate_status = -1
    return dominate_status