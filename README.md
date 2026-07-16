# RAINFOREST

## Setup your development environment

### Build and Start the Container

First, build the development container image and start the container in the background:

```
# Build the dev image
./scripts/image_build.sh dev

# Start the environment
./scripts/run.sh
```

### Access and Initialize the Container

Once the container is running, exec into it to initialize your workspace and activate the virtual environment:

```
# Enter the running container's bash shell
docker exec -it dev bash

# Inside the container:
./scripts/init.sh
source venv/bin/activate
```

## Retailers

| Name       | Link                            | Collected Data |
|------------|---------------------------------|----------------|
|shufersal   | https://prices.shufersal.co.il/ | stores         |

## Refs

Link: https://www.gov.il/he/pages/cpfta_prices_regulations
