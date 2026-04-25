# -*- coding: utf-8 -*-

#guestregistration.py
import pytz

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class guestregistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'hotel guest registration list'
    
    grc_id = fields.Integer(string="GRC #")
    room_id = fields.Many2one("hotel.rooms", string="Room No.")
    guest_id = fields.Many2one("hotel.guests", string="Guest Name")
    
    #roomname -< related fields found in the model hotel.rooms  
    roomname=fields.Char("Room No.",related='room_id.name')
    
    #roomtname <- room type name found in the model hotel.rooms 
    # also related to hotel.roomtypes
    roomtname=fields.Char("Room Type",related='room_id.roomtypename')
    
    #guestname <- related field found as a computed field called name in 
    # the model hotel.guests
    guestname=fields.Char("Guest Name",related='guest_id.name')

    datefromsched = fields.Datetime('Scheduled Check In', required=True, index=True, copy=False, default=fields.Datetime.now)
    datetosched = fields.Datetime('Scheduled Check Out', required=True, index=True, copy=False, default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', index=True)
    
    actualpax = fields.Integer("Actual PAX")

    details=fields.Text("Details")  

    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        index=True,
        default=lambda self: self.env.company,  # auto-assign current user's company
    )

    name = fields.Char(string='Guest Registration', compute='_compute_name', store=False)

    @api.depends('room_id', 'guest_id')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.roomname}, {rec.guestname}"

    create_date_ampm = fields.Char(
        string="Created ON",
        compute = '_compute_create_date_ampm',
        store = False # Not in the database
    )

    datefromsched_ampm = fields.Char(
        string="Scheduled Check In",
        compute='_compute_sched_ampm',
        store=False,
    )

    datetosched_ampm = fields.Char(
        string="Scheduled Check Out",
        compute='_compute_sched_ampm',
        store=False,
    )

    def _format_dt_user_tz(self, dt_value):
        if not dt_value:
            return ''
        user_tz = self.env.user.tz or 'UTC'
        dt_utc = fields.Datetime.from_string(dt_value)
        dt_local = pytz.utc.localize(dt_utc).astimezone(pytz.timezone(user_tz))
        return dt_local.strftime('%m-%d-%Y %I:%M:%S %p')

    @api.depends('create_date')
    def _compute_create_date_ampm(self):
        for rec in self:
            rec.create_date_ampm = rec._format_dt_user_tz(rec.create_date)

    @api.depends('datefromsched', 'datetosched')
    def _compute_sched_ampm(self):
        for rec in self:
            rec.datefromsched_ampm = rec._format_dt_user_tz(rec.datefromsched)
            rec.datetosched_ampm = rec._format_dt_user_tz(rec.datetosched)

    grc_id_display = fields.Char(
            string="GRC #",
            compute = "_compute_grc_id_display",
            store = False # Not stored in the database
    )

    @api.depends('grc_id')
    def _compute_grc_id_display(self):
        for rec in self:
            rec.grc_id_display = str(rec.grc_id)

    @api.model_create_multi
    def create(self, vals_list):
        # Odoo passes a list of value dicts in model_create_multi.
        for vals in vals_list:
            if not vals.get('grc_id'):
                seq = self.env['ir.sequence'].next_by_code('hotel.guestregistration')
                vals['grc_id'] = int(seq) if seq else 1

        return super().create(vals_list)

    def action_reserve(self):
        for rec in self:
            rec.state = "reserved"

    def action_checkin(self):
        for rec in self:
            rec.state = "checked_in"

    def action_checkout(self):
        for rec in self:
            rec.state = "checked_out"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancelled"

    def action_mark_draft(self):
        for rec in self:
            rec.state = "draft"

    @api.constrains('datefromsched', 'datetosched')
    def _check_schedule_dates(self):
        for rec in self:
            if rec.datefromsched and rec.datetosched and rec.datetosched <= rec.datefromsched:
                raise ValidationError("Scheduled Check Out must be later than Scheduled Check In.")

    @api.constrains('actualpax')
    def _check_actualpax_non_negative(self):
        for rec in self:
            if rec.actualpax < 0:
                raise ValidationError("Actual PAX cannot be negative.")

    @api.constrains('state', 'guest_id', 'room_id', 'actualpax')
    def _check_required_fields_for_progress_states(self):
        for rec in self:
            if rec.state in ('reserved', 'checked_in', 'checked_out'):
                if not rec.guest_id:
                    raise ValidationError("Guest is required before reserving or checking in/out.")
                if not rec.room_id:
                    raise ValidationError("Room is required before reserving or checking in/out.")
                if rec.actualpax <= 0:
                    raise ValidationError("Actual PAX must be greater than zero before reserving or checking in/out.")