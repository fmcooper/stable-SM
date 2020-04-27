# stable-SM Readme

Two-sided profile-based optimality in the stable marriage problem
******************************
******************************

1) what is this software?
2) software and data
3) compiling and running an example
4) interpreting results files
5) running multiple instances - preparation
6) running multiple instances
7) motivation experiments
8) versions


******************************

# 1) what is this software?

This software runs algorithms to find all stable matchings for an instance of the Stable Marriage problem with Incomplete lists (SMI). This comprises the Extended Gale-Shapley Algorithm to find the man-optimal stable matching and woman-optimal stable matching and then the minimal differences algorithm and digraph creator which allows us to output all stable matchings of an instance. Correctness testers are also provided which allow us to check that all stable matchings found are indeed stable, and to check that all stable matchings are found, using an Integer Program (IP).


******************************

# 2) software and data

You must have Java and Python installed on your computer to run all programs and 
PuLP and CPLEX installed to run the IP program.

For PuLP installation please follow the guide at:
https://pythonhosted.org/PuLP/main/installing_pulp_at_home.html

For CPLEX installation follow the guide at: 
https://www.ibm.com/support/knowledgecenter/de/SSSA5P_12.6.1/ilog.odms.studio.help/Optimization_Studio/topics/COS_installing.html making sure you set the $PATH and $LD_LIBRARY_PATH environment variables.

Download / git clone the stable-SM software from Github:
https://github.com/fmcooper/stable-SM


Data and software information can be found in the following paper: 
Two-sided profile-based optimality in the stable marriage problem
Authors: Frances Cooper and David Manlove

* The paper is located at: https://arxiv.org/abs/1905.06626
* The data is located at: https://doi.org/10.5281/zenodo.2542703
* The software is located at: https://doi.org/10.5281/zenodo.2545798


******************************

# 3) compiling and running an example

If you are on a mac computer, cd into the stable-SM directory and then run the following command:

```bash
$ source ./runExample.sh
```

This will compile and run an example (found in the "examples" directory) through all the required steps. Note that the default example to run can be found at "examples/DM_pg91/example.txt", which is the SM instance originally described in Irving, Leather and Gusfield's 1987 paper, "An Efficient Algorithm for the “Optimal” Stable Marriage". Results for the example may then be found in the "examples/DM_pg91" directory.

If you are on linux, open the "runExample.sh" file and change the timeout command from "gtimeout" to "timeout". Then proceed as above.

Notes
* There are several variables that may be changed in this script including the timeout command, timeout time, java classpath and location of the example. For more information please see the script.
* If you get CPLEX errors at this point then you will need to check you have followed all installation instructions above. Also ensure that your path variables have been correctly exported by running "$ echo $PATH" etc. 
* If you wish to run algorithms separately, please see the script for an example of how they are called.
* If you do not want to run the IP correctness testing, please comment out this section of the script.
* If you change the timeout time and want to accurately gain statistical results on the time taken then you will also need to change the time out time in the "stats/pythonStats.py" program.



******************************

# 4) interpreting results files

Once the above example has been run, there will be four results files created in the "examples/DM_pg91" directory alongside the example.txt instance file.

* resultsGS_notSwapped.txt: This is the results file after the Extended Gale-Shapley Algorithm has been run to find the man-optimal stable matching. It comprises an instance with reduced preference lists (that may be reinput into the program if required), statistics on the algorithm's performance and the man-optimal stable matching.
* resultsGS_swapped.txt: This is the results file after the Extended Gale-Shapley Algorithm has been run to find the woman-optimal stable matching. It comprises an instance with reduced preference lists (that may be reinput into the program if required), statistics on the algorithm's performance and the woman-optimal stable matching.
* stableMatchings.txt: This file lists and gives statistics on all rotations and stable matchings of the instance.The index of stable matching for the rank-maximal, generous, sex_equal, egalitarian and median stable matchings are given, and well as the digraph, simple digraph and algorithm statistics.
* correctness.txt: This file gives the number of stable matchings found by the algorithm above, and the number that have passed different correctness tests. If using the IP correctness testing, it will also have a list of all stable matchings found by the IP as well as statistics on the algorithm's performance.




******************************

# 5) running multiple instances - preparation

The file "userOptions.txt" lists all instances to be created and run over. The syntax required for each line of this file is:

```
experimentName <numMen>-<minPrefListLength>-<maxPrefListLength>-<skew> <numInstances> <c/nc (correctness testing tag)>
```

As an example, the following line would indicate that we want to create an experiment "S10", with 1000 instances, 10 men, 10 women, preference lists of length 10 and a uniform distribution. It also shows that we want to run IP correctness testing on these instances.

```
S10 10-10-10-0 1000 c
```

Notes
* If lines are removed or added from "userOptions.txt", you will need to update the overall statistics collators "stats/pythonCorrectness.py" and "stats/pythonStats.py".
* The example "userOptions.txt" file gives 19 experiments of varying size with just two instances of each type to shorten the running time.


******************************

# 6) running multiple instances

Running these experiments will overwrite any current instances in your "Evaluations" directory so please ensure you have backed up any experiments you would like to keep before running again.

If you are on a mac computer, cd into the stable-SM directory and then run the following command:

```bash
$ source ./runExperiments.sh
```

This will compile, generate instances and run instances through all the required steps. Results for instance ".../Evaluations/exp/Instances/x.txt" of experiment type "exp" may then be found in at the following locations:
* ".../Evaluations/exp/ResultsGS_notSwapped/x.txt"
* ".../Evaluations/exp/ResultsGS_Swapped/x.txt"
* ".../Evaluations/exp/Results_stable/x.txt"
* ".../Evaluations/exp/Correctness/x.txt"
Summaries of all experiments can be found in the "stats/tempCorrectnessResults" and "stats/tempStatsResults" directories.

If you are on linux, open the "runExperiments.sh" file and change the timeout command from "gtimeout" to "timeout". Then proceed as above.

Notes
* There are several variables that may be changed in this script including the timeout command, timeout time, correctness timeout time, location of results, java classpath, java garbage collection options, java heap space per operation and number of jobs to run simultaneously. For more information please see the script.


******************************

# 7) motivation experiments

Additional motivation experiments were added in version 1.0.2. These comprise the scripts: 

* ``userOptsMotivation.txt`` specifies the additional instances to be created.
* ``runMotivation.sh`` which runs additional instances sizes according to ``userOptsMotivation.txt`` finding and saving rotations for these given instances.

Results for motivation experiments can be found in the ``stats/motivation`` directory. 

Currently collection of results is disabled in the ``stats/motivation.py`` file. This is because data for the larger results (instances sizes 2000, 3000, 4000 and 5000) are not present in the ``Evaluations`` directory (they are available in the linked dataset DOI). However, results are already collected in ``stats/motivation/avstats.txt``. This allows you to perform analysis on the data without that data being present. Run the following command to perform the analysis:

```
python stats/motivation.py ./Evaluations/
```

******************************

# 7) versions

V1.0.3
* added functionality to create graphs found in associated paper
* ``stats/tempStatsResults/avstats.txt`` file now contains stats for all data up to n = 1000
* README updated

V1.0.2
* added functionality to perform motivation experiments and analysis
* README updated

V1.0.1
* README updated

******************************

This readme is based on a readme for a previous project found here: https://doi.org/10.5281/zenodo.1183221

