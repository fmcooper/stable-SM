#!/bin/bash
set -x

# variables you may change
TIMEOUTCOMMAND="gtimeout"		# timeout operation ** set command to "timeout" for linux and "gtimeout" for mac
TIMEOUT=1000					# timeout time for programs
CP="$(CLASSPATH):../"			# java classpath
# PREPATH="./examples/DM_pg91/"	# location of the example to solve
# PREPATH="./examples/DG_RI_pg12/"
PREPATH="./examples/DG_RI_pg22/"


# variables used by other programs (don't change unless necessary)
INSTANCE="example.txt"
GS_NS="resultsGS_notSwapped.txt"
GS_S="resultsGS_swapped.txt"
STABLE="stableMatchings.txt"
CORRECTNESS="correctness.txt"
PATH_INSTANCE="$PREPATH$INSTANCE"
PATH_GS_NS="$PREPATH$GS_NS"
PATH_GS_S="$PREPATH$GS_S"
PATH_STABLE="$PREPATH$STABLE"
PATH_CORRECTNESS="$PREPATH$CORRECTNESS"



# compile
source ~/.bashrc
javac -d . code/*.java
javac -d . correctness/*.java


# run the gale shapley algorithm to find the man optimal stable matching
$TIMEOUTCOMMAND $TIMEOUT java -cp $CP code/Main_GS $PATH_INSTANCE false > $PATH_GS_NS
EXIT=$?
if [ $EXIT -eq 124 ] ; then echo "timeout $TIMEOUT s" >> $PATH_GS_NS ; 
elif [ $EXIT -eq 4 ] ; then echo "upstream timeout $TIMEOUT s" >> $PATH_GS_NS ;
elif [ $EXIT -ne 0 ] ; then echo "**uncontrolled error**" >> $PATH_GS_NS ; fi   
echo "exitCode $EXIT" >> $PATH_GS_NS 
echo "code/Main_GS" >> $PATH_GS_NS 

# run the gale shapley algorithm to find the woman optimal stable matching
$TIMEOUTCOMMAND $TIMEOUT java -cp $CP code/Main_GS $PATH_GS_NS true > $PATH_GS_S
EXIT=$?
if [ $EXIT -eq 124 ] ; then echo "timeout $TIMEOUT s" >> $PATH_GS_S ; 
elif [ $EXIT -eq 4 ] ; then echo "upstream timeout $TIMEOUT s" >> $PATH_GS_S ;
elif [ $EXIT -ne 0 ] ; then echo "**uncontrolled error**" >> $PATH_GS_S ; fi   
echo "exitCode $EXIT" >> $PATH_GS_S 
echo "code/Main_GS" >> $PATH_GS_S 

# find all stable matchings
$TIMEOUTCOMMAND $TIMEOUT java -cp $CP code/Main_GetStableMatchings $PATH_INSTANCE $PATH_GS_NS $PATH_GS_S > $PATH_STABLE
EXIT=$?
if [ $EXIT -eq 124 ] ; then echo "timeout $TIMEOUT s" >> $PATH_STABLE ; 
elif [ $EXIT -eq 4 ] ; then echo "upstream timeout $TIMEOUT s" >> $PATH_STABLE ;
elif [ $EXIT -ne 0 ] ; then echo "**uncontrolled error**" >> $PATH_STABLE ; fi   
echo "exitCode $EXIT" >> $PATH_STABLE 
echo "code/Main_GetStableMatchings completed" >> $PATH_STABLE 

# run the correctness tester without running the IP
java -cp $CP correctness/Main_Tester $PATH_INSTANCE $PATH_STABLE false > $PATH_CORRECTNESS
EXIT=$?
if [ $EXIT -eq 5 ] ; then echo "timeout $TIMEOUT s" >> $PATH_CORRECTNESS ; 
elif [ $EXIT -eq 4 ] ; then echo "upstream timeout $TIMEOUT s" >> $PATH_CORRECTNESS ;
elif [ $EXIT -ne 0 ] ; then echo "**uncontrolled error**" >> $PATH_CORRECTNESS ; fi   
echo "exitCode $EXIT" >> $PATH_CORRECTNESS 
echo "correctness/Main_Tester completed" >> $PATH_CORRECTNESS 

# run the correctness tester IP
python correctness/pulpIP.py $PATH_INSTANCE $TIMEOUT >> $PATH_CORRECTNESS
EXIT=$?
if [ $EXIT -eq 5 ] ; then echo "ip_timeout $TIMEOUT s" >> $PATH_CORRECTNESS ; 
elif [ $EXIT -eq 4 ] ; then echo "upstream timeout $TIMEOUT s" >> $PATH_CORRECTNESS ;
elif [ $EXIT -ne 0 ] ; then echo "**uncontrolled error**" >> $PATH_CORRECTNESS ; fi  
echo "exitCode $EXIT" >> $PATH_CORRECTNESS 
echo "correctness/pulpIP.py completed" >> $PATH_CORRECTNESS 

echo "all processes complete"

