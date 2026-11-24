.PHONY: cluster ingress pod deploy svc ingress-apply clean-all
cluster:        ## create the kind cluster
	kind create cluster --config 00-setup/kind-config.yaml
ingress:        ## install ingress-nginx (manifest from the kind guide)
	kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
	kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=120s
pod:
	kubectl apply -f 01-pod/pod.yaml
deploy:
	kubectl apply -f 02-deployment/deployment.yaml
svc:
	kubectl apply -f 03-service/service.yaml
ingress-apply:
	kubectl apply -f 04-ingress/ingress.yaml
clean-all:      ## delete lab objects (the cluster stays)
	-kubectl delete -f 04-ingress/ingress.yaml -f 03-service/service.yaml -f 02-deployment/deployment.yaml -f 01-pod/pod.yaml
	-kubectl delete -f 05-config-storage/ -f 06-namespace-resources/namespace.yaml
	-kubectl delete secret db-pw
	-kubectl delete -f 07-debug/
