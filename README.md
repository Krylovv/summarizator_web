# summarizator_web

## Введение
Этот репозиторий содержит Web-приложение, позволяющее из текстового сообщения получить краткую информативную выжимку в виде одного-двух предложений.

## Архитектура
Web-приложение реализовано на языке Python с использованием фреймворка Django. Для суммаризации текста выполняется запрос по API к сервису [Суммаризатор](https://developers.sber.ru/portal/products/summarizer?attempt=1) от Сбера.
Docker-контейнер приложения опубликован в Dockerhub: [kryloff/sum_server_amd64_v1.0](https://hub.docker.com/repository/docker/kryloff/sum_server_amd64_v1.0/general)
Для автоматизации процессов CI/CD в проекте используются github actions.
Приложение развёрнуто в k8s кластере с использованием deployment.
Для k8s кластера настроена система мониторинга Prometheus + Grafana.

## Установка
### Docker
Для установки приложения воспользуйтесь образом с Dockerhub:
```
docker pull kryloff/sum_server_amd64_v1.0:latest
docker run -p 8001:8001 kryloff/sum_server_amd64_v1.0:latest 
```
Для проверки установки воспользуйтесь командой
```
docker ps
```
### Minikube K8s cluster
Для установки приложения в кластер внутри minikube в первую очередь потребуется [установить сам minikube](https://minikube.sigs.k8s.io/docs/start/). Для корректной работы приложения с подключенным мониторингом внутри minikube потребуется минимум 2 CPU и 4Гб оперативной памяти.
Клонирование репозитория на машину
```
git clone https://github.com/Krylovv/summarizator_web
```
Запуск minikube
```
minikube start
```
Для удобства работы рекомендуется создать alias: 
```
alias kubectl='minikube kubectl --'
```
Создание deployment и service
```
kubectl apply -f summarizator_web/infrastructure/deployment.yaml
kubectl apply -f summarizator_web/infrastructure/sum-service.yaml
```
Для доступа к приложению из внешней сети можно воспользоваться port-forward: 
```
kubectl port-forward --address=0.0.0.0 sum-service 8001
```
В таком случае приложение будет доступно по ip-адресу хоста на порту 8001.
Или создать ingress
```
minikube addons enable ingress
kubectl apply -f summarizator_web/infrastructure/nginx-ingress.yaml
```
Чтобы использовать ingress требуется указать доменное имя в файле sum-ingress.yaml, строка host
```
nano sum-ingress.yaml
```
Применение правил ingress для сервиса sum-service
```
kubectl apply -f summarizator_web/infrastructure/sum-ingress.yaml
```
После приложение будет доступно по адресу http://YOUR_HOST_NAME/app

## Мониторинг
В качестве мониторинга предлагается использовать решение [kube-prometheus](https://github.com/prometheus-operator/kube-prometheus/). Оно содержит prometheus в качестве источника данных, grafana для визуализации метрик, alertmanager для алертов.

Установка:
```
minikube delete && minikube start --kubernetes-version=v1.26.0 --bootstrapper=kubeadm --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=Webhook --extra-config=scheduler.bind-address=0.0.0.0 --extra-config=controller-manager.bind-address=0.0.0.0
minikube addons disable metrics-server
git clone https://github.com/prometheus-operator/kube-prometheus
kubectl apply --server-side -f kube-prometheus/manifests/setup
kubectl wait \
	--for condition=Established \
	--all CustomResourceDefinition \
	--namespace=monitoring
kubectl apply -f kube-prometheus/manifests/
```
Для доступа к мониторингу можно воспользоватся port-forward (запуск в разных терминалах)
```
kubectl port-forward --address=0.0.0.0 grafana 3000
kubectl port-forward --address=0.0.0.0 prometheus-k8s 9090
kubectl port-forward --address=0.0.0.0 alertmanager-main 9093
```
Соответственно, доступ к мониторингу по ip-адресу машины. Grafana порт 3000, Prometheus порт 9090, Alertmanager порт 9093.

## Как использовать?
Введите текст в форму и нажмите "Отправить", ниже вы получите сокращенную версию текста. Обратите внимание, что модель работает только с русским языком.

## Авторы
* Александр Крылов
* Анастасия Третьякова
