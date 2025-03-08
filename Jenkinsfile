        stage('Deploy to VPS') {
            agent any
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
