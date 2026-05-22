from odoo import models, fields, api

class BlankPageResource(models.Model):
    _name = 'blank.page.resource'
    _description = 'Page vide avec quiz'

    name = fields.Char(string="Nom")


    question1 = fields.Selection([
        ('a', 'Il n’y a aucune différence'),
        ('b', 'Interne = candidats de l’entreprise, Externe = candidats hors entreprise'),
        ('c', 'Externe est toujours moins cher'),
        ('d', 'Interne est illégal'),
    ], string="Q1: Quelle est la principale différence entre recrutement interne et externe ?")

    question2 = fields.Selection([
        ('a', 'Une technique de gestion salariale'),
        ('b', 'Une méthode pour structurer les réponses comportementales'),
        ('c', 'Une stratégie de licenciement'),
        ('d', 'Une méthode d’évaluation financière')
    ], string="Q2: Quelle est la méthode STAR utilisée en entretien ?")

    question3 = fields.Selection([
        ('a', 'Une technique de recrutement rapide'),
        ('b', 'Une méthode pour anticiper les besoins en compétences'),
        ('c', 'Une politique de licenciement'),
        ('d', 'Un outil informatique')
    ], string="Q3: Que signifie GPEC (Gestion Prévisionnelle des Emplois et des Compétences) ?")

    question4 = fields.Selection([
        ('a', 'Augmenter les salaires'),
        ('b', 'Attirer et fidéliser les talents'),
        ('c', 'Réduire les coûts RH'),
        ('d', 'Remplacer le service RH')
    ], string="Q4: Quel est l’objectif principal de la marque employeur ?")

    question5 = fields.Selection([
        ('a', 'Se fier uniquement à l’intuition'),
        ('b', 'Utiliser des entretiens structurés'),
        ('c', 'Choisir rapidement le candidat'),
        ('d', 'Ignorer les critères objectifs')
    ], string="Q5: Quelle est une bonne pratique pour éviter les biais en recrutement ?")

    question6 = fields.Selection([
        ('a', 'Les émotions des employés'),
        ('b', 'La performance et l’efficacité des processus RH'),
        ('c', 'La météo'),
        ('d', 'Le chiffre d’affaires uniquement')
    ], string="Q6: Que mesure principalement un KPI RH ?")


    def action_open_quiz_page2_resource(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quiz - Page 2 (2/2)',
            'res_model': 'blank.page.resource',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_blank_page_form_page2_resource').id, 'form')],
            'target': 'current',
            'res_id': self.id,
        }

    def action_back_to_quiz_page1_resource(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quiz - Page 1 (1/2)',
            'res_model': 'blank.page.resource',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_blank_page_form_page1_resource').id, 'form')],
            'target': 'current',
            'res_id': self.id,
        }

    score = fields.Integer(string="Score")
    total_questions = fields.Integer(default=6)
    pourcentage = fields.Float(string="Pourcentage (%)", compute="_compute_result", store=True)
    message = fields.Char(string="Message", compute="_compute_result")

    @api.depends('question1', 'question2', 'question3', 'question4', 'question5', 'question6')
    def _compute_result(self):
        for rec in self:
            score = 0

            if rec.question1 == 'b': score += 1
            if rec.question2 == 'b': score += 1
            if rec.question3 == 'b': score += 1
            if rec.question4 == 'b': score += 1
            if rec.question5 == 'b': score += 1
            if rec.question6 == 'b': score += 1

            rec.score = score

            if rec.total_questions > 0:
                rec.pourcentage = (score / rec.total_questions) * 100
            else:
                rec.pourcentage = 0

            if rec.pourcentage < 50:
                rec.message = "Oups... Vous ferez mieux au prochain Quiz !"
            else:
                rec.message = "Bravo ! Bon travail 🎉"

    def action_show_result(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Résultat du Quiz',
            'res_model': 'blank.page.resource',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_quiz_result').id, 'form')],
            'res_id': self.id,
            'target': 'current',
        }

