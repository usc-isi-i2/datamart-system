# Updating code at DMC

The ISI Datamart is installed at /data/datamart-system/

## Update source 

```
sudo kyao
cd /data/datamart-system/datamart-upload/
git pull
git checkout "commit-hash"

cd /data/datamart-system/datamart-userend
git pull
git checkout "commit-hash"
```

## Restart Datamart

### Stop the datamart
To shut down the Datamart, without stopping other services (like Blazegraph), do:

```
su root
cd /data/datamart-system
./stop-datamart.sh -d
```

### Rebuild the datamart docker image

To rebuild the datamart docker image, just remove the old image. A new image will be create during the datamart start up process.

```
su root
docker image rm datamart-upload_isi_datamart
```

Typically, rebuiding the datamart docker image
`datamart-upload_isi_datamart` is not needed, even with source code
datamart-upload and datamart-userend updates. These code changes are mapped into the running container.

Rebuilding the docker is needed only if the new source code requires
additional python packages.

### Start the datamart

```
su root
./start-datamart.sh -d
```
