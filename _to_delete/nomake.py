import os
R={
'README.md':[
("make cluster                     # kind create cluster --config 00-setup/kind-config.yaml\n","kind create cluster --config 00-setup/kind-config.yaml\n"),
("make ingress                            # installs ingress-nginx (manifest from the kind guide)\n",
 "kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml   # installs ingress-nginx (from the kind guide)\nkubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=120s\n"),
("make clean-all\nkind delete cluster --name lab","kubectl delete -f 04-ingress/ -f 03-service/ -f 02-deployment/ -f 01-pod/pod.yaml\nkubectl delete -f 05-config-storage/ -f 06-namespace-resources/namespace.yaml\nkubectl delete secret db-pw\nkubectl delete -f 07-debug/\nkind delete cluster --name lab   # removes the whole cluster, so the lines above are only needed to keep it"),
],
'08-lab/lab.md':[("`make cluster`","`kind create cluster --config 00-setup/kind-config.yaml`")]}
for f,rs in R.items():
    s=open(f,encoding='utf8').read()
    for a,b in rs:
        assert a in s,(f,a); s=s.replace(a,b)
    open(f,'w',encoding='utf8').write(s)
