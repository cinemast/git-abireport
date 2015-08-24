#!/bin/bash
set -e
INDEX="./index"
REPOS="./repos"
BUILD="./builds"

mkdir -p $BUILD
mkdir -p $INDEX
mkdir -p $REPOS

function build_tag()
{
	echo "Building new Tag: $1/$2"
	mkdir -p "$BUILD/$1/$2"
	git -C $REPOS/$1 checkout $2 > /dev/null
	cp -r $REPOS/$1/* $BUILD/$1/$2
	tail -n +1 $INDEX/$1 > $BUILD/$1/$2/git-build.sh
	chmod a+x $BUILD/$1/$2/git-build.sh
	pwd=$(pwd)
	cd $BUILD/$1/$2
	bash git-build.sh &> build.log
	cd $pwd
}

function build_tags() {
	for i in $(git -C $REPOS/$1 tag)
	do
		if [ ! -d "$BUILD/$1/$i" ]
		then
			build_tag $1 $i
		fi
	done
}


for i in $INDEX/*
do
	name=$(basename $i)
	if [ -d $REPOS/$name ]
	then
		echo "Updating repo for $name"
		git -C $REPOS/$name checkout master
		git -C $REPOS/$name pull
	else
		mkdir -p $REPOS/$name
		url=$(head -n 1 $INDEX/$name)
		echo "Fetching new repo: $url"
		git clone $url $REPOS/$name
	fi

	build_tags $name



done
