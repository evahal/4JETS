#!/bin/bash    

export SCRAM_ARCH="slc7_amd64_gcc700"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

echo "--------------------   --------------------   --------------------"

export PICODIR=/cms/xaastorage-2/PicoTrees/4JETS/$4/v6/$1
export NANODIR=/cms/xaastorage-2/NanoToolOutput/4JETS/$4/v6/SKIM_$1

echo $PICODIR
echo $NANODIR

mkdir -p $PICODIR
mkdir -p $NANODIR

FILES=$2*.root
for f in $FILES
do
    filename=$(basename -- "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"
    echo $filename
    echo "------------------> Pre-Processing $f"

    python preprocess.py $f $NANODIR $4 $5 $6 # input output year run triglist json
    echo "------------------> Processing $f"
    python treemaker.py $filename $NANODIR/$filename"_Skim.root" $7 $PICODIR $5 $4
done
cd $PICODIR 
hadd -f $1.root *root	
