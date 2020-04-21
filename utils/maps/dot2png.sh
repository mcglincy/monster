#!/bin/bash
for f in ./dot/*.dot
do
  out="./png/$(basename $f .dot).png"
  neato -Tpng $f -o $out -Goverlap=false
done
