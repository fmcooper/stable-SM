#!/bin/bash
set -x

# variables you may change
TIMEOUTTIME=10 						# timeout time for programs
CTTIMEOUTTIME=100					# timeout time for correctness testing
TIMEOUT="gtimeout $TIMEOUTTIME"		# timeout operation ** set command to "timeout" for linux and "gtimeout" for mac
PREPATH="./Evaluations/"			# location of your results
PARALLEL_OPTS="--jobs 4 --bar"		# changes the number of parallel jobs running
JAVA_OPTS="-cp $(CLASSPATH):../ -XX:+UseSerialGC -Xmx1G" 	# java options, serial garbage collection, heap space


# variables used by other programs (don't change unless necessary)
INSTANCESFILE="instanceGenerator/instanceNames.txt"
IPINSTANCESFILE="instanceGenerator/ipInstanceNames.txt"
NONIPINSTANCESFILE="instanceGenerator/nonipInstanceNames.txt"
RESGS_NSW="ResultsGS_notSwapped"
RESGS_SW="ResultsGS_Swapped"
RES_STABLE="Results_stable"
RES_CORR="Correctness"


export TIMEOUTTIME=$TIMEOUTTIME
export CTTIMEOUTTIME=$CTTIMEOUTTIME
export TIMEOUT=$TIMEOUT
export RESGS_NSW=$RESGS_NSW
export RESGS_SW=$RESGS_SW
export RES_STABLE=$RES_STABLE
export RES_CORR=$RES_CORR
export JAVA_OPTS=$JAVA_OPTS


# compile
source ~/.bashrc
javac -d . code/*.java
javac -d . correctness/*.java

# create the instances to generate lists
python instanceGenerator/instancesToGenerate.py userOptions.txt $PREPATH


# create the instances
createInstance() {
	DIR=$(dirname $1)
 	mkdir -p $DIR
 	python instanceGenerator/generator.py $1 > $1
 	# echo "instance created: $1"
}

export -f createInstance
cat $INSTANCESFILE | parallel $PARALLEL_OPTS createInstance {} 


# do the experiments
runGSexperiment() {
	INSTANCE=$1
	RESNAME=$2
	SWAPPED=$3
	DIR=$(dirname $INSTANCE)
	RESDIR=$(sed "s/Instances/$RESNAME/g" <<< $DIR)
	RESFILE=$(sed "s/Instances/$RESNAME/g" <<< $INSTANCE)
	mkdir -p $RESDIR
	$TIMEOUT java $JAVA_OPTS code/Main_GS $INSTANCE $SWAPPED > $RESFILE
	EXIT=$?
	if [ $EXIT -eq 124 ] ; then echo "$TIMEOUT s" >> $RESFILE ; 
	elif [ $EXIT -eq 4 ] ; then echo "upstream $TIMEOUT s" >> $RESFILE ;
	elif [ $EXIT -ne 0 ] ; then echo "**uncontrolled error**" >> $RESFILE ; fi   
	echo "exitCode $EXIT" >> $RESFILE 
	echo "code/Main_GS completed" >> $RESFILE 
}

runStableExperiment() {
	INSTANCE=$1
	DIR=$(dirname $INSTANCE)
	RESDIR=$(sed "s/Instances/$RES_STABLE/g" <<< $DIR)
	RESFILE=$(sed "s/Instances/$RES_STABLE/g" <<< $INSTANCE)
	RESFILESW=$(sed "s/Instances/$RESGS_SW/g" <<< $INSTANCE)
	RESFILENSW=$(sed "s/Instances/$RESGS_NSW/g" <<< $INSTANCE)
	mkdir -p $RESDIR
	$TOcommand $TIMEOUT java $JAVA_OPTS code/Main_GetStableMatchings $INSTANCE $RESFILENSW $RESFILESW > $RESFILE
	EXIT=$?
	if [ $EXIT -eq 124 ] ; then echo "timeout $TIMEOUT s" >> $RESFILE ; 
	elif [ $EXIT -eq 4 ] ; then echo "upstream timeout $TIMEOUT s" >> $RESFILE ;
	elif [ $EXIT -ne 0 ] ; then echo "**uncontrolled error**" >> $RESFILE ; fi   
	echo "exitCode $EXIT" >> $RESFILE 
	echo "code/Main_GetStableMatchings completed" >> $RESFILE 
}

export -f runGSexperiment
export -f runStableExperiment
cat $INSTANCESFILE | parallel $PARALLEL_OPTS runGSexperiment {} $RESGS_NSW false
# Next line could change to have the input from the above run
cat $INSTANCESFILE | parallel $PARALLEL_OPTS runGSexperiment {} $RESGS_SW true 
cat $INSTANCESFILE | parallel $PARALLEL_OPTS runStableExperiment {} 



# do correctness
runCorrectness() {
	INSTANCE=$1
	ISIP=$2
	DIR=$(dirname $INSTANCE)
	CORDIR=$(sed "s/Instances/$RES_CORR/g" <<< $DIR)
	RESFILE=$(sed "s/Instances/$RES_STABLE/g" <<< $INSTANCE)
	CORFILE=$(sed "s/Instances/$RES_CORR/g" <<< $INSTANCE)
	mkdir -p $CORDIR
	java $JAVA_OPTS correctness/Main_Tester $INSTANCE $RESFILE "false" > $CORFILE
	EXIT=$?
	if [ $EXIT -eq 5 ] ; then echo "timeout $TIMEOUT s" >> $CORFILE ; 
	elif [ $EXIT -eq 4 ] ; then echo "upstream timeout $TIMEOUT s" >> $CORFILE ;
	elif [ $EXIT -ne 0 ] ; then echo "**uncontrolled error**" >> $CORFILE ; fi   
	echo "exitCode $EXIT" >> $CORFILE 
	echo "correctness/Main_Tester completed" >> $CORFILE 

	if [ "$ISIP" == "true" ]
	then
		python correctness/pulpIP.py $INSTANCE $CTTIMEOUTTIME >> $CORFILE 
		EXIT=$?
		if [ $EXIT -eq 5 ] ; then echo "ip_timeout $TIMEOUT s" >> $CORFILE ; 
		elif [ $EXIT -eq 4 ] ; then echo "upstream timeout $TIMEOUT s" >> $CORFILE ;
		elif [ $EXIT -ne 0 ] ; then echo "**uncontrolled error**" >> $CORFILE ; fi  
		echo "exitCode $EXIT" >> $CORFILE 
		echo "correctness/pulpIP.py completed" >> $CORFILE 
	fi
}

export -f runCorrectness
cat $IPINSTANCESFILE | parallel $PARALLEL_OPTS runCorrectness {} true
cat $NONIPINSTANCESFILE | parallel $PARALLEL_OPTS runCorrectness {} false



# stats
python stats/pythonCorrectness.py $PREPATH
python stats/pythonStats.py $PREPATH


echo "all processes complete"

