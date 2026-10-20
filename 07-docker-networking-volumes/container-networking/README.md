# Container Networking

## Layout

- Frontend: `frontend-net`
- Backend: `frontend-net` and `backend-net`
- Database: `backend-net` and `database-net`

## Run

Set a local lab password in the shell. Compose needs this variable for every
command because it is used to initialize MySQL; do not commit the value.

```bash
export MYSQL_ROOT_PASSWORD='choose-a-local-lab-password'
```

```bash
docker compose up -d
docker compose ps
docker compose exec backend ping -c 2 frontend
docker compose exec backend ping -c 2 database
docker network ls
```

Stop the containers:

```bash
docker compose down
unset MYSQL_ROOT_PASSWORD
```
