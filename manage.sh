#!/bin/bash

PID_FILE='./data/lib/err/err.pid'

start_err() {
    err.py -c data/
}

start_errd(){
      err.py -c data/ -d
}


stop_errd(){
      kill -9 $(cat ${PID_FILE})
}



case "$1" in
        start_err)
            echo Starting Garak Bot. Ctrl+C to Stop.
            start_err
            ;;

        start_errd)
            echo Starting Garak Bot daemon.
            start_errd
            ;;
        stop_errd)
            echo Terminating Garak Bot daemon.
            stop_errd
            ;;
        *)
            echo $"Usage: $0 {start_err|start_errd|stop_errd}"
            exit 1
esac