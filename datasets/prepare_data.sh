#!/bin/bash
dir=../datasets/

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
      # замена запятых на точку в десятичных цифрах
      sed -i 's/,/./g' $dir*.tsv
      > path.txt
      echo $dir > path.txt
      sed -i -e "s/^.//" -e "s/[a-z]/\U&/1" -e "s|[A-Z]|&:|1" path.txt
      dir=$(cat path.txt)
      rm -f path.txt
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
      sed -i 's/,/./g' $dir*.tsv
else
      sed -i "" 's/,/./g' $dir*.tsv
fi

