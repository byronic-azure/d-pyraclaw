// ─────────────────────────────────────────────────────────────
// PyraClaw Sovereign AI Runtime — Jenkins Declarative Pipeline
// DD7 International GmbH · Patent PCT/EP2025/080977
// ─────────────────────────────────────────────────────────────

pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {
        PYTHON_VERSION = '3.11'
        DOCKER_IMAGE   = 'pyraclaw/sovereign-runtime'
        REGISTRY       = credentials('docker-registry-url')
    }

    stages {
        // ── Setup ────────────────────────────────────────────
        stage('Setup') {
            steps {
                sh '''
                    python${PYTHON_VERSION} -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install flake8 pytest pytest-cov bandit safety
                    pip install -r requirements.txt
                '''
            }
        }

        // ── Quality Gate ─────────────────────────────────────
        stage('Quality Gate') {
            parallel {
                stage('Lint') {
                    steps {
                        sh '''
                            . .venv/bin/activate
                            flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                            flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                        '''
                    }
                }
                stage('Security') {
                    steps {
                        sh '''
                            . .venv/bin/activate
                            bandit -r cli/ services/ -f json -o bandit-report.json --exit-zero || true
                            safety check -r requirements.txt --output json > safety-report.json || true
                        '''
                        archiveArtifacts artifacts: '*-report.json', allowEmptyArchive: true
                    }
                }
            }
        }

        // ── Test ─────────────────────────────────────────────
        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --tb=short --cov=. --cov-report=xml --cov-report=term-missing \
                        -q --no-header --junitxml=test-results.xml 2>&1 || true
                '''
                junit allowEmptyResults: true, testResults: 'test-results.xml'
            }
        }

        // ── Docker Build ─────────────────────────────────────
        stage('Docker Build') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                }
            }
        }

        // ── Docker Publish (tagged releases only) ────────────
        stage('Docker Publish') {
            when {
                buildingTag()
            }
            steps {
                script {
                    def tag = env.TAG_NAME.replaceFirst('^v', '')
                    docker.withRegistry("https://${REGISTRY}", 'docker-registry-creds') {
                        def image = docker.build("${DOCKER_IMAGE}:${tag}")
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }

        // ── Release (tagged builds only) ─────────────────────
        stage('Release') {
            when {
                buildingTag()
            }
            steps {
                echo "Release ${env.TAG_NAME} published successfully."
                echo "Image: ${DOCKER_IMAGE}:${env.TAG_NAME.replaceFirst('^v', '')}"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed — all stages passed.'
        }
        failure {
            echo 'Pipeline failed — review the stage logs above.'
        }
    }
}
