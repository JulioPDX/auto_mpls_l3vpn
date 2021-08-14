from netaddr import IPNetwork


def address(add):
    "Grab IP from address, example 10.0.0.1/24, will return '10.0.0.1'"
    add = str(IPNetwork(add).ip)
    return add


def mask(submask):
    "Grab subnet mask from address, example 10.0.0.1/24, will return '255.255.255.0'"
    submask = str(IPNetwork(submask).netmask)
    return submask
