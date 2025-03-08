pipeline {
    agent none

    environment {
        IMAGE_NAME = "joseantoniocgonzalez/django-polls"  // 🔴 Asegúrate de que el nombre de la imagen es correcto
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
            agent any
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                        sh '''
                            docker build -t $IMAGE_NAME .
                            echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USER" --password-stdin
                            docker push $IMAGE_NAME
                            docker rmi $IMAGE_NAME
                        '''
                    }
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
