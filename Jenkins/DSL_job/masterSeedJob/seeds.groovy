/////////////////////////////////////////////////////////////////////////////
//Master Control
// define enviornment variables
/////////////////////////////////////////////////////////////////////////////

// loaded from a properties file: jenkins/envvar.properties
def repos = reposlist.tokenize(",")


// def repos1 = [repo1]

/////////////////////////////////////////////////////////////////////////////////////////////////
// create the folders where the seed jobs will be placed within according to corresonding folder
/////////////////////////////////////////////////////////////////////////////////////////////////

for(repo in repos) {
    folder(repo)
}


/////////////////////////////////////////////////////////////////////////////////////////////////
// create seed jobs within defined folder - repositories within a specific project in bitbucket 
/////////////////////////////////////////////////////////////////////////////////////////////////

for(repo in repos) {
    def jobenv = repo + "/" + qaenv

    folder(jobenv) {
       description('Folder containing QA jobs') 
    }
}

for(repo in repos) {
  
    def constructjobname = seedprefix + repo
    def createseedinfolder = repo + "/" + constructjobname  
  
    // create a seed job for a specific repository in bitbucket within the project
    job(createseedinfolder) {

        label(jenkinsagent)

        logRotator {
            daysToKeep(7)
            numToKeep(30)
            artifactDaysToKeep(-1)
            artifactNumToKeep(1)
        }

        publishers {
            wsCleanup()
        }

        scm {
            BbS {
                id(bbid)
                branches {
                    branchSpec {
                        name(bbrepobranch)
                    }
                }
                credentialsId(bbcredentialid)
                sshCredentialsId('')
                gitTool(null)
                mirrorName('')
                projectName(bbproject)
                repositoryName(repo)
                serverId(bbserverid)
            }
        }
        triggers {
            scm("H/15 * * * *")
        }

        configure { node ->
            node / buildWrappers << 'com.lookout.jenkins.EnvironmentScript' {
                script 'cat ./jenkins/envvar.properties'
                scriptType unixScript
                runOnlyOnParent false
                hideEnvironmentVariablesValues false
            }
        }

        steps {
            jobDsl {
                targets 'jenkins/seed.groovy'
            }
        }
    }
}


/////////////////////////////////////////////////////////////////////////////
// organize in a listview in jenkins
/////////////////////////////////////////////////////////////////////////////

listView(bbproject) {
    description('Listview for a project in bitbucket')
    filterBuildQueue()
    filterExecutors()

    jobs {
       name ('')
       regex (".*($listviewpattern).*")
    }

    columns {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
    }
}
