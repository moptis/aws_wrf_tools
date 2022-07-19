#!/bin/bash

cd ./all_met/
for d in ../2*/
do
    echo $d
    ln -sf $d/met_em* .
done

