from odoo import models, fields, api

class BlankPageMobile(models.Model):
    _name = 'blank.page.mobile'
    _description = 'Page vide avec quiz'

    name = fields.Char(string="Nom")

    question1 = fields.Selection([
        ('a', 'Activity est utilisée uniquement pour le backend'),
        ('b', 'Fragment est dépendant d’une Activity'),
        ('c', 'Fragment remplace complètement Activity'),
        ('d', 'Activity est plus légère que Fragment'),
    ], string="Q1: Quelle est la différence principale entre Activity et Fragment en Android ?")

    question2 = fields.Selection([
        ('a', 'La durée de vie de l’application'),
        ('b', 'Les états par lesquels passe une Activity (onCreate, onStart, etc.)'),
        ('c', 'La gestion du réseau'),
        ('d', 'La gestion des bases de données')
    ], string="Q2: Dans Android, que signifie le cycle de vie (Lifecycle) d’une Activity ?")

    question3 = fields.Selection([
        ('a', 'Stocke des données côté serveur'),
        ('b', 'Gère l’état local et déclenche le rafraîchissement de la vue'),
        ('c', 'Remplace UIKit'),
        ('d', 'Sert uniquement pour les animations')
    ], string="Q3: En SwiftUI, que fait @State ?")

    question4 = fields.Selection([
        ('a', 'Aucune différence'),
        ('b', 'async/await rend le code asynchrone plus lisible'),
        ('c', 'Les callbacks sont plus modernes'),
        ('d', 'async/await est synchrone')
    ], string="Q4: Quelle est la différence entre async/await et les callbacks ?")

    question5 = fields.Selection([
        ('a', 'Un composant visuel ou structurel de l’UI'),
        ('b', 'Une base de données'),
        ('c', 'Une API REST'),
        ('d', 'Un thread')
    ], string="Q5: En Flutter, que signifie “Widget” ?")

    question6 = fields.Selection([
        ('a', 'Charger toutes les données au démarrage'),
        ('b', 'Utiliser le lazy loading'),
        ('c', 'Ne jamais utiliser le cache'),
        ('d', 'Mettre toutes les images en haute résolution')
    ], string="Q6: Quelle est une bonne pratique pour optimiser les performances d’une application mobile ?")

    def action_open_quiz_page2_mobile(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quiz - Page 2 (2/2)',
            'res_model': 'blank.page.mobile',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_blank_page_form_page2_mobile').id, 'form')],
            'target': 'current',
            'res_id': self.id,
        }

    def action_back_to_quiz_page1_mobile(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quiz - Page 1 (1/2)',
            'res_model': 'blank.page.mobile',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_blank_page_form_page1_mobile').id, 'form')],
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
            if rec.question5 == 'a': score += 1
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
            'res_model': 'blank.page.mobile',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_quiz_result').id, 'form')],
            'res_id': self.id,
            'target': 'current',
        }

