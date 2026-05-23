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
        venv\\Scripts\\python.exe -m pip install numpy
        venv\\Scripts\\python.exe -m pip install pdfminer.six==20221105
        venv\\Scripts\\python.exe -m pip install cryptography==3.4.8 pyOpenSSL==21.0.0 --force-reinstall
        venv\\Scripts\\python.exe -m pip install sentence-transformers torch
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

        sstage('Update Odoo Modules') {
    steps {
        bat '''
        set PYTHONPATH=%ODOO_DIR%

        venv\\Scripts\\python.exe %ODOO_DIR%\\odoo-bin ^
        -d %DB_NAME% ^
        -u pfe ^
        --stop-after-init ^
        --no-http ^
        --max-cron-threads=0

        taskkill /F /IM python.exe /T
        exit 0
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