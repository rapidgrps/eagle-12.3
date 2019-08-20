# -*- coding: utf-8 -*-
# Part of Eagle. See LICENSE file for full copyright and licensing details.

{
    'name': 'Blackbox Hardware Driver',
    'category': 'Point of Sale',
    'sequence': 6,
    'summary': 'Hardware Driver for Belgian Fiscal Data Modules',
    'website': 'https://www.eagle-erp.com/page/point-of-sale-hardware',
    'description': """
Fiscal Data Module Hardware Driver
==================================

This module allows a Point Of Sale client to communicate with a
connected Belgian Fiscal Data Module.

This module does **not** turn an Eagle Point Of Sale module into a certified
Belgian cash register. It allows the communication on with a certified Fiscal
Data Module but will not modify the behaviour of the Point of Sale.
""",
    'depends': ['hw_proxy'],
    'external_dependencies': {'python': ['serial']},
    'installable': False,
}
