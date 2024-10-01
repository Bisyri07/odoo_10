from odoo import fields, models, api # type: ignore

class WorkOrderCancelWizard(models.TransientModel):
    _name = 'work.order.cancel.wizard'

    work_order_id = fields.Many2one('work.order', string="Work Order")
    cancel_reason = fields.Text(string="Reason for cancellation", required=True)

    @api.multi
    def confirm_cancel(self):
        self.work_order_id.write({
            'state': 'cancelled',
            'notes': (self.work_order_id.notes or '') + "\nCancellation Reason: " + self.cancel_reason
        })
