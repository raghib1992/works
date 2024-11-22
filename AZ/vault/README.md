step1: Create secret in vault
Step2: Create secret in github to login into vault VAULT_PASSWORD VAULT_USERNAME
Step3: Create Workflow to fetch secret from vault created in step 1

```
name: Fetch Secret from vault

on:
    workflow_dispatch:

env:
  ## Sets environment variable for internet access
  http_proxy: http://azpse.astrazeneca.net:9480
  https_proxy: http://azpse.astrazeneca.net:9480
  no_proxy: 10.0.0.0/8,172.29.0.0/8,astrazeneca.net

jobs:
    login_vault:
        runs-on:
            - self-hosted
            - azimuth
        steps:
            - name: Setup
              run: echo "Working"  
            
            - name: Set APT Proxy Configuration
              run: |
                echo "Acquire::http::proxy \"${{ env.http_proxy }}\";" | sudo tee -a /etc/apt/apt.conf
                echo "Acquire::https::proxy \"${{ env.https_proxy }}\";" | sudo tee -a /etc/apt/apt.conf
                echo "Acquire::ftp::proxy \"${{ env.http_proxy }}\";" | sudo tee -a /etc/apt/apt.conf
                echo "Acquire::http::proxy::no_proxy \"${{ env.no_proxy }}\";" | sudo tee -a /etc/apt/apt.con

            - name: Set up Vault CLI
              run: |
                curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
                echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
                sudo apt-get update && sudo apt-get install vault 
                #libcap-dev
                # setcap -r /usr/bin/vault

            # - name: Fetch Secret via API
            #   env:
            #     VAULT_ADDR: https://vault.cna.astrazeneca.net
            #     USERNAME: ${{ secrets.VAULT_USERNAME }}
            #     PASSWORD: ${{ secrets.VAULT_PASSWORD }}
            #   run: |
            #     SECRET=$(curl -u "$USERNAME:$PASSWORD" \
            #     $VAULT_ADDR/secrets/aiops/dev/rabbitmq | jq -r '.password')
            #     echo "SECRET=$SECRET" >> $GITHUB_ENV
        
            # - name: Use Secret
            #   run: echo "The fetched secret is ${{ env.SECRET }}"
            
            - name: Vault login
              uses: hashicorp/vault-action@v2
              id: secret
              with:
                url: ${{ env.VAULT_ADDR }}
                method: userpass
                username: ${{ secrets.VAULT_USERNAME }}
                password: ${{ secrets.VAULT_PASSWORD }}
                secrets: |
                    aiops/data/dev/rabbitmq password
              env:
                VAULT_ADDR: https://vault.cna.astrazeneca.net
            
            - name: Sensitive Operation
              run: "echo '${{ steps.secret.outputs.password }}'"
            # - name: Sensitive Operation
            #   run: "my-cli --token '${{ steps.secrets.outputs.VAULT_PASS }}'"

            # - name: Use Secret
            #   run: echo "The secret value is ${{ env.VAULT_PASSWORD }}"

            # - name: Fetch Secret from Vault
            #   env:
            #     VAULT_ADDR: https://vault.cna.astrazeneca.net
            #   run: |
            #     SECRET=$(vault kv get -field=data secret/dev/rabbitmq | jq -r .password)
            #     echo "SECRET=$SECRET"

```