#!/bin/bash

function searchClassFromJars(){
	
  #e.g. baoying.quickfixtutorial.FirstQFJClient
	className2BeSearched=$1
	pathToBeSearched=${2:-.}
	
  ##e.g. baoying.quickfixtutorial.FirstQFJClient -> baoying/quickfixtutorial/FirstQFJClient
	pathAsClassName2BeSearched=$(echo $className2BeSearched | sed "s/\./\//g"  )
	
	#for rsome reason, the find -name does not work on my git bash. 
	#So, seach the sub dir is not supported for now.
	ls ${pathToBeSearched} | grep jar | awk ' { printf("%s\n", $NF)}' | while read jar
	do 
		#echo $className2BeSearched $jar
		unzip -l $jar | grep $pathAsClassName2BeSearched | while read foundClass
		do
			echo found in $jar as $foundClass
		done
	done
}
