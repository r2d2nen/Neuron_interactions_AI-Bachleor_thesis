#!/bin/bash

for j in {1..50..1}
do
    sed -i "s;single_lec_E_curve[[:digit:]][[:digit:]]*/50;single_lec_E_curve$j/50;g" single_energy_curve.py
    python single_energy_curve.py
done
    
    
    
