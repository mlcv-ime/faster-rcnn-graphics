#!/bin/bash

FLOWCHARTS=flowcharts768.tar.gz
MATH=math768.tar.gz 

cd datasets/flowcharts

echo "Downloading flowcharts dataset..."
wget http://www.vision.ime.usp.br/~frank.aguilar/datasets/flowcharts768.tar.gz -o $FLOWCHARTS 

echo "Unzipping..."
tar -xf $FLOWCHARTS

cd ../../datasets/math

echo "Downloading math dataset..."
wget http://www.vision.ime.usp.br/~frank.aguilar/datasets/math768.tar.gz -o $MATH

echo "Unzipping..."
tar -xf $MATH

cd ../../

echo "Done."
