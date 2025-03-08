pipeline {
    agent none

    environment {
        IMAGE_NAME = "joseantoniocgonzalez/django-polls"  // Nombre de la imagen en Docker Hub
        VPS_USER = "jose"  // Usuario correcto del VPS
        VPS_HOST = "217.72.207.210"  // IP del VPS
        PROJECT_PATH = "/home/jose/app"  // Ruta donde está el docker-compose en el VPS
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
                            echo "🔨 Construyendo la imagen Docker..."
                            docker build -t $IMAGE_NAME .

                            echo "🔐 Iniciando sesión en Docker Hub..."
                            echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USER" --password-stdin

                            echo "📤 Subiendo la imagen a Docker Hub..."
                            docker push $IMAGE_NAME

                            echo "🗑️ Eliminando la imagen local para liberar espacio..."
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
                            echo "🔍 Verificando SSH: Intentando conectar con usuario: $VPS_USER@$VPS_HOST"
                            echo "🔑 Clave SSH usada por Jenkins: $SSH_KEY"

                            echo "🔍 Verificando si la clave SSH existe en Jenkins..."
                            if [ ! -f "$SSH_KEY" ]; then
                                echo "❌ ERROR: No se encontró la clave SSH en Jenkins"
                                exit 1
                            fi
                            echo "✅ Clave SSH encontrada en Jenkins"

                            echo "🚀 Iniciando conexión SSH al VPS..."
                            ssh -vvv -i $SSH_KEY -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << EOF
                                echo "✅ Conexión SSH exitosa con el usuario: \$(whoami)"

                                cd $PROJECT_PATH
                                echo "🛑 Deteniendo contenedor existente..."
                                docker-compose down

                                echo "📥 Descargando la última imagen desde Docker Hub..."
                                docker pull $IMAGE_NAME

                                echo "🚀 Levantando el nuevo contenedor..."
                                docker-compose up -d --build

                                echo "✅ Despliegue finalizado en el VPS."
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
                 subject: "✅ Pipeline Finalizado con Éxito",
                 body: "El pipeline de Jenkins ha finalizado correctamente. Revisa los logs para más detalles."
        }
    }
}

