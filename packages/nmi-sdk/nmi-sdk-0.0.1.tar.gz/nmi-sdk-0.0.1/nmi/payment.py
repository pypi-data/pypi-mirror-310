#!/usr/bin/python3
# @Time    : 2024-11-10
# @Author  : Kevin Kong (kfx2007@163.com)

from .comm import Comm


class Payment(Comm):
    def credit_sale(
        self, ccnumber=None, ccexp=None, amount=None, payment_token=None, **kwargs
    ):
        data = {
            "ccnumber": ccnumber,
            "ccexp": ccexp,
            "amount": amount,
            "payment_token": payment_token,
        }
        data.update(kwargs)
        return self.post("sale", data)
