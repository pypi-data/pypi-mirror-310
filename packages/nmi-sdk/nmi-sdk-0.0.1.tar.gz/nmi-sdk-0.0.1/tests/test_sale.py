#!/usr/bin/python3
# @Time    : 2024-11-10
# @Author  : Kevin Kong (kfx2007@163.com)

import unittest
from nmi.api import NMI


class TestSale(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.nmi = NMI("6457Thfj624V5r7WUwc5v6a68Zsd6YEm")

    def test_credit_sale(self):
        data = {
            "type": "sale",
            "ccnumber": "4111111111111111",
            "ccexp": "1025",
            "cvv": "123",
            "amount": "1",
            "security_key": self.nmi.security_key,
        }
        resp = self.nmi.payment.credit_sale(**data)
        print('+++')
        print(resp)
    
if __name__ == "__main__":
    unittest.main()