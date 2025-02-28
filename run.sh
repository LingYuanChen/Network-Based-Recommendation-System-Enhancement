#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
item='musical_instruments_new'
# echo "Start parsingGraph.py ${item}"
# python3 parseGraph.py $item 4
# echo "Finish parsingGraph.py ${item}"

echo "Start parsingGraph.py ${item}"
python3 rollingWindow.py $item 4
echo "Finish parsingGraph.py ${item}"

echo "Start centrality.py ${item}"
python3 centrality.py $item
echo "Finish centrality.py ${item}"

echo "Start communityDetection.py ${item}"
python3 communityDetection.py $item
echo "Finish communityDetection.py ${item}"

echo "Start recommend.py ${item}"
python3 recommend.py $item 10
echo "Finish recommend.py ${item}"

echo "Start recommendAnalyze.py ${item}"
python3 recommendAnalyze.py $item 2014 101112 4 10
echo "Finish recommendAnalyze.py ${item}"
