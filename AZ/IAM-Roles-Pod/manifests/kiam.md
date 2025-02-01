```yml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  annotations:
    deprecated.daemonset.template.generation: "1"
  creationTimestamp: "2023-08-04T21:53:17Z"
  generation: 1
  labels:
    app: kiam
    chart: kiam-6.1.2
    component: agent
    heritage: Tiller
    release: kiam
  name: kiam-agent
  namespace: kube-system
  resourceVersion: "2553340894"
  uid: 8e470272-41dd-485c-8e09-4a46c917c35e
spec:
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: kiam
      component: agent
      release: kiam
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: kiam
        component: agent
        release: kiam
    spec:
      containers:
      - args:
        - --iptables
        - --no-iptables-remove
        - --host-interface=cali+
        - --json-log
        - --level=info
        - --port=8181
        - --cert=/etc/kiam/tls/cert
        - --key=/etc/kiam/tls/key
        - --ca=/etc/kiam/tls/ca
        - --server-address=kiam-server:443
        - --prometheus-listen-addr=0.0.0.0:9620
        - --prometheus-sync-interval=5s
        - --allow-route-regexp=.*
        - --gateway-timeout-creation=1s
        command:
        - /kiam
        - agent
        env:
        - name: HOST_IP
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: status.podIP
        image: harbor.csis.astrazeneca.net/csis_sysops/uswitch/kiam:v4.0
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /ping
            port: 8181
            scheme: HTTP
          initialDelaySeconds: 3
          periodSeconds: 3
          successThreshold: 1
          timeoutSeconds: 1
        name: kiam-agent
        resources:
          limits:
            cpu: "1"
            memory: 100Mi
          requests:
            cpu: 100m
            memory: 50Mi
        securityContext:
          capabilities:
            add:
            - NET_ADMIN
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /etc/kiam/tls
          name: tls
        - mountPath: /var/run/xtables.lock
          name: xtables
        - mountPath: /etc/ssl/certs
          name: ssl-certs
      dnsPolicy: ClusterFirstWithHostNet
      hostNetwork: true
      nodeSelector:
        role: worker
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: kiam-agent
      serviceAccountName: kiam-agent
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoSchedule
        key: kiam-agent
        operator: Equal
        value: "true"
      volumes:
      - name: tls
        secret:
          defaultMode: 420
          secretName: kiam-agent
      - hostPath:
          path: /run/xtables.lock
          type: FileOrCreate
        name: xtables
      - hostPath:
          path: /etc/pki/ca-trust/extracted/pem
          type: ""
        name: ssl-certs
  updateStrategy:
    type: OnDelete
status:
  currentNumberScheduled: 4
  desiredNumberScheduled: 4
  numberAvailable: 4
  numberMisscheduled: 0
  numberReady: 4
  observedGeneration: 1
  updatedNumberScheduled: 4
```

```yml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  annotations:
    deprecated.daemonset.template.generation: "1"
  creationTimestamp: "2023-08-04T21:53:17Z"
  generation: 1
  labels:
    app: kiam
    chart: kiam-6.1.2
    component: server
    heritage: Tiller
    release: kiam
  name: kiam-server
  namespace: kube-system
  resourceVersion: "2537179964"
  uid: f07c71be-e3f9-4ed2-a1ef-3d02060ec12b
spec:
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: kiam
      component: server
      release: kiam
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: kiam
        component: server
        release: kiam
    spec:
      containers:
      - args:
        - --json-log
        - --level=info
        - --bind=0.0.0.0:443
        - --cert=/etc/kiam/tls/cert
        - --key=/etc/kiam/tls/key
        - --ca=/etc/kiam/tls/ca
        - --role-base-arn-autodetect
        - --session-duration=60m
        - --sync=1m
        - --prometheus-listen-addr=0.0.0.0:9620
        - --prometheus-sync-interval=5s
        command:
        - /kiam
        - server
        env:
        - name: HTTP_PROXY
          value: http://azpzen.astrazeneca.net:9480
        - name: HTTPS_PROXY
          value: http://azpzen.astrazeneca.net:9480
        - name: NO_PROXY
          value: 169.254.169.254,localhost,127.0.0.1,.svc,.default,.local,.cluster.local,kube-api.paas-brown.astrazeneca.net,kubernetes,172.29.128.1
        - name: http_proxy
          value: http://azpzen.astrazeneca.net:9480
        - name: https_proxy
          value: http://azpzen.astrazeneca.net:9480
        - name: no_proxy
          value: 169.254.169.254,localhost,127.0.0.1,.svc,.default,.local,.cluster.local,kube-api.paas-brown.astrazeneca.net,kubernetes,172.29.128.1
        image: harbor.csis.astrazeneca.net/csis_sysops/uswitch/kiam:v4.0
        imagePullPolicy: IfNotPresent
        livenessProbe:
          exec:
            command:
            - /kiam
            - health
            - --cert=/etc/kiam/tls/cert
            - --key=/etc/kiam/tls/key
            - --ca=/etc/kiam/tls/ca
            - --server-address=127.0.0.1:443
            - --server-address-refresh=2s
            - --timeout=5s
            - --gateway-timeout-creation=1s
          failureThreshold: 3
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 10
        name: kiam-server
        readinessProbe:
          exec:
            command:
            - /kiam
            - health
            - --cert=/etc/kiam/tls/cert
            - --key=/etc/kiam/tls/key
            - --ca=/etc/kiam/tls/ca
            - --server-address=127.0.0.1:443
            - --server-address-refresh=2s
            - --timeout=5s
            - --gateway-timeout-creation=1s
          failureThreshold: 3
          initialDelaySeconds: 3
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 10
        resources:
          limits:
            cpu: "1"
            memory: 120Mi
          requests:
            cpu: 800m
            memory: 100Mi
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /etc/kiam/tls
          name: tls
        - mountPath: /etc/ssl/certs
          name: ssl-certs
          readOnly: true
      dnsPolicy: ClusterFirst
      hostNetwork: true
      nodeSelector:
        node-role.kubernetes.io/control-plane: ""
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: kiam-server
      serviceAccountName: kiam-server
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/control-plane
        operator: Exists
      - effect: NoExecute
        key: node-role.kubernetes.io/control-plane
        operator: Exists
      - effect: NoSchedule
        key: master-exec
        operator: Equal
        value: "true"
      - effect: NoExecute
        key: master-exec
        operator: Equal
        value: "true"
      volumes:
      - name: tls
        secret:
          defaultMode: 420
          secretName: kiam-server
      - hostPath:
          path: /usr/share/ca-certificates
          type: ""
        name: ssl-certs
  updateStrategy:
    type: OnDelete
status:
  currentNumberScheduled: 3
  desiredNumberScheduled: 3
  numberAvailable: 3
  numberMisscheduled: 0
  numberReady: 3
  observedGeneration: 1
  updatedNumberScheduled: 3
```