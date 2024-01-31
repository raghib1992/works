#!groovy

import groovy.time.TimeCategory 
import groovy.time.TimeDuration

env.BranchName = env.BranchName.trim()
currentBuild.displayName = "${BUILD_NUMBER}-${env.BranchName}-${BUILD_USER}"

def runId = UUID.randomUUID().toString()
print "JenkinsPipelineRunId = ${runId}"

node("TEF") {

  deleteDir()
  print "Building in ${env.WORKSPACE} workspace on ${env.NODE_NAME} Node"
  def DBHost
  if (!env.RelEngBranch) {
    print "${env.RelEngBranch} parameter doesn't exist; Defaulting it to master"
    env.RelEngBranch = 'master'
  }

  try {
    stage ("Checkout rel-eng") {
      def s1runId = UUID.randomUUID().toString()
      print "CodeCheckoutRunId = ${s1runId}"
      dir ("rel-eng") {
        checkout([$class: 'GitSCM', branches: [[name: "origin/${env.RelEngBranch}"]], extensions: [[$class: 'CloneOption', depth: 1, noTags: true, shallow: true]], userRemoteConfigs: [[credentialsId: 'Gitlab_Jenkins', url: 'https://gitlab.dev.paygateway.com/cayan/rel-eng.git']]])
        def gitCommit = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
        def gitBranch = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()

        print "rel-eng branch = ${gitBranch}; commit = ${gitCommit}"
      }
      print  "CodeCheckoutRunId = ${s1runId}"
    }

    def cayanCommon
    String featureTeamName,splitJobNum,hostNameApp,hostNameDb,hostNameTef,vmNameApp,vmNameDb,vmNameTef
    int pipelineNum

    stage ("Load libraries / variables") {
      def s2runId = UUID.randomUUID().toString()
      print "LoadLibrariesRunId = ${s2runId}"
      print "Loading CayanCommon.groovy"
      cayanCommon = load ("rel-eng/deploy_scripts/cayan-main/groovy/CayanCommon.groovy")

      // Sets all env variables and overrides to correct values
      print "Loading JenkinsCDEnv.groovy"
      load ("rel-eng/jenkins/JenkinsCDEnv.groovy")
      cayanCommon.SetTefExtraConfig(env.JOB_BASE_NAME)

      env.BuildPattern = cayanCommon.GetBuildPattern(env.BranchName)
      featureTeamName = env.JOB_BASE_NAME.split('_')[0]
      splitJobNum = env.JOB_BASE_NAME.split('_')[2]
      pipelineNum = splitJobNum.isInteger() ? splitJobNum.toInteger() : null

      // check if job name have _env_ in the middle
      def secNameBasePart = "${env.JOB_BASE_NAME.split('_')[1]}"
      def hostNameBase = ''
      if (secNameBasePart == "env") {
        // take the first part as a VM base name
        hostNameBase = "${env.JOB_BASE_NAME.split('_')[0]}-e${splitJobNum}"
      } else {
        // take the second part as a VM base name
        hostNameBase = "${env.JOB_BASE_NAME.split('_')[1]}-e${splitJobNum}"
      }

      def vmNameBase = "${env.JOB_BASE_NAME}"
      (hostNameApp,hostNameDb,hostNameTef) = ["${hostNameBase}-app","${hostNameBase}-db","${hostNameBase}-tef"]
      (vmNameApp,vmNameDb,vmNameTef) = ["${vmNameBase}_application","${vmNameBase}_db_mocks","${vmNameBase}_tef_runner"]
      env.Group = cayanCommon.SetEnvGroupVars(featureTeamName)
      
      powershell """
        Write-Host 'Job Parameters:'
        Write-Host 'BuildPattern = ${env.BuildPattern}'
        Write-Host 'Provision App Server = ${env.ProvisionApp}'
        Write-Host 'Provision Db Server = ${env.ProvisionDb}'
        Write-Host 'Provision TEF Server = ${env.ProvisionTef}'
        Write-Host 'InstallBurp = ${env.InstallBurp}'
        Write-Host 'RunPtf = ${env.RunPtf}'
        Write-Host 'RunTef = ${env.RunTef}'
		    Write-Host 'RunPerf = ${env.RunPerf}'
        Write-Host 'VerifyPerformanceTests = ${env.VerifyPerformanceTests}'
        Write-Host 'IncludeTags = ${env.IncludeTags}'
        Write-Host 'ExcludeTags = ${env.ExcludeTags}'
        Write-Host 'CustomArgument = ${env.CustomArgument}'

        Write-Host 'VM / Host Information:'
        Write-Host 'App HostName = ${hostNameApp}'
        Write-Host 'DB HostName = ${hostNameDb}'
        Write-Host 'TEF HostName = ${hostNameTef}'
        Write-Host 'App VM Name = ${vmNameApp}'
        Write-Host 'DB VM Name = ${vmNameDb}'
        Write-Host 'TEF VM Name = ${vmNameTef}'
        Write-Host 'Group = ${env.Group}'

        Write-Host 'Environment-specific Variables:'
        Write-Host 'DNS Server is: ${env.DnsServer}'
        Write-Host 'DnsJumpServer is: ${env.DnsJumpServer}'
        Write-Host 'SplunkDeploymentServer is: ${env.SplunkDeploymentServer}'
        Write-Host 'StaticIpSqlServer is: ${env.StaticIpSqlServer}'
        Write-Host 'AppHostMappings is: ${env.AppHostMappings}'
        Write-Host 'LongDomain is: ${env.longDomain}'
        Write-Host 'OUPath is: ${env.OUPath}'
        Write-Host 'vLanId is: ${env.vLanId}'
        Write-Host 'VirtualNetwork is: ${env.virtualNetwork}'
        Write-Host 'IpAddress is: ${env.IpAddress}'
        Write-Host 'Subnet is: ${env.Subnet}'
        Write-Host 'DefaultGateway is: ${env.DefaultGateway}'
        Write-Host 'DnsServers is: ${env.DnsServers}'
        Write-Host 'ParallelSlots is: ${env.ParallelSlots}'
        Write-Host 'TestTypes is: ${env.TestTypes}'
        Write-Host 'BuildConfigurations is: ${env.BuildConfigurations}'
        Write-Host 'StandardWebDriverPoolSize is: ${env.StandardWebDriverPoolSize}'
        Write-Host 'MobileWebDriverPoolSize is: ${MobileWebDriverPoolSize}'
        Write-Host 'ChefRunList is: ${env.chefRunList}'
        Write-Host 'DscList is: ${env.DscList}'
        Write-Host 'AcceptInProgress is: ${env.AcceptInProgress}'
        Write-Host 'MigrationStrategies is: ${env.MigrationStrategies}'
        Write-Host 'DbEnvironment is: ${env.DbEnvironment}'
        Write-Host 'ChefEnvironment is: ${env.chefEnvironment}'
        Write-Host 'AppParentName is: ${env.AppParentName}'
        Write-Host 'DbParentName is: ${env.DbParentName}'
        Write-Host 'TefParentName is: ${env.TefParentName}'
        Write-Host 'InfoLog is: ${env.InfoLog}'
        Write-Host 'CommonBuildPattern is: ${env.CommonBuildPattern}'
        Write-Host 'TemplateVersion is: ${env.TemplateVersion}'
        Write-Host 'SophosVersion is: ${env.SophosVersion}'
        Write-Host 'OpenSshVersion is: ${env.OpenSshVersion}'
        Write-Host 'SecretServerUrl is: ${env.SecretServerUrl}'
        Write-Host 'SecretServerDomain is: ${env.SecretServerDomain}'
      """
        print "LoadLibrariesRunId = ${s2runId}"
    }

    // stage ("Download cayan-main bundle") {
    //   powershell """
    //     Import-Module -Path '.\\rel-eng\\deploy_scripts\\common\\Artifactory.psm1' -Force

    //     Invoke-DownloadArtifact -BuildPattern ${env:buildPattern} -Destination 
    //   """
    // }

    stage ("Creating VMs") {
      def s3runId = UUID.randomUUID().toString()
      print "CreatingVMRunId = ${s3runId}"
      withCredentials([
        [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
        [$class: 'UsernamePasswordMultiBinding', credentialsId: 'relEngSqlId', usernameVariable: 'RelEngSqlUserName', passwordVariable: 'RelEngSqlPassword'],
        [$class: 'UsernamePasswordMultiBinding', credentialsId: 'jenkins_svc_dev', usernameVariable: 'DomainUserNameDev', passwordVariable: 'DomainUserPasswordDev']
      ]) {
        try {
		  def staticIps = [:]
          parallel (
            "${hostNameApp} VM" : {
              if (env.ProvisionApp == "true") {
                def retryAttempt = 0
                retry(2) {
                  if (retryAttempt > 0) {
                    sleep time: 1, unit: 'MINUTES'
                  }
                  retryAttempt = retryAttempt + 1
                  powershell """
                    .\\rel-eng\\jenkins\\CreateVm.ps1 `
                    -HostName '${hostNameApp}' `
                    -BaseVmName '${vmNameApp}' `
                    -ParentType 'Application'
                  """
                }
				staticIps[hostNameApp] = readFile("IP-${hostNameApp}.txt")
              }
            },
            "${hostNameDb} VM" : {
              if (env.ProvisionDb == "true") {
                def retryAttempt = 0
                retry(2) {
                  if (retryAttempt > 0) {
                    sleep time: 1, unit: 'MINUTES'
                  }
                  retryAttempt = retryAttempt + 1
                  powershell """
                    .\\rel-eng\\jenkins\\CreateVm.ps1 `
                    -HostName '${hostNameDb}' `
                    -BaseVmName '${vmNameDb}' `
                    -ParentType 'DB'
                  """
                }
				staticIps[hostNameDb] = readFile("IP-${hostNameDb}.txt")
        DBHost = staticIps[hostNameDb]
              }
            },
            "${hostNameTef} VM" : {
              if (env.ProvisionTef == "true") {
                def retryAttempt = 0
                retry(2) {
                  if (retryAttempt > 0) {
                    sleep time: 1, unit: 'MINUTES'
                  }
                  retryAttempt = retryAttempt + 1
                  powershell """
                    .\\rel-eng\\jenkins\\CreateVm.ps1 `
                    -HostName '${hostNameTef}' `
                    -BaseVmName '${vmNameTef}' `
                    -ParentType 'TEF'
                  """
                }
				staticIps[hostNameTef] = readFile("IP-${hostNameTef}.txt")
              }
            }
          )
		  def ipHtml = staticIps.sort().inject("<h3>VM IP Addresses</h3><table>\n") {html, kv ->
                         html += "<tr><th>${kv.getKey()}</th><td>${kv.getValue()}</td></tr>\n"
                         html
                       } + "</table>"
		  rtp nullAction: '1', parserName: 'HTML', stableText: ipHtml
        } catch (e) {
          dir(env.WORKSPACE) {
            deleteDir()
          }

          currentBuild.result = "FAILURE"
          print "Status After VM creation: Failure"

          def subject = "${env.JOB_BASE_NAME} job failed at VM creation"
          def details = """<p>Failed at VM creation</p>"""
          def emailprefix = "REL"
          cayanCommon.SendEmail(details, subject, emailprefix)

          throw e
        }
      }
       print "CreatingVMRunId = ${s3runId}"
    }

    stage ("Provisioning VMs") {
      def s4runId = UUID.randomUUID().toString()
      print "ProvisioningVMRunId = ${s4runId}"
      parallel (
        "${hostNameApp} VM" : {
          withCredentials([
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'MISecretServerId', usernameVariable: 'SecretServerUserName', passwordVariable: 'SecretServerPassword'],
	   [$class: 'UsernamePasswordMultiBinding', credentialsId: 'jenkins_svc_dev', usernameVariable: 'DomainUserNameDev', passwordVariable: 'DomainUserPasswordDev']
          ]) {
            if (env.ProvisionApp == "true") {
              powershell """
                .\\rel-eng\\jenkins\\DeployApp.ps1 `
                -BaseVmName '${vmNameApp}'
              """
            }
          }
        },
        "${hostNameDb} VM" : {
          withCredentials([
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'devSqlId', usernameVariable: 'DevSqlUserName', passwordVariable: 'DevSqlPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'devAdminSqlId', usernameVariable: 'DevSaSqlUserName', passwordVariable: 'DevSaSqlPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'MISecretServerId', usernameVariable: 'SecretServerUserName', passwordVariable: 'SecretServerPassword'],
	          [$class: 'UsernamePasswordMultiBinding', credentialsId: 'jenkins_svc_dev', usernameVariable: 'DomainUserNameDev', passwordVariable: 'DomainUserPasswordDev'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'paygateway_ssl_secret', usernameVariable: 'sslCertUser', passwordVariable: 'sslCertPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'devMSSQLOwnerConfigID', usernameVariable: 'DevMSSQLOwnerUserName', passwordVariable: 'DevMSSQLOwnerPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'devMSSQLAgentConfigID', usernameVariable: 'DevMSSQLAgentUserName', passwordVariable: 'DevMSSQLAgentPassword']
          ]) 
          {
              if (env.ProvisionDb == "true") {
                powershell """
                  .\\rel-eng\\jenkins\\DeployDB.ps1 `
                  -BaseVmName '${vmNameDb}' `
                  -AcceptInProgress:\$${AcceptInProgress} `
                  -InfoLog:\$${InfoLog};              
                  .\\rel-eng\\jenkins\\DeployMock.ps1 `
		      -DBBaseVmName '${vmNameDb}';
                  .\\rel-eng\\jenkins\\SplunkForwarder.ps1 `
		      -HostName '${vmNameDb}';
                """
                def DBExitCode = readFile(".\\rel-eng\\jenkins\\DBExitCode.txt").trim()
                if (DBExitCode.contains('0')) {
                  currentBuild.result = 'SUCCESS'
                  def versionProps = readFile("${WORKSPACE}\\version.txt").split("\n").inject([:]){result, line ->
                                  def kv = line.split("=")
                                  result[kv[0]] = kv[1]
                                  result
                              }
                  branch = versionProps["Branch"]
                  commit = versionProps["Commit"].substring(0, 8)
                  def versionHtml = """<h3>Version Info</h3><table>
                  <tr><th>Git</th><td><a href=\"https://gitlab.dev.paygateway.com/cayan/cayan-main/commits/${branch}#commit-${commit}\">${branch} @ ${commit}</a></td></tr>
                  <tr><th>Version</th><td>${versionProps['Version']}</td></tr>
                  </table>"""
                  rtp nullAction: '1', parserName: 'HTML', stableText: versionHtml                   
                } else {
                    currentBuild.result = 'FAILURE'
                    print "Status After DB deployment: Failure"
                    sh 'exit 1'
                }                     
              }             
            }
        },
        "${hostNameTef} VM" : {
          withCredentials([
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'MISecretServerId', usernameVariable: 'SecretServerUserName', passwordVariable: 'SecretServerPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'BurpId', usernameVariable: 'BurpUserName', passwordVariable: 'BurpPassword'],
	    [$class: 'UsernamePasswordMultiBinding', credentialsId: 'jenkins_svc_dev', usernameVariable: 'DomainUserNameDev', passwordVariable: 'DomainUserPasswordDev']
          ]) {
            if (env.ProvisionTef == "true") {
              powershell """
                .\\rel-eng\\jenkins\\DeployWebDriverService.ps1 `
                -TEFBaseVmName '${vmNameTef}';
                .\\rel-eng\\jenkins\\BurpSuite.ps1 `
                -BaseVmName '${vmNameTef}' `
                -InstallBurp \$${env.InstallBurp};
		.\\rel-eng\\jenkins\\SplunkForwarder.ps1 `
		    -HostName '${vmNameTef}';
              """
            }
          }
        }
      )
     print "ProvisioningVMRunId = ${s4runId}"  
    }

    stage("Binding VMs") {
      def s5runId = UUID.randomUUID().toString()
      print "BindingVMRunId = ${s5runId}"
      withCredentials([
        [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
        [$class: 'UsernamePasswordMultiBinding', credentialsId: 'jenkins_svc_dev', usernameVariable: 'DomainUserNameDev', passwordVariable: 'DomainUserPasswordDev']
      ]) {
        if (env.ProvisionApp == "true" || env.ProvisionDb == "true" || env.ProvisionTef == "true") {
          powershell """
            .\\rel-eng\\jenkins\\BindVMs.ps1 `
            -BaseVmName '${vmNameApp}' `
            -DbBaseVmName '${vmNameDb}' `
            -TEFVmName '${vmNameTef}';
          """
        }
      }
      print "BindingVMRunId = ${s5runId}"
    }

    stage ("Post-Binding Provisioning VMs") {
      def s6runId = UUID.randomUUID().toString()
      print "PostBindingProvisioningVMRunId = ${s6runId}"
      print "${env.JOB_BASE_NAME}"
      parallel (
        "${hostNameApp} VM" : {
          withCredentials([
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword']
          ]) {
            if (env.ProvisionApp == "true") {
              powershell """
                .\\rel-eng\\jenkins\\PostDeploy.ps1 `
                -BaseVmName '${vmNameApp}';
              """
              if (env.JOB_BASE_NAME == "rel_env_1"){
               powershell """
                .\\rel-eng\\deploy_scripts\\cayan-main\\ApigeeMicConfigure.ps1 `
                -VmName ${vmNameApp} `
                -QaDnsName '${env.QaDnsName}' `
                -QaMasterServer '${env.QaMasterServer}';
              """
              }
            }
          }
        },
		"${hostNameApp} VM Email" : {
		
		withCredentials([
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'relEngSqlId', usernameVariable: 'RelEngSqlUserName', passwordVariable: 'RelEngSqlPassword']
          ]) {
				powershell """
				.\\rel-eng\\deploy_scripts\\parent\\FixSmtpForDte.ps1 `
				-BaseVmName '${vmNameApp}';
				"""
			}
		},
        "${hostNameTef} VM" : {
          withCredentials([
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'MISecretServerId', usernameVariable: 'SecretServerUserName', passwordVariable: 'SecretServerPassword']
          ]) {
            if (env.ProvisionTef == "true") {
              powershell """
                .\\rel-eng\\jenkins\\DeployOpenSsh.ps1 `
                -TEFBaseVmName '${vmNameTef}' `
                -BaseVmName '${vmNameApp}';
              """
            }
          }
        }
      )
     print "PostBindingProvisioningVMRunId = ${s6runId}"
    }

    def wsdlSubject = "No WSDL MisMatch!!"
    stage("WSDL Check App VM") {
      def s7runId = UUID.randomUUID().toString()
      print "WSDLCheckAppVMRunId = ${s7runId}"
      try {
        powershell """
          .\\rel-eng\\jenkins\\VerifyWsdl.ps1 `
          -BaseVmName '${vmNameApp}';
        """
      } catch (e) {
        print "Failure: WSDL mismatch"
        wsdlSubject = "WSDL Mismatch!!"
        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
        sh "exit 1"
        }
      } finally {
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: "${WORKSPACE}\\.rwc\\cayan-main\\deployment\\wsdl", reportFiles: 'wsdlReport.html', reportName: "WSDL Results"])
      }
      print "WSDLCheckAppVMRunId = ${s7runId}"
    }

	if(env.RunPerf == "true") {
    try {
		  stage("Configuring Locust on ${hostNameTef}") {
        def s8runId = UUID.randomUUID().toString()
        DBHost = DBHost.trim();
        print "ConfiguringLocustRunId = ${s8runId}"
        timeout(time: 1, unit: 'HOURS') {
          withCredentials([
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'relEngSqlId', usernameVariable: 'RelEngSqlUserName', passwordVariable: 'RelEngSqlPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'devSqlId', usernameVariable: 'DevSqlUserName', passwordVariable: 'DevSqlPassword'],
            [$class: 'UsernamePasswordMultiBinding', credentialsId: 'devSqlId2', usernameVariable: 'DevSqlUserName2', passwordVariable: 'DevSqlPassword2']
          ]) {
          
            powershell """
              .\\rel-eng\\deploy_scripts\\cayan-main\\PrimeForLocust.ps1 `
              -locustServerName '${vmNameTef}';
            """          
            parallel (
              "${hostNameTef} Install Python and Locust" : {
              powershell """
                .\\rel-eng\\deploy_scripts\\perf\\InstallLocust.ps1 `
                -TEFBaseVmName '${vmNameTef}';
              """
              },
              "${hostNameTef} Install Locust Services" : {
                powershell """
                  .\\rel-eng\\deploy_scripts\\perf\\InstallLocustServices.ps1 `
                  -TEFBaseVmName '${vmNameTef}';
                """
              },
              "${vmNameApp} Install Locust Services" : {
                powershell """
                  .\\rel-eng\\deploy_scripts\\perf\\InstallLocustAppServices.ps1 `
                  -AppBaseVmName '${vmNameApp}' `
                  -SqlFqdn '${DBHost}' `
                  -SqlUserName '${DevSqlUserName}' `
                  -SqlPassword '${DevSqlPassword}' `
                  -SqlUserName2 '${DevSqlUserName2}' `
                  -SqlPassword2 '${DevSqlPassword2}'; 
                """
              },
              "${hostNameTef} Install Genius Python Modules" : {
                powershell """
                  .\\rel-eng\\deploy_scripts\\perf\\InstallGeniusPythonModules.ps1 `
                  -TEFBaseVmName '${vmNameTef}' `
                  -CayanMainBranch '${env.BranchName}';
                """
              }				  
            ) 							
          }
        } // timeout end
        print "ConfiguringLocustRunId = ${s8runId}"
      }
    } catch (e) {
      currentBuild.result = "FAILURE"
      print "Status ${env.JOB_BASE_NAME}: FAILURE at Configuring Locust"
      throw e
    }
    

    stage("Performance Locust Run on ${hostNameTef}") {
        def s9runId = UUID.randomUUID().toString()
        print "PerformanceLocustRunId = ${s9runId}"  
      timeout(time: 1, unit: 'HOURS') {
			withCredentials([
				[$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
				[$class: 'UsernamePasswordMultiBinding', credentialsId: 'relEngSqlId', usernameVariable: 'RelEngSqlUserName', passwordVariable: 'RelEngSqlPassword'],
        [$class: 'UsernamePasswordMultiBinding', credentialsId: 'devSqlId', usernameVariable: 'DevSqlUserName', passwordVariable: 'DevSqlPassword'],
        [$class: 'UsernamePasswordMultiBinding', credentialsId: 'devSqlId2', usernameVariable: 'DevSqlUserName2', passwordVariable: 'DevSqlPassword2'],        
        string(credentialsId: 'SplunkLab_API', variable: 'SplunkLab_token'),
        string(credentialsId: 'gw_api_token', variable: 'GW_API_token')
      ]) {  
					powershell """
						.\\rel-eng\\deploy_scripts\\perf\\ConfigureSplunkForLocust.ps1 `
						-TEFBaseVmName '${vmNameTef}' `
						-SplunkToken '${SplunkLab_token}' `
						-AppHostName '${hostNameApp}';
					"""
					
					powershell """
					  .\\rel-eng\\deploy_scripts\\perf\\GenerateTestMerchantsViaLocust.ps1 `
					  -TEFBaseVmName '${vmNameTef}' `
					  -VerifyPerformanceTests '${env.VerifyPerformanceTests}' `
					  -GatewayApiToken '${GW_API_token}';
					"""

					powershell """
					  .\\rel-eng\\deploy_scripts\\perf\\GenerateLocustTransportKeys.ps1 `
					  -TEFBaseVmName '${vmNameTef}';
					"""
					powershell """
					  .\\rel-eng\\perf-testing\\database\\AssignPlatformGpiCredentialsToAllMerchants.ps1 `
            -SqlFqdn '${DBHost}' `
            -SqlUserName '${DevSqlUserName}' `
            -SqlPassword '${DevSqlPassword}';
					"""  
					
					powershell """
					  .\\rel-eng\\perf-testing\\database\\CreateRecurringBills.ps1 `
            -SqlFqdn '${DBHost}' `
            -SqlUserName '${DevSqlUserName2}' `
            -SqlPassword '${DevSqlPassword2}';
					"""  

				}
      }
		
			timeout(time: 1, unit: 'HOURS') {
			withCredentials([
				[$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
				[$class: 'UsernamePasswordMultiBinding', credentialsId: 'relEngSqlId', usernameVariable: 'RelEngSqlUserName', passwordVariable: 'RelEngSqlPassword']
			]) {
				powershell """
					.\\rel-eng\\deploy_scripts\\perf\\DoLocustPerfRun.ps1 `
					-AppServer '${vmNameApp}' `
					-TEFBaseVmName '${vmNameTef}' `
					-BuildPattern '${env.BranchName}' `
					-TeamName '${featureTeamName.toUpperCase()}' `
					-VerifyPerformanceTests '${env.VerifyPerformanceTests}';
				"""	
				
					powershell """
						.\\rel-eng\\deploy_scripts\\perf\\ValidatePerfResults.ps1 `
						-newReportFile "${WORKSPACE}\\rel-eng\\deploy_scripts\\perf\\${featureTeamName.toUpperCase()}-perfReport-1.txt" `
						-verifyPerformanceTests '${env.VerifyPerformanceTests}' `
						-failureThreshold 0 `
						-newHtmlFile "${WORKSPACE}\\rel-eng\\deploy_scripts\\perf\\${featureTeamName.toUpperCase()}-perfReport-1.html";
					"""
					
					publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: "${WORKSPACE}\\rel-eng\\deploy_scripts\\perf\\", reportFiles: "${featureTeamName.toUpperCase()}-perfReport-1.html", reportName: "Perf Run HTML Results"])
					publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: "${WORKSPACE}\\rel-eng\\deploy_scripts\\perf\\", reportFiles: "${featureTeamName.toUpperCase()}-perfReport-1.txt", reportName: "Perf Run TXT Results"])
					
					def perfValidationExitCode = (readFile("${WORKSPACE}\\rel-eng\\deploy_scripts\\perf\\perfValidationExitCode.txt") =~ '\\d+')[0]
					
					if (perfValidationExitCode != '0') {
						buildStatus = 'FAILURE'
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
              sh "exit 1"
            }
					}
					
					print "perfValidationExitCode = ${perfValidationExitCode}"
					
				if (!env.VerifyPerformanceTests.toBoolean()) {
					print "VerifyPerformanceTests=${env.VerifyPerformanceTests} Comparing perf run to master"
					powershell """
							.\\rel-eng\\deploy_scripts\\perf\\ComparePerfResults.ps1 `
							-newReportFile "${WORKSPACE}\\rel-eng\\deploy_scripts\\perf\\${featureTeamName.toUpperCase()}-perfReport-1.txt" `
							-benchmarkReportVersion "1.0.11" `
							-pipelineName '${hostNameTef}';
						"""					
						
					publishHTML([
						allowMissing: false,
						alwaysLinkToLastBuild: true,
						keepAll: true, 
						reportDir: "${WORKSPACE}\\rel-eng\\deploy_scripts\\perf\\", 
						reportFiles: "BenchmarkComparison.html",
						reportName: "Perf Master Comparison"
					])
				} else {
					print "VerifyPerformanceTests=${env.VerifyPerformanceTests} Skipping master comparison"
				}

				}
			}
			
			def buildStatus = currentBuild.result
			buildStatus = buildStatus ?: 'SUCCESSFUL'
			
			currentBuild.result = 'SUCCESS'
			
			if (!env.VerifyPerformanceTests.toBoolean()) {
				def perfExitCode = readFile("${WORKSPACE}\\rel-eng\\deploy_scripts\\perf\\perfExitCode.txt") =~ '\\d+'
				
				if (perfExitCode[0] != '0') {
					buildStatus = 'FAILURE'
					currentBuild.result = 'FAILURE'
				}
			
				print "perfExitCode = ${perfExitCode[0]}"
			}
			
			print "performanceLocustRunId = ${s9runId}"			
		}
  }

  if (env.RunTef == "true" || env.RunPtf == "true") {
    stage ("Setting Memory Buffer for VMs") {
      def s10runId = UUID.randomUUID().toString()
      print "SetMemBufferVMRunId = ${s10runId}"
      def AppVMResetUnlock = false
      parallel (
        "${hostNameDb} VM" : {
          print "Starting the process, Set Memory Buffer for: ${hostNameDb} VM"
          powershell """
            .\\rel-eng\\jenkins\\SetVmMemoryBuffer.ps1 `
            -VmName '${vmNameDb}' `
            -MemoryBuffer 20;
          """
          AppVMResetUnlock = true
          print "Completed the process, Set Memory Buffer for: ${hostNameDb} VM"
        },
        "${hostNameTef} VM" : {
          print "Starting the process, Set Memory Buffer for: ${hostNameTef} VM"
          powershell """
            .\\rel-eng\\jenkins\\SetVmMemoryBuffer.ps1 `
            -VmName '${vmNameTef}' `
            -MemoryBuffer 20;
          """
          print "Completed the process, Set Memory Buffer for: ${hostNameTef} VM"
        },
        "${hostNameApp} VM" : {
          waitUntil(initialRecurrencePeriod: 10000) {AppVMResetUnlock}
          print "Starting the process, Set Memory Buffer for: ${hostNameApp} VM"
          powershell """
            .\\rel-eng\\jenkins\\SetVmMemoryBuffer.ps1 `
            -VmName '${vmNameApp}' `
            -MemoryBuffer 20;
          """
          print "Completed the process, Set Memory Buffer for: ${hostNameApp} VM"
        }
      )
     print "SetMemBufferVMRunId = ${s10runId}"
    }

    stage("Re-Binding VMs") {
      def s11runId = UUID.randomUUID().toString()
      print "ReBindingVMRunId = ${s11runId}"
      withCredentials([
        [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
        [$class: 'UsernamePasswordMultiBinding', credentialsId: 'jenkins_svc_dev', usernameVariable: 'DomainUserNameDev', passwordVariable: 'DomainUserPasswordDev']
      ]) {
        powershell """
          .\\rel-eng\\jenkins\\BindVMs.ps1 `
          -BaseVmName '${vmNameApp}' `
          -DBBaseVmName '${vmNameDb}' `
          -TEFVmName '${vmNameTef}';
        """
      }
      print "ReBindingVMRunId = ${s11runId}"
    }

    stage("Warmup App VM") {
      def s12runId = UUID.randomUUID().toString()
      print "WarmupAppVMRunId =${s12runId}"
      powershell """
        .\\rel-eng\\jenkins\\VerifyApp.ps1 `
        -BaseVmName '${vmNameApp}';
      """
      // bat "Powershell.exe -File ${WORKSPACE}\\rel-eng\\jenkins\\VerifyJobBox.ps1 -BaseVmName \"${AppBaseVMName}\""
      // publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: "${WORKSPACE}\\.jobboxcheck\\results", reportFiles: 'jobboxhealthsite.html', reportName: "Job Box Health Check Results"])
     print "WarmupAppRunId = ${s12runId}"
    }

    stage("Run TEF/PTF") {
      def s13runId = UUID.randomUUID().toString()
      print "RunTEFRunId = ${s13runId}"
      def buildStatus = currentBuild.result
      try {
        timeout(time: 6, unit: 'HOURS') {
        Date start = new Date()
        print "Timestamp at the start of the TEF Run"
        print start.toString()
        withCredentials([
          [$class: 'UsernamePasswordMultiBinding', credentialsId: 'local_AdministratorID', usernameVariable: 'LocalUserName', passwordVariable: 'LocalPassword'],
          [$class: 'UsernamePasswordMultiBinding', credentialsId: 'tefComponentId', usernameVariable: 'TefComponentUserName', passwordVariable: 'TefComponentPassword']
        ]) {
            powershell """
            \$testTypes = \$env:TestTypes -split ','
            .\\rel-eng\\jenkins\\RunTEF.ps1 `
            -DBBaseVmName '${vmNameDb}' `
            -TEFVmName '${vmNameTef}' `
            -TestTypes ${env.TestTypes} `
            -RunTef \$${env.RunTef} `
            -RunPtf \$${env.RunPtf}
          """
          }
        Date stop = new Date()
        print "Timestamp at the stop of the TEF Run"
        print stop.toString()

        TimeDuration td = TimeCategory.minus( stop, start )
        def normalized = ( td.hours != 0 ? td.hours * 60 : 0 ) + td.minutes
        print "Total time taken for the TEF run in minutes: ${normalized}"
        }
      } finally {
        parallel (
            "${hostNameApp} VM" : {
              powershell """
                .\\rel-eng\\jenkins\\SetVmMemoryBuffer.ps1 `
                -VmName '${vmNameApp}' `
                -MemoryBuffer 5;
                .\\rel-eng\\jenkins\\SetVmvCPUCount.ps1 `
                -VmName '${vmNameApp}' `
                -CpuCount 1;
              """
            },
            "${hostNameDb} VM" : {
              powershell """
                .\\rel-eng\\jenkins\\SetVmMemoryBuffer.ps1 `
                -VmName '${vmNameDb}' `
                -MemoryBuffer 5;
                .\\rel-eng\\jenkins\\SetVmvCPUCount.ps1 `
                -VmName '${vmNameDb}' `
                -CpuCount 1;
              """
            },
            "${hostNameTef} VM" : {
              powershell """
                .\\rel-eng\\jenkins\\SetVmMemoryBuffer.ps1 `
                -VmName '${vmNameTef}' `
                -MemoryBuffer 5;
                .\\rel-eng\\jenkins\\SetVmvCPUCount.ps1 `
                -VmName '${vmNameTef}' `
                -CpuCount 1;
              """
            }
          )
        }

        if (env.RunPtf == "true") {
          publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: "${WORKSPACE}\\.cayanMainWorkspace\\results\\ptf", reportFiles: 'ptf_results.html', reportName: "PTF Test Results"])
        }

        def tests = env.TestTypes.split(',')
        for (int i = 0; i < tests.size(); i++) { 
          def testRun = tests[i] + "_" + (i+1)
          publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: "${WORKSPACE}\\.cayanMainWorkspace\\results\\TEF-Artefact-${testRun}", reportFiles: 'TestRunSummary.html', reportName: "${testRun} TEF Test Results"])
          buildStatus  = buildStatus ?: 'SUCCESSFUL'
          def tefExitCode = readFile("${WORKSPACE}\\.cayanMainWorkspace\\results\\TEF-Artefact-${testRun}\\tefExitCode.txt") =~ '\\d+'
          currentBuild.result = 'SUCCESS'
          if (tefExitCode[0] != '0') {
            buildStatus = 'TEF Test FAILURE'
            currentBuild.result = 'FAILURE'
          }
        }
        print "Status ${env.JOB_BASE_NAME}: ${buildStatus}"
        def details = """<p>Test run successfully generated <a href='${env.BUILD_URL}/${env.TestTypes}_TEF_Test_Results/'>${env.TestTypes}</a> Test Results</p>"""
        def subject = wsdlSubject + " & TEF run on ${env.JOB_BASE_NAME} with branch: ${env.BranchName} run was ${buildStatus}"

        if (env.RunPtf == "true") {
          details += """<p>PTF Test run successfully generated <a href='${env.BUILD_URL}/PTF_TEF_Test_Results/'>PTF</a> Test Results</p>"""
        }

        if (tests.size() != 0) {
          for (i = 0; i < tests.size(); i++) {
            details += readFile("${WORKSPACE}\\.cayanMainWorkspace\\results\\TEF-Artefact-${tests[i]}" + "_" + (i+1) +"\\TestRunSummary.html")
          }
        }

        if (env.RunPtf == "true") {
          details += readFile("${WORKSPACE}\\.cayanMainWorkspace\\results\\ptf\\ptf_results.html")
        }

        cayanCommon.SendEmail(details, subject, featureTeamName.toUpperCase())
        print "RunTEFRunId = ${s13runId}"
      }
    }

    deleteDir()
    if (currentBuild.result == "SUCCESS" ) {
      print "Status ${env.JOB_BASE_NAME}: SUCCESSFUL"
    }
  } catch (e) {
    throw e

    deleteDir()

    currentBuild.result = "FAILURE"
    print "Status ${env.JOB_BASE_NAME}: FAILURE"
  }
}

print "JenkinsPipelineRunId = ${runId}"
