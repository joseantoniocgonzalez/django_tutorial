pipeline {
    agent none

    environment {
        DOCKER_HUB_USER = 'er.joselin@gmail.com'
        IMAGE_NAME = "erjoselin/django-polls"  // Ajusta el nombre de la imagen si es necesario
        DOCKER_HUB_PASSWORD = credentials('docker-hub-credentials') // Usa la credencial de Jenkins
    }

    stages {
        stage('Clone') {
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
                sh 'pip install -r requirements.txt'
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
                sh 'python3 manage.py test'
            }
        }

        stage('Build and Push Docker Image') {
            agent {
                label 'jenkins-node'
            }
            steps {
                script {
                    sh '''
                        # Construir la imagen Docker
                        docker build -t $IMAGE_NAME .

                        # Iniciar sesión en Docker Hub de manera segura
                        echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USER --password-stdin

                        # Subir la imagen
                        docker push $IMAGE_NAME

                        # Eliminar la imagen local después de subirla
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
