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

For security, the user credentials are left out from the repository. The docker
will read the credentials from the `.env`.

```
# Running the following code, will generate an example `.env` whereby you should
# replace the example with your credentials
make init

# This will then build the docker image. As I am using quite a large image, the
# image will take quite some time for it to build
make build
```

Now, we can start the container with the following snippet. Several firefox
browser should pop out.
```
make run
```
### Side note

Do not be confused by the two `Makefile`, the `Makefile` in the `src/` folder is
meant to be used in the container.
