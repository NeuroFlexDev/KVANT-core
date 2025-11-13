#!/usr/bin/env bash

_error() {
  echo $1
  exit 1
}

help() {
  echo "Commands:"
  echo ""
  echo "build     - build project"
  echo "dev       - run dev server"
  echo ""
}

_python() {
  interpreter=$1
  if [ -z $interpreter ]; then
    interpreter=python3
  fi
  PY=`which $interpreter`
  if [ -z $PY ]; then
    _error "Invalid python interpreter: $PY"
  fi
}

_sqitch() {
    local URI="db:$1"
    SQITCH=`which sqitch`
    if [ -z $SQITCH ]; then
        _error "Cannot find 'sqitch' in your PATH: $PATH"
    fi
    SQITCH="$SQITCH --chdir src/migrations"
    $SQITCH deploy $URI
}

build() {
  _python $1
  poetry env use $PY
  poetry env info
  poetry lock --no-update
  poetry install --no-interaction --no-ansi
}

dev() {
  poetry run uvicorn src.main:app --host ${APP_BIND:=0.0.0.0} --reload
}

distfile() {
  poetry build --no-ansi
}

db_migrate() {
    URI=`poetry run python src/sqitch.py`
    _sqitch $URI
}

case "$1" in
  build)
    build $2
    ;;
  dev)
    dev
    ;;
  distfile)
    distfile $2
    ;;
  db)
    db_migrate $2
    ;;
  *)
    help
    ;;
esac
