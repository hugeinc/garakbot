#!/bin/bash


start_err() {
    err.py -c data/
}

start_errd(){
      err.py -c data/ -d
}


case "$1" in
        start_err)
            echo Starting Garak Bot. Ctrl+C to Stop.
            start_err
            ;;

        start_errd)
            echo Starting Garak Bot as a daemon.
            start_errd
            ;;
        *)
            echo $"Usage: $0 {start_err|start_errd}"
            exit 1
esac