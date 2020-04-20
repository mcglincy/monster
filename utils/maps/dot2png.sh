#!/bin/bash
for f in *.dot
do
  out="$(basename $f .dot).png"
  neato -Tpng $f -o $out -Goverlap=false
done
