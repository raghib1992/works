/en-US/account/login?return_to=%2Fen-US%2F

https://community.splunk.com/t5/Installation/Why-are-AWS-ELB-Health-Checks-not-working-properly-after/m-p/299716

https://community.splunk.com/t5/Security/Using-AWS-HTTPS-ELB-with-EC2-Splunk-Web-on-HTTP-port-8000/m-p/73694

https://docs.splunk.com/Documentation/Splunk/8.2.4/Admin/Bestbestpracticesforproxyserver


You can’t proxy https and only do http. I’m open to suggestions if anyone has any to have this work the way I thought it could work. I know we can fall back to instances but we are going to have the same issue unless we assign a public ip to the instance and skip the alb all together. I think using smart store is still a good approach vs local block.

Adding another ecs task to reverse proxy is redundant to the load balancer. If we could get a public ip to stick on the task directly without changing, we don’t need the alb at all but sadly that isn’t supported either.
