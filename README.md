# infra-ext-webcheck

[![N|Solid](https://www.whatap.io/img/logo.png)](https://www.whatap.io)

infra-ext-webcheck is a web uptime monitoring plugin for whatap-infra monitoring service.

* Uptime, Status Code, Response Time

### Installation
infra-ext-webcheck requires [python](https://python.org/) 2.6+ to run.
#### Install the dependencies.

```sh
$ cd infra-ext-webcheck
$ sudo chmod +x webcheck.monitoring.py
$ sudo vi webcheck.config
```

#### webcheck.config
```
{new url}
{new url}
```

example
```
http://whatap.io
https://github.com
```

#### register script
```sh
sudo WHATAP_HOME=/usr/whatap/infra/conf /usr/whatap/infra/whatap_infrad --user={user to execute mysql monitor} init-script
```
