pipeline {
    agent none

    environment {
        IMAGE_NAME = "joseantoniocgonzalez/django-polls"
        VPS_USER = "jose"
        VPS_HOST = "217.72.207.210"
        PROJECT_PATH = "/home/jose/app"
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
                    pip install -r requirements.txt
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

        stage('Deploy to VPS') {
            agent any
            steps {
                script {
                    sh """
                        echo "🔍 Verificando conexión SSH con $VPS_USER@$VPS_HOST"
                        ssh -i "/var/lib/jenkins/.ssh/id_rsa" -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'EOF'
                            echo "🛠️ Desplegando en el VPS..."
                            cd $PROJECT_PATH
                            docker-compose down
                            docker pull $IMAGE_NAME
                            docker-compose up -d --build
                            echo "✅ Despliegue finalizado correctamente."
EOF
                    """
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
