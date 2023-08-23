#!/bin/bash
cd ..
dir=$(pwd)
file=src/part1.sql
find_str="(SELECT setting FROM pg_settings WHERE name = 'data_directory')"

if [[ -e $file ]]; then
	if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # замена запятых на точку в десятичных цифрах
        sed -i 's/,/./g' datasets/*.tsv
        > path.txt
        echo $dir > path.txt
        sed -i -e "s/^.//" -e "s/[a-z]/\U&/1" -e "s|[A-Z]|&:|1" path.txt
        dir=$(cat path.txt)
        sed -i "s|$find_str|'$dir'|g" $file
        rm -f path.txt
	else 
        sed -i "" 's/,/./g' datasets/*.tsv
        sed -i "" "s|$find_str|'$dir'|g" $file
 	fi
else
	echo "File does not exist"
fi

mkdir -p export_data
cd src
