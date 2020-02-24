### Quickstart

```sh
docker-compose up --build
```

### How it works

###### WEB microservice

 - Receives arithmetic operation and operators which will be *asynchronously* RPCed to `RPC microservice`.
 - Provides access to procedure's results and status.

###### RPC microservice

 - Receives arithmetic operation and operators invoked by `WEB microservice`.
 - Persists the procedure result, so `WEB microservice` can retrieve and respond it.

### How to (lazily) use it

```sh
sh calculate.sh OPERATION
```

This will request the `WEB microservice` to schedule an  
### Notes

`Nameko` uses the `eventlets` lib to work it's async magic.
 This make it impossible to debug the tests without messing around with how Nameko works, which ends up losing the credibility of the tests. 
 It's fine and nicely supports tests for `sync` RPCs, though :D

Scale at your will by instantiating more `web` and/or `rpc` containers

It's also good to remember that there are no mounted volumes, so all the procedure's records will be lost in the `void` once the containers stop.
And that will was really  fun to do <3