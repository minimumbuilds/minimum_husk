# minimum_template

This the self-contstructing base template for minimum_builds autobuilds.

Clone this repository and ``make init`` to:

Create:
- Create cooresponding repository on GibHub
- Create & trigger Travis.ci for build tests
- Create & trigger autobuilds on Docker Hub.

Build:
- Update all file to reflect to CWD as the project name
- Remove this README.md and replace with a versioned project specific README.md

Requiremments:
- ACCOUNTS: www.github.com, hub.docker.com, travis-ci.org
- bumpversion https://github.com/peritus/bumpversion
- hub https://hub.github.com/

# minimum_template

Version: v0.0.1

## Docker Image

[![](https://images.microbadger.com/badges/version/minimumbuilds/minimum_template:v0.0.0.svg)](https://microbadger.com/images/minimumbuilds/minimum_template:v0.0.0 "Get your own version badge on microbadger.com")[![](https://images.microbadger.com/badges/image/minimumbuilds/minimum_template:v0.0.0.svg)](https://microbadger.com/images/minimumbuilds/minimum_template:v0.0.0 "Get your own image badge on microbadger.com")[![](https://images.microbadger.com/badges/commit/minimumbuilds/minimum_template:v0.0.0.svg)](https://microbadger.com/images/minimumbuilds/minimum_template:v0.0.0 "Get your own commit badge on microbadger.com") 

## Build
[![Build Status](https://travis-ci.org/minimumbuilds/minimum_template.svg?branch=v0.0.0)](https://travis-ci.org/minimumbuilds/minimum_template)

## Pull
	docker pull minimumbuilds/minimum_template

## Run
	docker run -it --rm minimumbuilds/minimum_template

## Contents

### Base:
- Official 3.6 alpine linux docker

### Adds:
- python3

Minimal Builds. There are many like it, this one is mine.

## Built With

* [Alpine Linux](https://hub.docker.com/_/alpine/) - Alpine Linux Official Docker

## Authors

* **Minimum Builds** - *Initial work* - [minimumbuilds](https://github.com/minimumbuilds)
