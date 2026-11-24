# Kubernetes'e Giriş: Lab Deposu

"Introduction to Kubernetes" sunumunun (44 slayt) çalıştırılabilir örnekleri. Her klasör sunumdaki bir bölüme karşılık gelir. Önce slaytı izle, sonra manifesti çalıştırıp kendin dene.

## Gereksinimler
- Docker (çalışıyor olmalı), [kind](https://kind.sigs.k8s.io/docs/user/quick-start), `kubectl`
- kind yerine minikube veya Docker Desktop kümesi de olur; yalnızca kurulum adımı ve Ingress farklıdır.

## Hızlı başlangıç
```bash
make cluster                     # kind create cluster --config 00-setup/kind-config.yaml
kubectl get nodes                # STATUS: Ready
kubectl config current-context   # kind-lab
```

## Klasörler

| Klasör | Sunumdaki konu | Dosyalar |
|---|---|---|
| `00-setup` | Yerel küme | `kind-config.yaml`, `kind-multinode.yaml` |
| `01-pod` | Pod, yaşam döngüsü, probes | `pod.yaml`, `pod-probes.yaml`, `pod-liveness-fail.yaml` |
| `02-deployment` | ReplicaSet, Deployment, rollout | `deployment.yaml` |
| `03-service` | Label, Service, DNS | `service.yaml`, `service-nodeport.yaml` |
| `04-ingress` | Ingress | `ingress.yaml` |
| `05-config-storage` | ConfigMap, Secret, PV/PVC | `configmap.yaml`, `pod-config-secret.yaml`, `pvc.yaml`, `pod-pvc.yaml` |
| `06-namespace-resources` | Namespace, requests/limits | `namespace.yaml`, `pod-oom.yaml` |
| `07-debug` | Hata ayıklama | `broken-*.yaml` (bilerek bozuk) |
| `08-lab` | Slayttaki 8 adımlı lab | `lab.md` |
| `CHEATSHEET.md` | Docker -> kubectl tablosu, sık komutlar | |

## Bölüm bölüm egzersizler

### 01 · Pod
```bash
kubectl apply -f 01-pod/pod.yaml
kubectl get pods                        # ContainerCreating -> Running
kubectl describe pod hello              # en alttaki Events: Scheduled, Pulling, Pulled, Started
kubectl port-forward pod/hello 8080:80  # tarayıcıda localhost:8080
kubectl delete pod hello                # kimse yeniden yaratmaz
```
**Probes:** `01-pod/pod-probes.yaml` uygula; sonra `01-pod/pod-liveness-fail.yaml` uygula ve `kubectl get pods -w` ile RESTARTS sayısının arttığını izle.
**Soru:** readiness ve liveness probe farkı nedir? Hangisi başarısız olursa container yeniden başlatılır?

### 02 · Deployment ve rollout
```bash
kubectl apply -f 02-deployment/deployment.yaml
kubectl get deploy,rs,pods
kubectl delete pod <POD_ADI>            # self-healing: yenisi birkaç saniyede gelir
kubectl scale deployment web --replicas=5
kubectl set image deployment/web nginx=nginx:1.26-alpine
kubectl rollout status deployment/web
kubectl rollout history deployment/web
kubectl set image deployment/web nginx=nginx:yok-boyle-bir-etiket   # bozuk sürüm
kubectl get pods                        # yeni Pod ImagePullBackOff, eskiler hâlâ Running
kubectl rollout undo deployment/web
```
**Soru:** Bozuk imajı gönderdiğimizde neden kesinti olmadı?

### 03 · Service ve DNS
```bash
kubectl apply -f 03-service/service.yaml
kubectl get svc web
kubectl get endpoints web               # Pod IP'leri listelenir
kubectl run tmp --rm -it --image=busybox:1.36 --restart=Never -- wget -qO- http://web
kubectl port-forward svc/web 8080:80
```
**Soru:** Pod silinince IP'si değişir. Service adresi neden değişmez?
**Dene:** `kubectl scale deployment web --replicas=0` yap, `kubectl get endpoints web` boş mu? Sonra tekrar 3 yap.

### 04 · Ingress
```bash
make ingress                            # ingress-nginx kurulumu (kind rehberindeki manifest)
kubectl apply -f 04-ingress/ingress.yaml
curl -H "Host: shop.example.com" http://localhost/
```
Küme `kind-config.yaml` ile kurulmadıysa Ingress çalışmaz; `port-forward` ile devam et.

### 05 · ConfigMap, Secret, PVC
```bash
kubectl apply -f 05-config-storage/configmap.yaml
kubectl create secret generic db-pw --from-literal=password=change-me
kubectl apply -f 05-config-storage/pod-config-secret.yaml
kubectl exec config-demo -- env | grep -E "REDIS_HOST|DB_PASSWORD"
kubectl get secret db-pw -o jsonpath='{.data.password}' | base64 -d   # Secret şifreli değil, yalnızca base64
# Kalıcılık:
kubectl apply -f 05-config-storage/pvc.yaml -f 05-config-storage/pod-pvc.yaml
kubectl delete pod writer
kubectl apply -f 05-config-storage/pod-pvc.yaml
kubectl logs writer                     # iki tarih satırı: veri kaldı
```
PVC bir süre `Pending` görünebilir: kind'ın StorageClass'ı Pod yaratılınca volume'u bağlar.

### 06 · Namespace ve kaynaklar
```bash
kubectl apply -f 06-namespace-resources/namespace.yaml
kubectl create deployment w --image=nginx:1.27-alpine --replicas=6 -n dev
kubectl get pods -n dev                 # ResourceQuota yüzünden bazı Pod'lar yaratılamaz: kubectl describe rs -n dev
kubectl apply -f 06-namespace-resources/pod-oom.yaml
kubectl describe pod oom                # Last State: OOMKilled
```
Not: quota'lı namespace'te requests/limits olmayan Pod reddedilebilir; `create deployment` ile yapılan deneyde mesajı `describe rs` içinde oku.

### 07 · Hata ayıklama
`07-debug/` altındaki her dosya farklı bir hata taşır. Uygula, belirtiyi gör, `get -> describe -> logs` sırasıyla nedeni bul ve düzelt. İpuçları dosyaların başındaki yorumlarda.

### 08 · Lab
Sunumdaki 8 adımın tamamı: `08-lab/lab.md`.

## Temizlik
```bash
make clean-all
kind delete cluster --name lab
```

## Not
Manifestler sunumdaki örneklerden türetilmiştir ve nginx imajıyla çalışır. Takılırsan önce `kubectl describe` çıktısının en altındaki **Events** bölümüne bak.
