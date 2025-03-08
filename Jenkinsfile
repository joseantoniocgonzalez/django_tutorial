pipeline {
    agent none

    environment {
        IMAGE_NAME = "joseantoniocgonzalez/django-polls"  // 🔴 Imagen en Docker Hub
        VPS_USER = "jose"  // 🔴 Usuario del VPS
        VPS_HOST = "217.72.207.210"  // 🔴 IP del VPS
        PROJECT_PATH = "/home/jose/app"  // 🔴 Ruta del proyecto en el VPS
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
                    withCredentials([sshUserPrivateKey(credentialsId: 'vps-ssh-credentials', keyFileVariable: 'SSH_KEY')]) {
                        sh '''
                            echo "🔑 Guardando clave SSH temporalmente..."
                            echo "$SSH_KEY" > /tmp/jenkins_ssh_key
                            chmod 600 /tmp/jenkins_ssh_key
                            
                            echo "🚀 Iniciando conexión SSH con el VPS..."
                            ssh -i /tmp/jenkins_ssh_key -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'EOF'
                                echo "✅ Conexión SSH establecida."
                                cd $PROJECT_PATH
                                echo "🛑 Apagando contenedores antiguos..."
                                docker-compose down
                                echo "⬇️ Descargando nueva imagen..."
                                docker pull $IMAGE_NAME
                                echo "🔄 Reiniciando servicio con nueva versión..."
                                docker-compose up -d --build
                                echo "🎉 Despliegue finalizado."
                            EOF
                            
                            echo "🗑️ Eliminando clave SSH temporal..."
                            rm -f /tmp/jenkins_ssh_key
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            mail to: 'er.joselin@gmail.com',
                 subject: "✅ Pipeline Finalizado",
                 body: "El pipeline de Jenkins ha finalizado correctamente. Revisa los logs para más detalles."
        }
    }
}
