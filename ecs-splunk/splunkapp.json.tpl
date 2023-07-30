[
    {
      "name": "splunk",
      "image": "splunk/splunk",
      "cpu": 1024,
      "memory": 2048,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000
        }
      ],
      "environment" : [
        { "name" : "SPLUNK_START_ARGS", "value" : "--accept-license" },
        { "name" : "SPLUNK_PASSWORD", "valueFrom" : "${splunk-password}" }
      ],
      "mountPoints" : [
        {
          "sourceVolume" : "etc",
          "containerPath" : "/opt/splunk/etc"
        }
      ]
    }
]