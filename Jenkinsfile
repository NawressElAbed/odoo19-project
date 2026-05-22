pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                pip install -r requirements.txt
                '''
            }
        }

        stage('Update Odoo modules') {
            steps {
                bat '''
                python odoo-bin -u dashboard_recruteur,pfe -d odoo_new --stop-after-init
                '''
            }
        }

        stage('Restart Odoo') {
            steps {
                bat '''
                net stop odoo
                net start odoo
                '''
            }
        }
    }
}