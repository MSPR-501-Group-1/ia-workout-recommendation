pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'mspr-ia-workout-recommendation'
        PYTHON_VERSION    = '3.11'
        IMAGE_NAME        = 'mspr/ia-workout-recommendation'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                '''
            }
        }

        stage('Test & Coverage') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mkdir -p test-results
                    PYTHONPATH=. pytest tests/ \
                        --cov=. \
                        --cov-report=xml:coverage.xml \
                        --cov-report=term-missing \
                        --junitxml=test-results/results.xml \
                        -v
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results/*.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    withEnv(["SONAR_SCANNER_OPTS=-Xmx512m"]) {
                        tool name: 'SonarQube Scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                        script {
                            def scannerHome = tool 'SonarQube Scanner'
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                    -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                                    -Dsonar.sources=. \
                                    -Dsonar.inclusions="**/*.py" \
                                    -Dsonar.exclusions="**/.venv/**,**/tests/**,**/scripts/**" \
                                    -Dsonar.tests=tests \
                                    -Dsonar.python.coverage.reportPaths=coverage.xml \
                                    -Dsonar.python.version=${PYTHON_VERSION}
                            """
                        }
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest ."
            }
        }
    }

    post {
        success {
            echo "Pipeline ia-workout-recommendation : SUCCESS (build #${BUILD_NUMBER})"
        }
        failure {
            echo "Pipeline ia-workout-recommendation : FAILURE (build #${BUILD_NUMBER})"
        }
        always {
            deleteDir()
        }
    }
}
