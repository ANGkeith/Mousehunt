# Mousehunt

This repository is part of my personal project for practising usage of selenium
and docker.

## Prerequisites

The only dependency is docker :). The current setup only support Linux hosts
since different methods are required to access the X11-Session of the container.

```
Docker version 18.09.7, build 2d0083d
```

## Usage
First, modify the `.env.sample` with your respective credential. Then run the
following

```
# This will generate a default `.env` and `docker-compose.yml` configuration
make init

# This will then build the docker image. As I am using quite a large image, the
# image will take quite some time for it to build
make build
```

To start the container(s).
```
make run
```
### Side note

Do not be confused by the two `Makefile`, the `Makefile` in the `src/` folder is
meant to be used in the container.
