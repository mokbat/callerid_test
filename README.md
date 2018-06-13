# CALLER ID Module (Test and App)
> This is a module which runs a set of test cases for performing caller id testing.

![GIT][git-image]
![DOCKER][docker-image]
![MIT][mit-license]

[mit-license]: https://img.shields.io/github/license/mashape/apistatus.svg
[git-image]: https://img.shields.io/github/release/qubyte/rubidium.svg
[docker-image]: https://img.shields.io/badge/docker-automated-green.svg
[docker-vers]: https://img.shields.io/badge/docker-18.03-blue.svg

## Installation

#### Docker
Ubuntu:

```sh
sudo apt-get install docker-ce
```

RHEL and Flavors:

```sh
sudo yum install docker-ce
```

#### GIT
Ubuntu:

```sh
sudo apt-get install git
```

RHEL and Flavors:

```sh
sudo yum install git
```

## Usage example with Docker

#### Use Git Clone, Build Docker and Run Test
```sh
git clone https://github.com/mokbat/callerid_test
```

## Usage example without Docker

#### Clone this repository
```sh
curl -O https://raw.githubusercontent.com/mokbat/callerid_test/master/run.sh
```

#### Execute the script
```sh
source run.sh
```

#### Install dependencies for testing
```sh
pip3 install -r requirements.txt --no-index
```

#### Run Functional Tests
```sh
python3 -m unittest test_functional.py
```

#### Run Load Tests
```sh
locust --host=http://localhost:8089 -f test_performance.py
```
Use the web browser - ```http://localhost:8089```
Start the test by specifying ```number of users``` to simulate and ```users/sec```

## Meta

Sundar Ramakrishnan – mokbat@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://mokbat.github.io/callerid_test/](https://mokbat.github.io/callerid_test/)

<!-- Markdown link & img dfn's -->
[mit-license]: https://img.shields.io/github/license/mashape/apistatus.svg
[git-image]: https://img.shields.io/github/release/qubyte/rubidium.svg
[git-vers]: https://img.shields.io/github/release/qubyte/rubidium.svg
[docker-image]: https://img.shields.io/badge/docker-automated-green.svg
[docker-vers]: https://img.shields.io/badge/docker-18.03-blue.svg
