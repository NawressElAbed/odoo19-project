from odoo import models, fields, api

class StaticDashboard(models.Model):
    _name = 'static.dashboard'
    _description = 'Tableau de bord statique'

    title = fields.Char(string="Titre")

    nbre_candidats = fields.Integer(
        string="Nombre de candidats",
        compute="_compute_counts",
        store=True
    )

    nbre_postes = fields.Integer(
        string="Nombre de postes",
        compute="_compute_counts",
        store=True
    )

    total_candidats = fields.Integer(
        string="Total",
        compute="_compute_total",
        store=True
    )

    pourcentage = fields.Float(
        string="Pourcentage (%)",
        compute="_compute_pourcentage",
        store=True
    )

    @api.depends('title')
    def _compute_counts(self):
        for rec in self:

            if 'hr.job' not in self.env or 'hr.applicant' not in self.env:
                rec.nbre_postes = 0
                rec.nbre_candidats = 0
                continue

            if rec.title == "Resource humaine":

                rec.nbre_postes = self.env['hr.job'].search_count([
                    '|',
                    ('name', 'ilike', 'RH'),
                    ('name', 'ilike', 'resource')
                ])

                rec.nbre_candidats = self.env['hr.applicant'].search_count([
                    '|',
                    ('job_id.name', 'ilike', 'RH'),
                    ('job_id.name', 'ilike', 'resource')
                ])

            elif rec.title == "Développement web":

                rec.nbre_postes = self.env['hr.job'].search_count([
                    '|','|','|','|','|','|',
                    ('name', 'ilike', 'web'),
                    ('name', 'ilike', 'python'),
                    ('name', 'ilike', 'odoo'),
                    ('name', 'ilike', 'développeur'),
                    ('name', 'ilike', 'ingénieur'),
                    ('name', 'ilike', 'react'),
                    ('name', 'ilike', 'nestjs'),
                ])

                rec.nbre_candidats = self.env['hr.applicant'].search_count([
                    '|','|','|','|','|','|',
                    ('job_id.name', 'ilike', 'web'),
                    ('job_id.name', 'ilike', 'python'),
                    ('job_id.name', 'ilike', 'odoo'),
                    ('job_id.name', 'ilike', 'développeur'),
                    ('job_id.name', 'ilike', 'ingénieur'),
                    ('job_id.name', 'ilike', 'react'),
                    ('job_id.name', 'ilike', 'nestjs'),
                ])

            elif rec.title == "Développement mobile":

                rec.nbre_postes = self.env['hr.job'].search_count([
                    ('name', 'ilike', 'mobile')
                ])

                rec.nbre_candidats = self.env['hr.applicant'].search_count([
                    ('job_id.name', 'ilike', 'mobile')
                ])

            else:
                rec.nbre_postes = 0
                rec.nbre_candidats = 0

    @api.depends('nbre_candidats')
    def _compute_total(self):
        total = sum(self.search([]).mapped('nbre_candidats'))
        for rec in self:
            rec.total_candidats = total

    @api.depends('nbre_candidats')
    def _compute_pourcentage(self):
        total = sum(self.search([]).mapped('nbre_candidats'))

        for rec in self:
            if total > 0:
                rec.pourcentage = (rec.nbre_candidats / total) * 100
            else:
                rec.pourcentage = 0

    def action_open_blank_page(self):
        blank_page = self.env['blank.page'].search([], limit=1)
        if not blank_page:
            blank_page = self.env['blank.page'].create({'name': 'Quiz'})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quiz - Page 1 (1/2)',
            'res_model': 'blank.page',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_blank_page_form_page1').id, 'form')],
            'target': 'current',
            'res_id': blank_page.id,
            'context': {'create': False},
        }

    def action_open_blank_page_mobile(self):
        blank_page_mobile = self.env['blank.page.mobile'].search([], limit=1)
        if not blank_page_mobile:
            blank_page_mobile = self.env['blank.page.mobile'].create({'name': 'Quiz'})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quiz - Page 1 (1/2)',
            'res_model': 'blank.page.mobile',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_blank_page_form_page1_mobile').id, 'form')],
            'target': 'current',
            'res_id': blank_page_mobile.id,
            'context': {'create': False},
        }

    def action_open_blank_page_resource(self):
        blank_page_resource = self.env['blank.page.resource'].search([], limit=1)
        if not blank_page_resource:
            blank_page_resource = self.env['blank.page.resource'].create({'name': 'Quiz'})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quiz - Page 1 (1/2)',
            'res_model': 'blank.page.resource',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_blank_page_form_page1_resource').id, 'form')],
            'target': 'current',
            'res_id': blank_page_resource.id,
            'context': {'create': False},
        }

    def action_show_candidate_emails(self):
        self.ensure_one()

        domain = []

        if self.title == "Développement web":
            domain = [
                '|', '|', '|', '|', '|', '|',
                ('job_id.name', 'ilike', 'web'),
                ('job_id.name', 'ilike', 'python'),
                ('job_id.name', 'ilike', 'odoo'),
                ('job_id.name', 'ilike', 'développeur'),
                ('job_id.name', 'ilike', 'ingénieur'),
                ('job_id.name', 'ilike', 'react'),
                ('job_id.name', 'ilike', 'nestjs'),
            ]
            quiz_action = self.env.ref('dashboard_recruteur.action_blank_page')

        elif self.title == "Développement mobile":
            domain = [
                ('job_id.name', 'ilike', 'mobile')
            ]
            quiz_action = self.env.ref('dashboard_recruteur.action_blank_page_mobile')

        elif self.title == "Resource humaine":
            domain = [
                '|',
                ('job_id.name', 'ilike', 'RH'),
                ('job_id.name', 'ilike', 'resource')
            ]
            quiz_action = self.env.ref('dashboard_recruteur.action_blank_page_resource')

        else:
            quiz_action = self.env.ref('dashboard_recruteur.action_blank_page')


        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        quiz_link = f"{base_url}/web#action={quiz_action.id}"

        return {
            'name': 'Emails des candidats',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.applicant',
            'view_mode': 'list',
            'views': [(self.env.ref('dashboard_recruteur.view_applicant_email_list').id, 'list')],
            'target': 'current',
            'domain': domain,
            'context': {
                'default_body': f"""
                    <p>Bonjour,</p>
                    <p>Voici le lien du quiz :</p>
                    <p><a href="{quiz_link}">Accéder au quiz</a></p>
                    <p>Bon courage</p>
                """,
            }
        }