#!/bin/bash
kernels=('RBF' 'Exponential' 'Matern32' 'Matern52')
for j in {0..3..1}
do
    echo ${kernels[$j]}
    sed -i "s;kernel = [[:print:]]*;kernel = '${kernels[$j]}';g" test_backup.py

    for i in {100..3000..100}
    do
	number=$i
	echo "i is now $i of 3000"
	sed -i "s/validation[[:digit:]][[:digit:]]*/validation$number/g" test_backup.py
	sed -i "s;params_save_path = [[:print:]]*;params_save_path = '/net/data1/ml2017/gpyparams/${kernels[$j]}_validation_"$number"_memcenter100lhs_sgt50_no_multidim.pickle';g" test_backup.py
	#sed -i "s/samples = [[:digit:]][[:digit:]]*/samples = $number/g" test_backup.py
	mprof run test_backup.py
	
	mv mprof*.dat /net/data1/ml2017/mem_profiles/training_valid100-3000_multidim/${kernels[$j]}_multidim_training_val$i.dat
	
    done 
done
