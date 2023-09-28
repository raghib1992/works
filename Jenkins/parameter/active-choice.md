# active paramter

## Paramter name
- name: env
- check groovy script
```groovy
return[
'Production',
'QA',
'Development'
]
```
# Reactive parameter
## paramter name
- name: server
```groovy
if(env.equals("Production")){
  return ["Prod1"]
}
else if(env.equals("QA")){
  return ["QA1","QA2"]
}
else if(env.equals("Development")){
  return ["Dev1","Dev2","Dev3"]
}
else{
	return ["Select a server from dropdown"]
}
```