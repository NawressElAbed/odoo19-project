from odoo import models, fields, api
from datetime import datetime, timedelta


class InterviewAuto(models.Model):
    _name = 'interview.auto'
    _description = 'Planification automatique des entretiens'

    name = fields.Char(default="Entretien automatique")
    applicant_id = fields.Many2one('hr.applicant', string="Candidat")
    interview_date = fields.Datetime(string="Date entretien")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('scheduled', 'Planifié')
    ], default='draft')

    # =========================
    # AUTOMATISATION
    # =========================
    @api.model
    def cron_schedule_interviews(self):
        """Créer automatiquement des entretiens pour candidats"""

        applicants = self.env['hr.applicant'].search([
            ('active', '=', True)
        ])

        for app in applicants:
            exists = self.search([
                ('applicant_id', '=', app.id)
            ])

            if not exists:
                self.create({
                    'applicant_id': app.id,
                    'interview_date': fields.Datetime.now() + timedelta(days=2),
                    'state': 'scheduled'
                })