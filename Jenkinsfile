pipeline {
    agent none

    environment {
        DOCKER_HUB_USER = 'er.joselin@gmail.com'
        IMAGE_NAME = "erjoselin/django-polls"
        DOCKER_HUB_PASSWORD = credentials('docker-hub-credentials')
    }

    stages {
        stage('Clone Repository') {
            agent {
                docker {
                    image 'python:3'
                    args '-u root:root'
                }
            }
            steps {
                git branch: 'master', url: 'https://github.com/joseantoniocgonzalez/django_tutorial'
            }
        }

        stage('Install Dependencies') {
            agent {
                docker {
                    image 'python:3'
                    args '-u root:root'
                }
            }
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            agent {
                docker {
                    image 'python:3'
                    args '-u root:root'
                }
            }
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt  # Asegurar que las dependencias están instaladas en el contenedor de pruebas
                    python3 manage.py test
                '''
            }
        }

        stage('Build and Push Docker Image') {
            agent {
                label 'principal'
            }
            steps {
                script {
                    sh '''
                        docker build -t $IMAGE_NAME .
                        echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USER --password-stdin
                        docker push $IMAGE_NAME
                        docker rmi $IMAGE_NAME
                    '''
                }
            }
        }
    }

    post {
        always {
            mail to: 'er.joselin@gmail.com',
                 subject: "Pipeline Finalizado",
                 body: "El pipeline de Jenkins ha finalizado. Revisa los logs para más detalles."
        }
    }
}
