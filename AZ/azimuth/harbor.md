# Docker Pull and Push to Harbor

### Pulling and updating latest images example using mountain/kalimanjaro:latest image

```sh
docker pull mountain/kalimanjaro:latest
docker tag mountain/kalimanjaro:latest harbor.csis.mrndevops.in/mountain/kalimanjaro:v0.27.0
docker login harbor.csis.astrazeneca.net
docker push harbor.csis.mrndevops.in/mountain/kalimanjaro:v0.27.0
```