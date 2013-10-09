import pprint

__author__ = 'song'


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def split_list(file_names=["song", 'xiao', "feng", "desk", "book", "cook"]):
    return list(chunks(file_names, 3))


if __name__ == "__main__":
    pprint.pprint(split_list())




