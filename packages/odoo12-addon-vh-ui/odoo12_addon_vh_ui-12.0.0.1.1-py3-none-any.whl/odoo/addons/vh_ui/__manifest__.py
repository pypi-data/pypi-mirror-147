# -*- coding: utf-8 -*-
{
  'name': "vertical-habitatge-ui",

  'summary': """
    UI customizations for habitatge.""",

  'author': "Coopdevs",
  'website': "https://gitlab.com/coopdevs/vertical-habitatge",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
  # for the full list
  'category': 'vertical-habitatge',
  'version': '12.0.0.1.1',

  # any module necessary for this one to work correctly
  'depends': ['base','account','account_payment_partner'],

  # always loaded
  'data': [
    'views/templates.xml',
  ],
}
