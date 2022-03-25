# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class TerminateReason(models.TransientModel):
    """Defining TransientModel to terminate reason."""

    _name = "terminate.reason"
    _description = "Terminate Reason"

    reason = fields.Text('Reason')

    def save_terminate(self):
        '''Method to terminate student and change state to terminate.'''
        self.env['student.student'].browse(
                self._context.get('active_id')).write({
                                'state': 'terminate',
                                'terminate_reason': self.reason,
                                'active': False})
        student_rec = self.env['student.student'].browse(
                                    self._context.get('active_id'))
        student_rec.standard_id._compute_total_student()
        user = self.env['res.users'].search([
                            ('id', '=', student_rec.user_id.id)])
        student_reminder = self.env['student.reminder'].search([
                                    ('stu_id', '=', student_rec.id)])
        for rec in student_reminder:
            rec.active = False
        if user:
            user.active = False
