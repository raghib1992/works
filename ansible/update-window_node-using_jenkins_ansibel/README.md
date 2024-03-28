## Used tools
1. Artifacttory
2. Playbook
3. Jenkins
4. Ansible


## Step 1: Upload file to artifactory
```sh
curl -v -u sstanley:Sstanley@123# -T dotnet-runtime-8.0.2-win-x64.exe -X PUT https://artifactory.dev.paygateway.com/artifactory/common/aws_jenkins_nodes_on_demand/dotnet-runtime/dotnet-runtime-8.0.2-win-x64.exe

curl -v -u sstanley:Sstanley@123# -T SigningClient-1.1.0.zip -X PUT https://artifactory.dev.paygateway.com/artifactory/common/aws_jenkins_nodes_on_demand/SigningClient/SigningClient-1.1.0.zip
```

## Step 2: Verify the artifacts in artifactory

## Step 3: Open Terraform-Infrastructure bitbucket repo locally in VSC

## Step 4: Create new branch from master 
```sh
git checkout -b REL_GWOPS-14543-update-ondemand-node
```

## Step 5: Create Playbook
```yml
#dotnet_runtime_8.0.2-win-x64.yml
---
- name: dotnet_runtime_8.0.2-win-x64.yml
  hosts: all
  become: false
  tasks:
    - name: download dotnet-runtime-8.0.2-win-x64.exe
      win_get_url:
        url: 'https://itools.dev.paygateway.com:443/artifactory/common/aws_jenkins_nodes_on_demand/dotnet-runtime/dotnet-runtime-8.0.2-win-x64.exe'
        dest: 'C:\Windows\Temp\dotnet-runtime-8.0.2-win-x64.exe'

    - name: install dotnet-runtime-8.0.2-win-x64.exe
      raw: 'C:\Windows\Temp\dotnet-runtime-8.0.2-win-x64.exe /SILENT /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"'
	  
	  
#SigningClient-1.1.0.yml
---
- name: SigningClient-1.1.0.yml
  hosts: all
  become: false
  vars:
    mysrc: 'C:\Work\Temp\SigningClient-1.1.0.zip'
    mydest: 'C:\Work\signing_client\'
  tasks:
    - name: Download SigningClient-1.1.0.zip
      ansible.windows.win_get_url:
        url: https://artifactory.dev.paygateway.com/ui/repos/tree/General/common/aws_jenkins_nodes_on_demand/SigningClient/SigningClient-1.1.0.zip
        dest: "{{ mysrc }}"

    - name: extract SigningClient-1.1.0.zip on C:\
      community.windows.win_unzip:
        src: "{{ mysrc }}"
        dest: "{{ mydest }}" 

    - name: Ensure those variables is present on the global system path, and in the specified order
      ansible.windows.win_path:
        elements:
        - 'C:\Work\signing_client'
```


## Step 6: Update the playbook in variable.groovy file at `terraform-infrastructure\aws\jenkins\jenkins-nodes\nodes\vos1-vos2-label-on-demand\variables.groovy`
```yml
// Define the playbooks (they will run respecting the order)
env.ANSIBLE_PLAYBOOKS = 'windows_defender_remove.yml prepare_partition_e.yml resize_partition_c.yml long_paths_enabled.yml git_2.37.1x64.yml jdk_1.8.0_275.yml microsoft-jdk-11.0.17-windows-x64.yml work_folder.yml 7zip_standalone_2201.yml curl-7.88.1_2-win64-mingw.yml verifone.yml cmake-3.26.0-win64-x64.yml cppcheck-2.11-x64.yml ninja_1.11.1.yml ccache-4.8.2.yml python_39_v2.yml open_ssh_win64_port_22.yml ssh_public_key_config.yml win_scheduled_task_CleanUpJenkinsUser_v2.yml win_scheduled_task_CleanUpWorkspace_v2.yml reboot_windows.yml ccache-4.8.3.yml cmake-3.28.0-win64-x64.yml dotnet_runtime_8.0.2-win-x64.yml SigningClient-1.1.0.yml'
```

## Step 7: Push the changes to remote repo

## Step 8: Run the jenkins pipeline *https://jenkins.dev.paygateway.com/job/jenkins-nodes-constructor1/build?delay=0sec*
- BranchName: REL_GWOPS-14543-update-ondemand-node
- PauseBeforeCreateAMIVersion true
- CREATING_VERSIONED_AMI true

## Step 9: After RunAnsible Stage verify all thing goes ok

## Step 10: approve for next step

## Step 11: Copy AMI version and ID