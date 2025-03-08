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
            agent {
                node {
                    label 'master'
                }
            }
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
            agent {
                node {
                    label 'master'
                }
            }
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'vps-ssh-credentials', keyFileVariable: 'SSH_KEY')]) {
                        sh '''
                            echo "🔍 Verificando conexión SSH con $VPS_USER@$VPS_HOST"
                            ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << EOF
                                echo "🛠️ Desplegando en el VPS..."
                                cd $PROJECT_PATH

                                # 🔍 Verifica si el archivo docker-compose.yaml existe
                                if [ ! -f docker-compose.yaml ]; then
                                    echo "❌ ERROR: No se encontró el archivo docker-compose.yaml en $PROJECT_PATH"
                                    exit 1
                                fi

                                echo "🛑 Deteniendo contenedores antiguos..."
                                docker-compose down

                                echo "🔄 Descargando la nueva imagen..."
                                docker pull $IMAGE_NAME

                                echo "🚀 Iniciando nuevo contenedor..."
                                docker-compose up -d --build

                                echo "✅ Despliegue finalizado correctamente."
                            EOF
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
