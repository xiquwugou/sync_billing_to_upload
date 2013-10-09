def foo():
    sum = 0
    for i in xrange(10000000):
        sum += i
    return sum

if __name__ == "__main__":
    foo()