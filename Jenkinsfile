pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Clean Workspace') {
            steps {
                bat '''
                if exist venv rmdir /s /q venv
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                "%PYTHON%" -m venv venv
                '''
            }
        }

        stage('Check Python Version') {
            steps {
                bat '''
                venv\\Scripts\\python.exe --version
                '''
            }
        }

        stage('Upgrade pip tools') {
            steps {
                bat '''
                venv\\Scripts\\python.exe -m pip install --upgrade pip setuptools wheel
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

 stage('Update Odoo modules') {
    steps {
        bat '''
        set PYTHONPATH=C:\\odoo1
        venv\\Scripts\\python.exe C:\\odoo1\\odoo-bin -d odoo_new -u dashboard_recruteur,pfe --stop-after-init
        '''
    }
}

        stage('Restart Odoo') {
            steps {
                bat '''
                net stop odoo
                timeout /t 5
                net start odoo
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Déploiement réussi'
        }

        failure {
            echo '❌ Build échoué'
        }
    }
}