# strsplit by not-nef

def inbetween(string, start, end):
    result = string.split("{}".format(start), 1)[1]
    result = result.split("{}".format(end), 1)[0]
    return result

def before(string, end):
    result = string.split("{}".format(end), 1)[0]
    return result

def after(string, start):
    result = string.split("{}".format(start), 1)[1]
    return result