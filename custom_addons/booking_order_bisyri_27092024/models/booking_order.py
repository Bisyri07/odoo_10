from odoo import models, fields, api, _ # type: ignore
from odoo.exceptions import ValidationError # type: ignore

class BookingOrderInherit(models.Model):
    _inherit='sale.order'

    is_booking_order = fields.Boolean(string='Is booking Order', default=True)
    team_id = fields.Many2one('service.team', string='Team', required=True, ondelete='set null')
    team_leader_id = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members_id = fields.Many2many('res.users', string='Team Members', required=True)
    booking_start = fields.Datetime(string='Booking start', required=True)
    booking_end = fields.Datetime(string='Booking end', required=True)

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sale Order'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], 
       string='Order Status', 
       readonly=True, 
       copy=False, 
       store=True, 
    )

    @api.constrains('team_member_ids')
    def _check_team_members(self):
        for record in self:
            if not record.team_member_ids:
                raise ValidationError(_('Team Members cannot be empty.'))
            
    # kondisi dimana ketika team diisi leader dan member terisi juga
    @api.onchange('team_id')
    def onchange_team_id(self):
        if self.team_id:
            self.team_leader_id = self.team_id.team_leader
            self.team_members_id = self.team_id.team_members

    @api.multi
    def action_check_availability(self):
        for record in self:
            # Get the active work orders for the team
            active_work_orders = self.env['work.order'].search([
                ('team_id', '=', record.team_id.id),
                ('state', '!=', 'cancelled'),
                ('planned_start', '<=', record.booking_end),
                ('planned_end', '>=', record.booking_start),
            ])
            
            if active_work_orders:
                work_order = active_work_orders[0]
                raise ValidationError(_("Team already has work order during that period on SO%s" % work_order.booking_order_reference.id))
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Success'),
                        'message': _('Team is available for booking'),
                        'type': 'success',
                        'sticky': False,
                    }
                }
            
    @api.multi
    def action_confirm(self):
        for record in self:
            # Check availability before confirming the order
            active_work_orders = self.env['work.order'].search([
                ('team_id', '=', record.team_id.id),
                ('state', '!=', 'cancelled'),
                ('planned_start', '<=', record.booking_end),
                ('planned_end', '>=', record.booking_start),
            ])

            if active_work_orders:
                work_order = active_work_orders[0]
                raise ValidationError(_("Team is not available during this period, already booked on SO%s. Please book on another date." % work_order.booking_order_reference.id))
            else:
                # Confirm the order as usual and create a work order
                super(BookingOrderInherit, self).action_confirm()
                
                # Create work order
                self.env['work.order'].create({
                    'booking_order_reference': record.id,
                    'team_id': record.team_id.id,
                    'team_leader_id': record.team_leader_id.id,
                    'team_members_id': [(6, 0, record.team_members_id.ids)],
                    'planned_start': record.booking_start,
                    'planned_end': record.booking_end,
                    'state': 'pending',
                })