pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        git(url: 'https://github.com/L0G1C06/mlJenkins', branch: 'feat-model')
      }
    }

    stage('Python version') {
      steps {
        sh 'python3 --version'
      }
    }

    stage('Build') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Train') {
      steps {
        sh 'python3 train-lda.py'
      }
    }

  }
}