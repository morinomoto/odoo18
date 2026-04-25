# -*- coding: utf-8 -*-

from odoo import models, fields

class charges(models.Model):
    _name = 'hotel.charges'
    _description = 'hotel charges/accounts master list'
    _order="name"
    
    dailyrate = fields.Float("Daily Rate", digits=(10,2))
    weekendrate = fields.Float("Weekend Rate", digits=(10,2))

    name = fields.Char("Account Name")
    description = fields.Char("Account Description")
    paymentaccount= fields.Boolean("Payment Account", default=False)
    
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        index=True,
        default=lambda self: self.env.company,  # auto-assign current user's company
    )


class dailycharges(models.Model):
    _name = 'hotel.dailycharges'
    _description = 'hotel roomtype daily charges list'
    
    charge_id = fields.Many2one('hotel.charges', string="Charge Title")
    amount = fields.Float("Daily Amount", digits=(10,2))
    roomtype_id = fields.Many2one('hotel.roomtypes', string="Roomtype")    

    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        index=True,
        default=lambda self: self.env.company,  # auto-assign current user's company
    )