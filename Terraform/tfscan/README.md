# **Jenkins**
### 1. Install Terraform Plugins
### 2. COnfigure terraform tool
#### i. In **Manage Jenkins > Global Tool Config > Terraform**
#### ii. Add Terraform.
#### iii. Uncheck the “Install Automatically” check box.
#### iv. Name: Terraform
#### v. Install Directory: /usr/local/bin/
### 3. Jenkinsfile
```
pipeline {
  agent any

  tools {
    terraform 'Terraform'
  }

  stages{
    stage('checkout') {
      steps {
        checkout scm
      }
    }
    stage('terraform') {
      steps {
        dir('terrascan'){
            sh 'terraform init'
        }
      }
    }
  }
}
```
### 4. Install **Docker Pipeline** Plugins