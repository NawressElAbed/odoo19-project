from datetime import datetime, timedelta
from odoo import models, fields, api

class BlankPage(models.Model):
    _name = 'blank.page'
    _description = 'Page vide avec quiz'

    name = fields.Char(string="Nom")

    question1 = fields.Selection([
        ('a', 'Il remplace complètement le DOM réel'),
        ('b', 'Il permet de manipuler directement le DOM'),
        ('c', 'Il optimise les mises à jour en comparant les changements'),
        ('d', 'Il stocke les données de l’application'),
    ], string="Q1: En React, que fait réellement le Virtual DOM ?")

    question2 = fields.Selection([
        ('a', 'Il n’y a aucune différence'),
        ('b', 'useEffect est synchrone, useLayoutEffect est asynchrone'),
        ('c', 'useLayoutEffect s’exécute avant le rendu visuel, useEffect après'),
        ('d', 'useEffect est utilisé uniquement pour les API')
    ], string="Q2: Différence entre useEffect et useLayoutEffect ?")

    question3 = fields.Selection([
        ('a', 'Les opérations sont exécutées une par une'),
        ('b', 'Le code est exécuté uniquement de façon synchrone'),
        ('c', 'Les opérations n’arrêtent pas l’exécution du programme'),
        ('d', 'Node.js ne peut pas gérer plusieurs requêtes')
    ], string="Q3: Que signifie non-blocking I/O en Node.js ?")

    question4 = fields.Selection([
        ('a', 'Utiliser uniquement HTTP'),
        ('b', 'Ajouter des commentaires dans le code'),
        ('c', 'Utiliser HTTPS + authentification (JWT/OAuth)'),
        ('d', 'Cacher les routes')
    ], string="Q4: Bonne pratique pour sécuriser une API REST ?")

    question5 = fields.Selection([
        ('a', 'Une erreur serveur'),
        ('b', 'Une politique de sécurité entre domaines différents'),
        ('c', 'Un framework JavaScript'),
        ('d', 'Une base de données')
    ], string="Q5: Que signifie CORS ?")

    question6 = fields.Selection([
        ('a', 'Aucune différence'),
        ('b', '== compare les valeurs uniquement, === compare valeur + type'),
        ('c', '=== est plus lent'),
        ('d', '== est utilisé uniquement en React')
    ], string="Q6: Différence entre == et === en JavaScript ?")

    def action_open_quiz_page2(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quiz - Page 2 (2/2)',
            'res_model': 'blank.page',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_blank_page_form_page2').id, 'form')],
            'target': 'current',
            'res_id': self.id,
        }

    def action_back_to_quiz_page1(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quiz - Page 1 (1/2)',
            'res_model': 'blank.page',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_blank_page_form_page1').id, 'form')],
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
            if rec.question1 == 'c': score += 1
            if rec.question2 == 'c': score += 1
            if rec.question3 == 'c': score += 1
            if rec.question4 == 'c': score += 1
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
            'res_model': 'blank.page',
            'view_mode': 'form',
            'views': [(self.env.ref('dashboard_recruteur.view_quiz_result').id, 'form')],
            'res_id': self.id,
            'target': 'current',
        }
