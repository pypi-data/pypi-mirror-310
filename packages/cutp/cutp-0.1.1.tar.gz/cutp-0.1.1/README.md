# CUTP - Check Umbrel TCP Ports

A simple CLI tool to check if the TCP port you want to use in your container does not conflict with the port used by any of your [Umbrel](https://github.com/getumbrel/umbrel) apps.

### Check the desired port

Let's assume you want to use port `1287`, then run:

```bash
cutp check 1287
# Port 1287 is free.
```

### Generating a random port

If you are lacking creativity today, cutp can suggest a port:

```bash
cutp gen
# 4120
