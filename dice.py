# coding:utf-8
import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from scipy.special import comb
import sys

def main(n):
    l = len(str(n))

    res = 0
    str_ = ""
    str_ += "Ones Count (p = 1 / 3):\n"
    p = 1 / 3
    for x in range(0, n+1):
        tmp = count(n, p, x)
        x = str(x).zfill(l)
        if 1 - res < 0:
            res = 1
        str_ += f"Exactly {x} in {n}:  {tmp:.3f}  |  At least {x} in {n}:  {1-res:.3f}\n"
        res += tmp

    str_ += "-"*54 + "\n"

    res = 0
    str_ += "Ones Not Count (p = 1 / 6):\n"
    p = 1 / 6
    for x in range(0, n+1):
        tmp = count(n, p, x)
        x = str(x).zfill(l)
        if 1 - res < 0:
            res = 1
        str_ += f"Exactly {x} in {n}:  {tmp:.3f}  |  At least {x} in {n}:  {1-res:.3f}"
        if x != n:
            str_ += "\n"
        res += tmp

    return str_

def count(n, p, x):
    return comb(n, x) * p**x * (1-p)**(n-x)

def application(environ, start_response):
    start_response('200 OK', [('Content-Type','text')])
    params = parse_qs(environ['QUERY_STRING'])
    try:
        n = params['n'][0]
        if not check(n):
            raise ValueError
        res = main(int(n))
    except Exception:
        res = "Error!"
    return [res.encode()]

def check(n):
    try:
        n = int(n)
    except Exception:
        return False
    if n > 1000 or n <= 0:
        return False
    return True

if __name__ == "__main__":
    port = 5088
    httpd = make_server("0.0.0.0", port, application)
    print("serving http on port {0}...".format(str(port)))
    httpd.serve_forever()