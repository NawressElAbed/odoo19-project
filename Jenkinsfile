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

        stage('Update Odoo Modules') {
            steps {
                bat '''
                set PYTHONPATH=%ODOO_DIR%

                venv\\Scripts\\python.exe %ODOO_DIR%\\odoo-bin ^
                -d %DB_NAME% ^
                -u pfe ^
                --stop-after-init ^
                --no-http ^
                --max-cron-threads=0
                '''
            }
        }

       stage('Restart Odoo (Safe)') {
    steps {
        bat '''
        echo Restart Odoo safely...

        REM Kill only Odoo process
        wmic process where "commandline like '%%odoo-bin%%'" delete

        REM Jenkins-safe sleep (5 sec)
        ping 127.0.0.1 -n 6 > nul

        REM Restart Odoo
        start "" venv\\Scripts\\python.exe C:\\odoo1\\odoo-bin -c C:\\odoo1\\odoo.conf
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