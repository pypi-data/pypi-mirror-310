#!/usr/bin/python3
# @Time    : 2024-11-10
# @Author  : Kevin Kong (kfx2007@163.com)

from .payment import Payment

class NMI(object):
    def __init__(self, security_key) -> None:
        self.security_key = security_key

    payment = Payment()