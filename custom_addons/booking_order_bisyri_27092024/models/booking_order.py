from odoo import models, fields, api, _ # type: ignore
from odoo.exceptions import ValidationError # type: ignore

class BookingOrderInherit(models.Model):
    _inherit='sale.order'

    is_booking_order = fields.Boolean(string='Is booking Order', default=True)
    team_id = fields.Many2one('service.team', string='Team', required=True)
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
            
