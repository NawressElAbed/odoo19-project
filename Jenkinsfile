pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
        ODOO_DIR = "C:\\odoo1"
        VENV_DIR = "venv"
        DB_NAME = "odoo_new"
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

        stage('Upgrade pip') {
            steps {
                bat '''
                venv\\Scripts\\python.exe -m pip install --upgrade pip setuptools wheel
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Install Extra Odoo deps') {
            steps {
                bat '''
                venv\\Scripts\\python.exe -m pip install numpy pdfminer.six
                '''
            }
        }

        stage('Check Odoo Startup') {
            steps {
                bat '''
                venv\\Scripts\\python.exe %ODOO_DIR%\\odoo-bin --version
                '''
            }
        }

        stage('Update Odoo Modules') {
            steps {
                bat '''
                set PYTHONPATH=%ODOO_DIR%

                venv\\Scripts\\python.exe %ODOO_DIR%\\odoo-bin ^
                -d %DB_NAME% ^
                -u dashboard_recruteur,pfe ^
                --addons-path=%ODOO_DIR%\\addons;%WORKSPACE%\\addons ^
                --stop-after-init
                '''
            }
        }

        stage('Restart Odoo Service') {
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
            echo "✅ Déploiement Odoo réussi"
        }

        failure {
            echo "❌ Échec du pipeline Odoo"
        }
    }
}