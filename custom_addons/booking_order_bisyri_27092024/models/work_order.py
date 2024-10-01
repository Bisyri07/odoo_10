from odoo import models, fields, api # type: ignore
from odoo.exceptions import UserError # type: ignore


class WorkOrder(models.Model):
    _name = 'work.order'
    _inherit = ['mail.thread']  # Adds chatter functionality

    wo_number = fields.Char(string='WO Number', readonly=True, default='New')
    booking_order_ref = fields.Many2one('sale.order', string='Booking Order Reference', readonly=True)
    team_id = fields.Many2one('service.team', string='Team', required=True, ondelete='cascade')
    team_leader_id = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members')
    planned_start = fields.Datetime(string='Planned Start', required=True)
    planned_end = fields.Datetime(string='Planned End', required=True)
    date_start = fields.Datetime(string='Date Start', readonly=True)
    date_end = fields.Datetime(string='Date End', readonly=True)
    notes = fields.Text(string='Notes')
    booking_order_reference = fields.Many2one('sale.order', string="Booking Order Reference")
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='State', default='pending', track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('wo_number', 'New') == 'New':
            vals['wo_number'] = self.env['ir.sequence'].next_by_code('work.order') or 'New'
        return super(WorkOrder, self).create(vals)

    def action_start_work(self):
        self.write({
            'state': 'in_progress',
            'date_start': fields.Datetime.now(),
        })

    def action_end_work(self):
        self.write({
            'state': 'done',
            'date_end': fields.Datetime.now(),
        })

    def action_reset_work(self):
        self.write({
            'state': 'pending',
            'date_start': False,
        })

    def action_cancel_work(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Work Order',
            'view_mode': 'form',
            'res_model': 'work.order.cancel.wizard',
            'target': 'new',
            'context': {
                'default_work_order_id': self.id
            }
        }
    
    @api.multi
    def render_html(self, docids, data=None):
        docs = self.env['work.order'].browse(docids)
        return self.env['report'].render('booking_order_bisyri_27092024.work_order_report', {'docs': docs})

