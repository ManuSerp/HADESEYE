#bin/bash
#mode1 freq mode2 pp|rt 2400:24500 mpl|qt (not mandatory)
if [ $# = 3 ]
then
    
    if [ $3 = "qt" ]
    then
        python -i rfsweep/qt_sweep.py --setup $1 --freq $2
    else
        python rfsweep/rfsweep.py --setup $1 --freq $2
        
    fi
else
    python rfsweep/rfsweep.py --setup $1 --freq $2
    
    
fi


