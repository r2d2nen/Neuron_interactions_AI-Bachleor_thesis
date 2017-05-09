#!/bin/bash
kernels=('Matern52' 'Exponential')
for j in {0..1..1}
do
    echo ${kernels[$j]}
    sed -i "s;kernel = [[:print:]]*;kernel = '${kernels[$j]}';g" test.py

    for i in {250..3000..250}
    do
	number=$i
	echo "i is now $i of 3000"
	sed -i "s/training[[:digit:]][[:digit:]]*/training$number/g" test.py
	sed -i "s;params_save_path = [[:print:]]*;params_save_path = '/net/data1/ml2017/gpyparams/E_curve_gpy/${kernels[$j]}_E_curve_training_"$number"_lhs_sgt1_150_multidim.pickle';g" test.py
	sed -i "s/samples = [[:digit:]][[:digit:]]*/samples = $number/g" test.py
	python test.py
	
	#rm mprof*.dat
	
    done 
done
