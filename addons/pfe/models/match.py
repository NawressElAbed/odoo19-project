from datetime import timedelta

from odoo import models, fields, api
from ..scripts import match
import base64, io
from pdfminer.high_level import extract_text


class JobCvMatch(models.Model):
    _name = "job.cv.match"
    _description = "Matching CVs ↔ Postes"
    _inherit = ['rating.mixin']

    applicant_id = fields.Many2one("hr.applicant", required=True)
    job_id = fields.Many2one("hr.job", required=True)
    score = fields.Float("Score")

    star_display = fields.Char(compute="_compute_stars", store=True)
    mention = fields.Char(compute="_compute_mention", store=True)

    @api.depends('score')
    def _compute_stars(self):
        for rec in self:
            score = rec.score or 0

            if score == 0.0:
                full = 0
            elif score < 0.5:
                full = 1
            elif score < 0.7:
                full = 2
            elif score < 0.9:
                full = 3
            else:
                full = 4

            empty = 4 - full
            rec.star_display = "⭐" * full + "☆" * empty

    @api.depends('score')
    def _compute_mention(self):
        for rec in self:
            score = rec.score or 0

            if score < 0.5:
                rec.mention = "🙁 Faible"
            elif score < 0.7:
                rec.mention = "😐 Moyen"
            elif score < 0.9:
                rec.mention = "🙂 Bien"
            else:
                rec.mention = "🥰 Très bien"

    def run_matching(self):
        for record in self:
            if not record.applicant_id or not record.job_id:
                continue

            cv_text = record.applicant_id.partner_name or ""

            attachments = self.env['ir.attachment'].search([
                ('res_model', '=', 'hr.applicant'),
                ('res_id', '=', record.applicant_id.id),
                ('mimetype', '=', 'application/pdf')
            ])

            for att in attachments:
                if att.datas:
                    pdf_content = base64.b64decode(att.datas)
                    pdf_stream = io.BytesIO(pdf_content)
                    cv_text += " " + (extract_text(pdf_stream) or "")

            job_text = f"{record.job_id.name or ''} {record.job_id.description or ''}"

            _, similarity_scores = match.run_match([cv_text], [job_text])

            record.score = float(similarity_scores[0, 0])
            if record.score >= 0.5 and record.applicant_id:

                stage = self.env['hr.recruitment.stage'].search([
                    ('name', '=', 'First Interview')
                ], limit=1)

                if stage:
                    record.applicant_id.write({
                        'stage_id': stage.id
                    })
                    if record.score >= 0.5 and record.applicant_id:

                        stage = self.env['hr.recruitment.stage'].search([
                            ('name', '=', 'First Interview')
                        ], limit=1)

                        if stage:

                            record.applicant_id.write({
                                'stage_id': stage.id
                            })

                            interview_start = fields.Datetime.now() + timedelta(days=1)
                            interview_start = interview_start.replace(
                                hour=10,
                                minute=0,
                                second=0
                            )

                            interview_stop = interview_start.replace(hour=11)

                            meeting = self.env['calendar.event'].create({
                                'name': f"Entretien RH - {record.applicant_id.partner_name}",
                                'start': interview_start,
                                'stop': interview_stop,
                                'description': 'Premier entretien RH automatique'
                            })

                            if record.applicant_id.email_from:
                                mail = self.env['mail.mail'].create({
                                    'subject': 'Convocation entretien RH',
                                    'email_to': record.applicant_id.email_from,
                                    'body_html': f"""
                                        <p>Bonjour {record.applicant_id.partner_name},</p>

                                        <p>Votre candidature a été retenue.</p>

                                        <p>Votre entretien RH est programmé :</p>

                                        <p><b>Date :</b> {interview_start.strftime('%d/%m/%Y')}</p>
                                        <p><b>Heure :</b> 10:00</p>
                                        
                                        <p>Localisation : Chayma Building, Yasser Arafat Ave, Sousse, Tunisie</p>

                                        <p>Merci de votre présence.</p>

                                        <br/>
                                        <p>Service Recrutement</p>
                                    """
                                })

                                mail.send()
                                second_stage = self.env['hr.recruitment.stage'].search([
                                    ('name', '=', 'Second Interview')
                                ], limit=1)

                                if second_stage:
                                    record.applicant_id.write({
                                        'stage_id': second_stage.id
                                    })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Matching CVs',
            'res_model': 'job.cv.match',
            'view_mode': 'form',
            'target': 'current',
        }