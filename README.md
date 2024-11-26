# gpt-paraphaser

This repository is a gpt paraphaser service for [Caila](https://app.caila.io/) based on OpenAI model available at Caila.

> Caila is a platform for hosting microservices based on ML models.
> It is a powerful tool that can cover every aspect of your solution’s lifecycle, from model training and QA to deployment and monitoring.

## Get started

Start by getting yourself acquainted with the contents of [`main.py`](./src/main.py).
In terms of features, this is a simple “Hello World” service:

- It has no `fit` method, so it can’t be trained.
- Its `predict` method returns paraphased versions of a query text.

The service relies on the Caila [Python SDK](https://github.com/just-ai/mlp-python-sdk) to expose its functionality to the platform.

Before building a Docker image, insert your account ID and Caila API token in the code.

To create your API token go to *My space* --> *API-tokens* -- *Create token*.

## Build Docker image

To build the service locally, run `./build.sh` in the project root.
You need to have [Docker Engine](https://docs.docker.com/engine/install/) installed and running.

The build script will create a Docker image, push it to the [public Caila Docker registry](https://docker-pub.caila.io/), and print the image URL to the console:

```txt
--------------------------------------------------
Docker image: docker-pub.caila.io/caila-public/mlp-hello-world-service-xxxxxxxxxxxxxxxx:main
--------------------------------------------------
```

You will need this URL to configure your service in Caila.

> ⚠ The public Caila Docker registry has a limited storage time and is intended for educational purposes only.
> Do not use it for production.

## Create Caila service

1. Sign in to [Caila](https://app.caila.io/) or sign up for a new account.
3. Go to *My space* and select *Images* in the sidebar.
    > 🛈 If you don’t see this tab, go to *My space* → *Services*, select *Create service*, and submit a request for access.
    > Our customer support team will get back to you shortly.
5. Select *Create image*. Provide the image name and the URL you got from the build script.
6. On the image description page, select *Create service*. Provide the service name and leave the other settings at their defaults.
7. You should now see your service in the *Services* tab. Go to its details page and select *Diagnostics*.
8. Select *Add instance*. Wait for the instance to start (the status indicator should turn from yellow to green).
9. Go to the *Testing* and try sending a request with a JSON body like
`{
   "text": "Семь раз отмерь, один раз отрежь."
 }`.

If you see `{
  "rephrased_texts": [
    "1st rephased text.",
    "2nd rephased text.",
     ....
    "N rephased text."
  ]
}` in the output, congratulations!
Your service is up and running.

If you would like to learn more about Caila, check out our official [documentation](https://docs.caila.io/).

> ℹ️ You can choose any OpenAI model available in *Catalog* --> *onenai-proxi*. Insert the name in the code next to "model".

## License

This project is licensed under Apache License 2.0.
