#!/usr/bin/env bash
# Maintainer: 'Sergey Buyalsky'
# Team contact: ssb@fronttier.ru
# Description: 'Run application in a docker image'

set -eu -o pipefail

function main() {

  if [[ ${DEBUG:=false} == 'true' ]] ; then
      echo "Enabled debug mode"
      sleep infinity
  else
      /app/project.sh db
      /app/project.sh $APP_ENV
  fi

}

main; exit $?