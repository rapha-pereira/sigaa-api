run-dev:
	poetry run uvicorn app.main:app

gcloud-build:
	gcloud builds submit --tag gcr.io/white-rigging-372215/sigaa-api-docker

build:
	docker build -t sigaa-api-docker .

tag:
	docker tag sigaa-api-docker gcr.io/white-rigging-372215/sigaa-api-docker

push:
	docker push gcr.io/white-rigging-372215/sigaa-api-docker

deploy:
	gcloud run deploy sigaa-api-service --image gcr.io/white-rigging-372215/sigaa-api-docker --platform managed --region southamerica-west1 --allow-unauthenticated