from odoo import fields, models # type: ignore

class ServiceTeam(models.Model):
    _name='service.team'
    _description='service_team'
    _rec_name='team_name'

    team_name = fields.Char(string='Team Name', required=True)
    team_leader = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members')


    