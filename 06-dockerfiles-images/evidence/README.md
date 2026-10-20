# Multi-Stage Build Evidence

Name: Pranav Bharadwaj

Enrollment number: **24bcs10006**

The commands and output below were captured from a fresh local build and run
on 9 October 2026. The application returned the required text on port `8080`,
and the Node.js, Python, and Java deployments responded on their documented
ports.

## Build and run

From the repository root:

```console
$ docker compose -p homework-session07 -f 06-dockerfiles-images/docker-compose.yml up -d --build
```

All four images built and the four containers started successfully.

## Application checks

```console
$ for port in 8080 8201 8202 8203; do printf '%s: ' "$port"; curl --fail --silent --show-error --max-time 8 "http://127.0.0.1:$port/" | grep -o '<h1>[^<]*</h1>'; done
8080: <h1>Hello World from Docker multi-stage build</h1>
8201: <h1>Hello World from Node.js deployment</h1>
8202: <h1>Hello World from Python deployment</h1>
8203: <h1>Hello World from Java deployment</h1>
```

## `docker ps`

```console
$ docker ps --filter name=homework-session07 --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
NAMES                              STATUS          PORTS
homework-session07-python-1        Up 10 seconds   0.0.0.0:8202->5000/tcp, [::]:8202->5000/tcp
homework-session07-java-1          Up 10 seconds   0.0.0.0:8203->8080/tcp, [::]:8203->8080/tcp
homework-session07-multi-stage-1   Up 11 seconds   0.0.0.0:8080->3000/tcp, [::]:8080->3000/tcp
homework-session07-nodejs-1        Up 10 seconds   0.0.0.0:8201->3000/tcp, [::]:8201->3000/tcp
```

The temporary verification containers were stopped after these checks. To
repeat the demonstration, run the build command above and then:

```bash
docker compose -p homework-session07 -f 06-dockerfiles-images/docker-compose.yml ps
curl http://127.0.0.1:8080/
```
