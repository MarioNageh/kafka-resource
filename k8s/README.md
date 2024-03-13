# Create a kind cluster

kind create cluster --config kind-cluster.yaml --name kafka-cluster

# List the clusters
kubectl config get-contexts
kubectl config use-context kind-kafka-cluster         
kubectl config current-context


------------------------------- To Work Ingress Cluster

Deploy the nginx-ingress controller and wait for it to be ready by running:

kubectl apply --filename https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s


kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx



# To List All Objects 
kubectl get all










# Kafka Server Files
- Configurations ```/etc/kafka/```
- Binaries ```/bin/```
- Kafka Data ```/var/lib/kafka/```
- Kafka Logs ```/var/lib/kafka/```


# KAFKA COMMANDS 
- delete topic
``` ./kafka-topics --bootstrap-server localhost:9092 --delete --topic mario```


- list topic
``` ./kafka-topics --bootstrap-server localhost:9092 --list```


- create topic
``` ./kafka-topics --bootstrap-server localhost:9092 --create --topic astra --partitions 3 --replication-factor 2```

- describe topic
``` ./kafka-topics --bootstrap-server localhost:9092 --describe --topic astra```

- list consumer groups
``` ./kafka-consumer-groups --bootstrap-server localhost:9092 --list```

- produce message
``` ./kafka-console-producer --bootstrap-server localhost:9092 --topic astra```

- produce message to partition 1
``` ./kafka-console-producer --bootstrap-server localhost:9092 --topic astra --property "parse.key=true" --property "key.separator=:"`


- describe consumer group
``` ./kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group mario```

- consume with consumer group
``` ./kafka-console-consumer --bootstrap-server localhost:9092 --topic astra --group mario```

- use performance test to produce messages
``` ./kafka-producer-perf-test --topic astra --num-records 1000000 --record-size 1000 --throughput 100000 --producer-props bootstrap.servers=localhost:9092```