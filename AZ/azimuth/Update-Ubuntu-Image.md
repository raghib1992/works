## Update Ubuntu:22.04 Images
1. Ubuntu image create by main.workflow.yaml file in `azimuth-images` workflow
2. In workfow yaml file, check for Dockerfile path
3. Update Dockerfile or main.workflow.yml file as per need.
4. To update env value, update the env value in main.workflow.yml file
5. run action to create updated images
6. This workflow is runs-on self-hosted runner
7. Check runner for dev env used by workflow `azimuth-profiles/github-runners/dev/azu-ignite.yaml`

```yml
---
apiVersion: actions.summerwind.dev/v1alpha1
kind: RunnerDeployment
metadata:
  name: runner-deploy-azu-ignite-azimuth-demo
  namespace: brown-dev-001
spec:
  template:
    metadata:
      annotations:
        sidecar.istio.io/inject: "false"
    spec:
      serviceAccountName: default-editor
      labels:
        - azimuth
      repository: AZU-IGNITE/azimuth-demo
      env:
        - name: http_proxy
          value: http://azpse.astrazeneca.net:9480
        - name: https_proxy
          value: http://azpse.astrazeneca.net:9480
        - name: no_proxy
          value: 10.0.0.0/8,172.29.0.0/8,astrazeneca.net
        - name: DISABLE_RUNNER_UPDATE
          value: "true"
      dockerEnv:
        - name: http_proxy
          value: http://azpse.astrazeneca.net:9480
        - name: https_proxy
          value: http://azpse.astrazeneca.net:9480
        - name: no_proxy
          value: 10.0.0.0/8,172.29.0.0/8,astrazeneca.net
      volumeMounts:
        - mountPath: /home/jovyan/vol-1/
          name: shared-lcm
      volumes:
        - name: shared-lcm
          persistentVolumeClaim:
            claimName: shared-brown-dev-001
      resources:
        limits:
          cpu: "1"
          memory: "3Gi"
        requests:
          cpu: "0.5"
          memory: "2Gi"
```