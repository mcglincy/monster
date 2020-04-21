#!/bin/bash
for f in ./dot/*.dot
do
  out="./svg/$(basename $f .dot).svg"
  neato -Tsvg $f -o $out -Goverlap=false
done
