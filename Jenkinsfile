pipeline {
    agent any

    parameters {
        choice(
            name: 'MAKE_TARGET',
            choices: [
                'test-all',
                'test-verbose',
                'test-admin',
                'test-instructor',
                'test-admin-quiz',
                'test-admin-user',
                'test-quiz-list-all',
                'test-quiz-add',
                'test-quiz-add-delete',
                'test-quiz-add-edit',
                'test-quiz-del',
                'test-quiz-search',
                'test-quiz-preview',
                'test-quiz-submission',
                'test-group-add',
                'test-group-del',
                'test-group-edit',
                'test-score-edit',
                'test-smoke',
                'test-lesson-delete',
                'test-add-assignment',
                'test-delete-assignment'
            ],
            description: 'Pilih Makefile target yang akan dijalankan'
        )

        booleanParam(
            name: 'REBUILD_IMAGE',
            defaultValue: false,
            description: 'Rebuild docker image sebelum run'
        )
    }

    environment {
        COMPOSE_PROJECT_NAME = "vts-ui-test"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            when {
                expression { params.REBUILD_IMAGE }
            }
            steps {
                sh '''
                  docker compose build vts-ui-test
                '''
            }
        }

        stage('Run UI Test') {
            steps {
                sh """
                  docker compose run --rm \
                    vts-ui-test \
                    make ${params.MAKE_TARGET}
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.html', fingerprint: true
        }
        failure {
            echo '❌ UI Test FAILED'
        }
        success {
            echo '✅ UI Test PASSED'
        }
        cleanup {
            sh 'docker compose down -v || true'
        }
    }
}
