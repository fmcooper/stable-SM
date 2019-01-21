package code;
import java.util.ArrayList;

/**
 * <p> This class represents the model of an SM instance. </p>
 *
 * @author Frances
 */
public class Model {   
	/** <p> Information string - output to results file </p> */
	private String infoString;

	/** <p> The number of proposers in an instance </p> */
	private int numProposers;
	/** <p> An array of Person proposers </p> */
	private Person[] proposers;
	/** <p> An array of Person receivers </p> */
	private Person[] receivers;

	/** <p> proposer assignment results </p> */
	private int[] proposerAssignments;
	/** <p> List of rotations for this instance. </p>*/
	private ArrayList<Rotation> rotations;
	/** <p> List of all stable matchings of the instance. </p>*/
	private ArrayList<Matching> stableMatchings;
	/** <p> Indexes of Optimal Stable Matchings. </p>*/
	private int opt_rankMaximal;
	private int opt_generous;
	private int opt_sexEqual;
	private int opt_egalitarian;
	private int opt_generalisedMedian;

	/** <p> 2D array of type 1 labels for women in mens lists (used to create digraph) </p> */
	private int[][] mensListType1Labels;
	/** <p> 2D array of type 2 labels for women in mens lists (used to create digraph) </p> */
	private int[][] mensListType2Labels;
	/** <p> List of rotations for this instance. </p>*/
	private int[][][] digraph;
	private ArrayList<ArrayList<Integer>> simpleDigraph;

	/** <p> Stores when an instance run took place. </p> */
	public String timeAndDate;


	/**
	 * <p> Constructor for the Model class - sets the instance variables. </p>
	 * @param numProposers		
	 * @param proposersPrefs 
	 * @param receiversPrefs
	 */
	public Model(int numProposers, int[][] proposersPrefs, int[][] receiversPrefs) {
		// instantiate the instance variables
		this.numProposers = numProposers;
		proposers = new Person[numProposers];
		receivers = new Person[numProposers];
		int[][] proposersRankLists = new int[numProposers][numProposers];
		int[][] receiversRankLists = new int[numProposers][numProposers];
		for (int i = 0; i < numProposers; i++) {
			for (int j = 0; j < numProposers; j++) {
				proposersRankLists[i][j] = -1;
				receiversRankLists[i][j] = -1;
			}
		}

		proposerAssignments = new int[numProposers];

		// creating proposers
		for (int i = 0; i < numProposers; i++) {
			proposers[i] = new Person(i, null, null);
		}

		// creating receivers
		for (int i = 0; i < numProposers; i++) {
			int[] prefListInt = receiversPrefs[i];
			ArrayList<Person> prefList = new ArrayList<Person>();
			for (int j = 0; j < prefListInt.length; j++) {
				int propInd = prefListInt[j];
				receiversRankLists[i][propInd] = j;
				prefList.add(proposers[propInd]);
			}
			receivers[i] = new Person(i, prefList, receiversRankLists[i]);
		}

		// adding preference list to proposers
		for (int i = 0; i < numProposers; i++) {
			int[] prefListInt = proposersPrefs[i];
			ArrayList<Person> prefList = new ArrayList<Person>();
			for (int j = 0; j < prefListInt.length; j++) {
				int recInd = prefListInt[j];
				proposersRankLists[i][recInd] = j;
				prefList.add(receivers[recInd]);
			}
			proposers[i].setPreferenceList(prefList);
			proposers[i].setRankList(proposersRankLists[i]);
		}

		// add the preference list and rank lists that are not to be changed to each agent
		// (this allows easy refreshing of the preference and rank lists)
		for (int i = 0; i < numProposers; i++) {
			int[] noChangesPreferenceListProp = new int[proposersPrefs[i].length];
			for (int j = 0; j < proposersPrefs[i].length; j++) {
				noChangesPreferenceListProp[j] = proposersPrefs[i][j];
			}

			int[] noChangesRankListProp = new int[proposersRankLists[i].length];
			for (int j = 0; j < proposersRankLists[i].length; j++) {
				noChangesRankListProp[j] = proposersRankLists[i][j];
			}

			int[] noChangesPreferenceListRec = new int[receiversPrefs[i].length];
			for (int j = 0; j < receiversPrefs[i].length; j++) {
				noChangesPreferenceListRec[j] = receiversPrefs[i][j];
			}

			int[] noChangesRankListRec = new int[receiversRankLists[i].length];
			for (int j = 0; j < receiversRankLists[i].length; j++) {
				noChangesRankListRec[j] = receiversRankLists[i][j];
			}

			proposers[i].setNoChangesPreferenceList(noChangesPreferenceListProp);
			proposers[i].setNoChangesRankList(noChangesRankListProp);
			receivers[i].setNoChangesPreferenceList(noChangesPreferenceListRec);
			receivers[i].setNoChangesRankList(noChangesRankListRec);
		}

		rotations = new ArrayList<Rotation>();
		stableMatchings = new ArrayList<Matching>();

		opt_rankMaximal = -1;
		opt_generous = -1;
		opt_sexEqual = -1;
		opt_egalitarian = -1;
		opt_generalisedMedian = -1;

		mensListType1Labels = new int [numProposers][numProposers];
		mensListType2Labels = new int [numProposers][numProposers];
		

		infoString = "";
		timeAndDate = "";
	}




	/*******************************************************************************
	/*******************************************************************************
	/*******************************************************************************
	// Once rotations have been found and saved these methods provide the functionality 
	// to return all stable matchings.
	/*******************************************************************************
	/*******************************************************************************
	/*******************************************************************************

	/**
	 * <p> Save all stable matchings to the stableMatchings instance variable. </p>
	 */
	public void getAllStableMatchings() {
		createSimpleDigraph();

		// find number of incoming edges to each rotation in the digraph
		int[] predecessorCount = new int[rotations.size()];
		for (int i = 0; i < simpleDigraph.size(); i++) {
			ArrayList<Integer> row = simpleDigraph.get(i);
			for (int j = 0; j < row.size(); j++) {
				predecessorCount[row.get(j)]++;
			}
		}

		// save list of rotations with no incoming edges
		ArrayList<Integer> rotationsWithoutPredecessor = new ArrayList<Integer>();
		for (int i = 0; i < predecessorCount.length; i++) {
			if (predecessorCount[i] == 0) {
				rotationsWithoutPredecessor.add(i);
			}
		}

		// no need to relabel rotations as they are labelled in topological order from the minimal
		// differences algorithm
		// save M_0 and start recursion over digraph from each starter node (with no incoming edges)
		int[] stableMatching = new int[numProposers];
		for (int i = 0; i < numProposers; i++) {
			stableMatching[i] = proposerAssignments[i];
		}
		addStableMatching(stableMatching);

		for (int rotation : rotationsWithoutPredecessor) {
			findStableRecursive(stableMatching, rotation, rotationsWithoutPredecessor, predecessorCount);

		}
	}


	/**
	 * <p> Recursive: saves a stable matching. </p>
	 * @param stableMatching 			the current stable matching
	 * @param currentRotation 			the rotation to eliminate
	 * @param rotationsWithoutPredecessor 			rotations to eliminate
	 * @param predecessorCount			the number of predecessors for a rotation
	 */
	private void findStableRecursive(int[] stableMatching, int currentRotation, ArrayList<Integer> rotationsWithoutPredecessor, int[] predecessorCount) {
		if (rotationsWithoutPredecessor.size() != 0) {
			
			int[] copySM = deepCopy(stableMatching);
			copySM = eliminateRotation(copySM, rotations.get(currentRotation));
			addStableMatching(copySM);

			ArrayList<Integer> copyRWP = deepCopy(rotationsWithoutPredecessor);

			copyRWP.remove(Integer.valueOf(currentRotation));

		// update the predecessor counts - if any are 0 then add rotation to copyRWP
			int[] copyPC = deepCopy(predecessorCount);

			ArrayList<Integer> sdChildren = simpleDigraph.get(currentRotation);
			for (int i = 0; i < sdChildren.size(); i++) {
				copyPC[sdChildren.get(i)]--;
				if (copyPC[sdChildren.get(i)] == 0) {
					copyRWP.add(sdChildren.get(i));
				}
			}
			
			// recurse
			for (int rwp : copyRWP) {
				if (rwp > currentRotation) {
					findStableRecursive(copySM, rwp, copyRWP, copyPC);
				}
			}
		}
	}


	/**
	* <p> Adds a stable matching to the stable matching list. </p>
	* @param matching
	*/
	public void addStableMatching(int[] matching) {
		int[] profileMen = calcProfile(matching, OptsProfile.proposerView);
		int[] profileWomen = calcProfile(matching, OptsProfile.receiverView);
		int[] profile = calcProfile(matching, OptsProfile.combinedView);
		int costMen = calcCost(matching, OptsProfile.proposerView);
		int costWomen = calcCost(matching, OptsProfile.receiverView);
		int cost = calcCost(matching, OptsProfile.combinedView);

		stableMatchings.add(new Matching(matching, profileMen, profileWomen, profile, costMen, costWomen, cost));
	}


	/**
	 * <p> Given an input matching and a rotation, returns the new matching found by eliminating
	 * the rotation in the input matching. </p>
	 * @param matching
	 * @param r
	 * 
	 * @return new matching
	 */
	private int[] eliminateRotation(int[] matching, Rotation r) {
		ArrayList<Person[]> rotation = r.getRotation();
		for (int i = 0; i < rotation.size(); i++) {
			int thisManIndex = rotation.get(i)[0].getIdIndex();
			int nextWomanIndex = -1;
			if (i == rotation.size() - 1) {
				nextWomanIndex = rotation.get(0)[1].getIdIndex();
			}
			else {
				nextWomanIndex = rotation.get(i + 1)[1].getIdIndex();
			}
			matching[thisManIndex] = nextWomanIndex;
		}

		return matching;
	}


	/** 
	* <p> Retrieves the man assigned to the first woman on m's list such that w strictly prefers m to their partner in Mi. </p> 
	* @param man
	* @param matchingMi
	*
	* @return man
	*/
	public Person getNextM(Person man, int[] matchingMi) {
		Person womanS = getS(man, matchingMi);
		if (womanS == null) {
			System.out.println("womanS: null!");
		}
		for (int i = 0; i < matchingMi.length; i++) {
			if (matchingMi[i] == womanS.getIdIndex()) {
				return proposers[i];
			}
		}
		return null;
	} 


	/** 
	* <p> Retrieves the first woman on m's list such that w strictly prefers m to their partner in Mi. </p> 
	* @param man
	* @param matchingMi
	*
	* @return woman
	*/
	public Person getS(Person man, int[] matchingMi) {
		boolean passedAssignedWoman = false;
		int index = 0;
		ArrayList<Person> prefList = man.getPreferenceList();
		while(index < prefList.size()) {
			Person currentWoman = prefList.get(index);
			// check if current woman would prefer to be with this man than with their current partner
			if (passedAssignedWoman) {
				if (currentWoman.getRank(getAssignedForWoman(currentWoman,matchingMi)) > currentWoman.getRank(man)) {
					return currentWoman;
				}
			}
			// check if have passed the current assigned woman
			if (currentWoman == getAssignedForMan(man, matchingMi)) { // shallow compare
				passedAssignedWoman = true;
			}
			index++;
		}
		return null;
	}


	/** 
	* <p> Returns the assignment for a given woman in the given matching. </p> 
	* @param w
	* @param matchingMi
	*
	* @return man assigned to the given woman
	*/
	public Person getAssignedForWoman(Person w, int[] matchingMi) {
		for (int i = 0; i < matchingMi.length; i++) {
			if (matchingMi[i] == w.getIdIndex()) {
				return proposers[i];
			}
		}
		return null;
	}


	/** 
	* <p> Returns the assignment for a given man in the given matching. </p> 
	* @param m
	* @param matchingMi
	*
	* @return woman assigned to the given man
	*/
	public Person getAssignedForMan(Person m, int[] matchingMi) {
		return receivers[matchingMi[m.getIdIndex()]];
	}




	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/
	// Methods associated with digraph (after all rotations have been found)
	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/

	/**
	 * <p> Instantiates the rotation poset digraph. </p>
	 * @param numRotations
	 */
	public void instantiateDigraph(int numRotations) {
		digraph = new int[numRotations][numRotations][2];
	}


	/**
	 * <p> Adds an edge to the rotation poset digraph. </p>
	 * @param from 		from this rotation
	 * @param to 		to this rotation
	 * @param type 		type of rotation
	 */
	public void addDigraphEdge(int from, int to, int type) {
		digraph[from - 1][to - 1][type - 1] = 1;
	}



	/**
	 * <p> Creates the simple digraph representation (where each ij element is an edge) from the larger digraph. </p>
	 */
	public void createSimpleDigraph() {
		simpleDigraph = new ArrayList<ArrayList<Integer>>();
		for (int i = 0; i < digraph.length; i++) {
			simpleDigraph.add(new ArrayList<Integer>());
			for (int j = 0; j < digraph[i].length; j++) {
				int type1 = digraph[i][j][0];
				int type2 = digraph[i][j][1];
				if (type1 != 0 || type2 != 0) {
					simpleDigraph.get(i).add(j);
				}
			}
		}
	}



	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/
	// Methods associated with finding optimal stable matchings
	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/

	/** 
	* <p> Assigns which stable matchings are optimal. </p> 
	*/
	public void findStableOptimals() {
		int bestRmSoFar = 0;
		int bestGenSoFar = 0;
		int bestSexEqSoFar = 0;
		int bestEgalSoFar = 0;
		for (int i = 1; i < stableMatchings.size(); i++) {
			if (compareRM(stableMatchings.get(i), stableMatchings.get(bestRmSoFar))) {
				bestRmSoFar = i;
			}
			if (compareGen(stableMatchings.get(i), stableMatchings.get(bestGenSoFar))) {
				bestGenSoFar = i;
			}
			if (compareSexEq(stableMatchings.get(i), stableMatchings.get(bestSexEqSoFar))) {
				bestSexEqSoFar = i;
			}
			if (compareEgal(stableMatchings.get(i), stableMatchings.get(bestEgalSoFar))) {
				bestEgalSoFar = i;
			}
		}
		opt_rankMaximal = bestRmSoFar;
		opt_generous = bestGenSoFar;
		opt_sexEqual = bestSexEqSoFar;
		opt_egalitarian = bestEgalSoFar;
		opt_generalisedMedian = getMedian(stableMatchings);
	}


	/**
	* Compare two matchings rank-maximally and returns true if 1st dominates 2nd.
	* Both matching arrays must be of the same length.
	* @param first matching
	* @param second matching
	*
	* @return true if 1st dominates 2nd
	*/
	public boolean compareRM(Matching first, Matching second) {
		int[] firstProfile = first.getProfile();
		int[] secondProfile = second.getProfile();
		for (int i = 0; i < firstProfile.length; i++) {
			if (firstProfile[i] > secondProfile[i]) {
				return true;
			}
			else if (firstProfile[i] < secondProfile[i]) {
				return false;
			}
		}
		return false;
	}


	/**
	* Compare two matchings generous-ly and returns true if 1st dominates 2nd.
	* Both matching arrays must be of the same length.
	* @param first matching
	* @param second matching
	*
	* @return true if 1st dominates 2nd
	*/
	public boolean compareGen(Matching first, Matching second) {
		int[] firstProfile = first.getProfile();
		int[] secondProfile = second.getProfile();
		for (int i = firstProfile.length - 1; i >= 0; i--) {
			if (firstProfile[i] < secondProfile[i]) {
				return true;
			}
			else if (firstProfile[i] > secondProfile[i]) {
				return false;
			}
		}
		return false;
	}


	/**
	* Compare two matchings in a 'sex equal' way and returns true if 1st dominates 2nd.
	* Both matching arrays must be of the same length.
	* @param first matching
	* @param second matching
	*
	* @return true if 1st dominates 2nd
	*/
	public boolean compareSexEq(Matching first, Matching second) {
		if (first.getSexEqualCost() < second.getSexEqualCost()) {
			return true;
		}
		return false;
	}


	/**
	* Compare two matchings by their egalitarian weight function and returns true if 1st dominates 2nd.
	* Both matching arrays must be of the same length.
	* @param first matching
	* @param second matching
	*
	* @return true if 1st dominates 2nd
	*/
	public boolean compareEgal(Matching first, Matching second) {
		if (first.getCost() < second.getCost()) {
			return true;
		}
		return false;
	}


	/**
	* Returns the stable matching index of the median.
	* @param all stable matchings
	*
	* @return index of the median
	*/
	public int getMedian(ArrayList<Matching> stableMatchings) {
		// counts of woman w_j on man m_i's lists
		int[][] counts = new int[numProposers][numProposers];
		for (Matching sm : stableMatchings) {
			for (int i = 0; i < sm.getMatching().length; i++) {
				counts[i][sm.getMatching()[i]]++;	
			}
		}

		int[][] genMedTable = new int[numProposers][stableMatchings.size()];
		int currentIndexInGenMedTable = 0;
		// iterate over the mens preferences adding the women from counts in order of preference
		for (int man = 0; man < numProposers; man++) {
			currentIndexInGenMedTable = 0;
			for (int womanIndex = 0; womanIndex < numProposers; womanIndex++) {
				int countForThisWoman = counts[man][proposers[man].getPreferenceListPersonAt(womanIndex).getIdIndex()];

				// add to the Generalized median table
				for (int i = 0; i < countForThisWoman; i++) {
					genMedTable[man][currentIndexInGenMedTable] = proposers[man].getPreferenceListPersonAt(womanIndex).getIdIndex();
					currentIndexInGenMedTable++;
				}
			}
		}

		// if there are an odd number of stable matchings then take the middle one of the genMedTable
		int[] generalisedMed = new int[numProposers];
		if (stableMatchings.size() % 2 == 1) {
			int middleIndex = (stableMatchings.size() / 2);
			for (int j = 0; j < generalisedMed.length; j++) {
				generalisedMed[j] = genMedTable[j][middleIndex];
			}
		}
		else {
			int middleIndex = (stableMatchings.size() / 2) - 1;	// taking the 'left' generalised median
			for (int j = 0; j < generalisedMed.length; j++) {
				generalisedMed[j] = genMedTable[j][middleIndex];
			}
		}
		return getStableMatchingIndex(generalisedMed);
	}


	/**
	* <p> Returns the stable matching index of the given matching. </p>
	* @param matching
	*
	* @return index of the given matching
	*/
	public int getStableMatchingIndex(int[] matching) {
		for (int i = 0; i < stableMatchings.size(); i++) {
			Matching stableMatching = stableMatchings.get(i);
			boolean found = true;
			for (int j = 0; j < stableMatching.getMatching().length; j++) {
				if (stableMatching.getMatching()[j] != matching[j]) {
					found = false; 	// could optimise this - use a while loop
				}
			}
			if (found == true) {
				return i;
			}
		}
		return -1;
	}


	/**
	 * <p> Returns the profile of the given matching. </p>
	 * @param matching
	 * @param indicator (whether looking from propower, reciever or both view)
	 * 
	 * @return the profile of the matching
	 */
	public int[] calcProfile(int[] matching, OptsProfile indicator) {
		int[] profile = new int[numProposers];
		for (int i = 0; i < numProposers; i++) {
			if (matching[i] != -1) {
				// proposer view
				if (indicator == OptsProfile.proposerView) {
					int rank = proposers[i].getRank(receivers[matching[i]]);
					profile[rank - 1]++;
				}
				// receiver view
				else if (indicator == OptsProfile.receiverView) {
					int rank = receivers[matching[i]].getRank(proposers[i]);
					profile[rank - 1]++;
				}
				// combined view
				else if (indicator == OptsProfile.combinedView) {
					int rank = proposers[i].getRank(receivers[matching[i]]);
					profile[rank - 1]++;
					rank = receivers[matching[i]].getRank(proposers[i]);
					profile[rank - 1]++;
				}
			}
		}
		return profile;
	}


	/**
	 * <p> Returns the cost of the given matching. </p>
	 * @param matching
	 * @param indicator (whether looking from propower, reciever or both view)
	 *
	 * @return the cost of the matching
	 */
	public int calcCost(int[] matching, OptsProfile indicator) {
		int cost = 0;
		for (int i = 0; i < numProposers; i++) {
			if (matching[i] != -1) {
				// proposer view
				if (indicator == OptsProfile.proposerView) {
					int rank = proposers[i].getRank(receivers[matching[i]]);
					cost += rank;
				}
				// receiver view
				else if (indicator == OptsProfile.receiverView) {
					int rank = receivers[matching[i]].getRank(proposers[i]);
					cost += rank;
				}
				// combined view
				else if (indicator == OptsProfile.combinedView) {
					int rank = proposers[i].getRank(receivers[matching[i]]);
					cost += rank;
					rank = receivers[matching[i]].getRank(proposers[i]);
					cost += rank;
				}
			}
		}
		return cost;
	}


	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/
	// Methods associated with output
	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/


	/**
	 * <p>Returns a representation of the model that can be reinput into the program.</p>
	 * @param swap indicates whether the proposers and receivers are to be swapped
	 *
	 * @return a reuseable SM instance
	 */
	public String getUseableInstance(boolean swap) {
		String returnString = "" + numProposers + "\n";

		String props = "";
		for (int i = 0; i < numProposers; i++) {
			props += proposers[i].getId() + ": ";
			ArrayList<Person> prefList = proposers[i].getPreferenceList();
			for (int j = 0; j < prefList.size(); j++) {
				int rank = proposers[i].getRankList()[prefList.get(j).getIdIndex()];
				if (rank != -1) {
					props += prefList.get(j).getId() + " ";
				}
			}
			props += "\n";
		}

		String recs = "";
		for (int i = 0; i < numProposers; i++) {
			recs += receivers[i].getId() + ": ";
			ArrayList<Person> prefList = receivers[i].getPreferenceList();
			for (int j = 0; j < prefList.size(); j++) {
				int rank = receivers[i].getRankList()[prefList.get(j).getIdIndex()];
				if (rank != -1) {
					recs += prefList.get(j).getId() + " ";
				}
			}
			recs += "\n";
		}

		if (swap) {
			return returnString + recs + props;
		}
		return returnString + props + recs;
	}


	/**
	 * <p> Returns a string if there is no matching found. </p>
	 * @return no matching found string
	 */
	public String getNoMatchingResult() {
		String returnString = "";

		// add time and date information
		returnString += timeAndDate;

		// add a String to indicate that no matching was found
		returnString += "No matching found.";

		return returnString;
	}


	/**
	 * <p> Returns a vertical string of the assigned values. </p>
	 * @return a vertical string of assigned values
	 */
	public String getRawResults() {
		String returnString = "";
		for (int i = 0; i < proposerAssignments.length; i++) {
			returnString += proposerAssignments[i] + " ";
		}

		return returnString;
	}


	/**
	 * <p> Returns a string list of all stable matchings of the instance. </p>
	 * @return rotations
	 */
	public String getResults() {
		getAllStableMatchings();
		findStableOptimals();

		// String s = getUseableInstance(false) +"\n\n";

		String s = "// General stats\n";
		s += "numRotations: " + rotations.size() + "\n";
		s += "numStableMatchings: " + stableMatchings.size() + "\n\n\n";

		s += "// Rotations\n";
		for (int i = 0; i < rotations.size(); i++) {
			Rotation r = rotations.get(i);
			s += r.getString(i) + "\n";
			s += "rotProfileMen_" + i + ": " + rotationProfileChange(i, OptsProfile.proposerView) + "\n";
			s += "rotProfileWomen_" + i + ": " + rotationProfileChange(i, OptsProfile.receiverView) + "\n";
			s += "rotProfileCombined_" + i + ": " + rotationProfileChange(i, OptsProfile.combinedView) + "\n --- \n";
		}

		s += "\n\n// Stable matchings\n";
		s += "// found using rotations not digraph\n\n";

		s += "optimal_stable_matchings: \n";
		s += "rank-maximal_index: " + opt_rankMaximal + "\n";
		s += "generous_index: " + opt_generous + "\n";
		s += "sex_equal_index: " + opt_sexEqual + "\n";
		s += "egalitarian_index: " + opt_egalitarian + "\n";
		s += "generalisedMedian_index: " + opt_generalisedMedian + "\n\n";

		s += "stable_matching_list:\n";
		for (Matching sm : stableMatchings) {
			s += sm.stringOfArray(sm.getMatching(), true) + "\n";
		}

		s += "\n\n";
		for (int i = 0; i < stableMatchings.size(); i++) {
			Matching matching = stableMatchings.get(i);
			s += matching.getString(i) + "\n --- \n";
		}

		s += getDigraphInfo() + "\n\n";

		return s;
	}


	/**
	 * <p> Returns the profile of the matching. </p>
	 * @param matching
	 * @param indicator
	 *
	 * @return the profile of the matching
	 */
	public String getMatchingProfile(int[] matching, OptsProfile indicator) {
		int[] profile = calcProfile(matching, indicator);
		String stringProfile = "< ";
		for (int i = 0; i < profile.length; i++) {
			stringProfile += profile[i] + " ";
		}
		stringProfile += ">";
		return stringProfile;
	}


	/**
	 * <p> Get combined profile change of a rotation. </p>
	 * @param stableMatching
	 *
	 * @return the profile of the rotation
	 */
	private String rotationProfileChange(int rotation, OptsProfile indicator) {
		int[] profile = calcProfileChange(rotation, indicator);
		String stringProfile = "";
		for (int i = 0; i < profile.length; i++) {
			stringProfile += profile[i] + " ";
		}
		return stringProfile;
	}


	/**
	 * <p> Get combined profile change of a rotation. </p>
	 * @param stableMatching
	 *
	 * @return the profile of the rotation
	 */
	private int[] calcProfileChange(int rotation, OptsProfile indicator) {
		int[] profile = new int[numProposers];
		ArrayList<Person[]> thisRotation = rotations.get(rotation).getRotation();
		for (int i = 0; i < thisRotation.size(); i++) {
			int thisManIndex = thisRotation.get(i)[0].getIdIndex();
			int thisWomanIndex = thisRotation.get(i)[1].getIdIndex();
			int nextWomanIndex = -1;
			int nextManIndex = -1;
			if (i == thisRotation.size() - 1) {
				nextManIndex = thisRotation.get(0)[0].getIdIndex();
				nextWomanIndex = thisRotation.get(0)[1].getIdIndex();
			}
			else {
				nextManIndex = thisRotation.get(i + 1)[0].getIdIndex();
				nextWomanIndex = thisRotation.get(i + 1)[1].getIdIndex();
			}
			
			// proposer view
			if (indicator == OptsProfile.proposerView) {
				// rank of current partner minus rank of next partner
				int rankCurrent = proposers[thisManIndex].getRank(receivers[thisWomanIndex]);
				int rankNew = proposers[thisManIndex].getRank(receivers[nextWomanIndex]);
				profile[rankCurrent - 1]--;
				profile[rankNew - 1]++;
			}
			// receiver view
			else if (indicator == OptsProfile.receiverView) {
				int rankCurrent = receivers[nextWomanIndex].getRank(proposers[nextManIndex]);
				int rankNew = receivers[nextWomanIndex].getRank(proposers[thisManIndex]);
				profile[rankCurrent - 1]--;
				profile[rankNew - 1]++;
			}
			// combined view
			else if (indicator == OptsProfile.combinedView) {
				// prop view
				int rankCurrent = proposers[thisManIndex].getRank(receivers[thisWomanIndex]);
				int rankNew = proposers[thisManIndex].getRank(receivers[nextWomanIndex]);
				profile[rankCurrent - 1]--;
				profile[rankNew - 1]++;

				// rec view
				rankCurrent = receivers[nextWomanIndex].getRank(proposers[nextManIndex]);
				rankNew = receivers[nextWomanIndex].getRank(proposers[thisManIndex]);
				profile[rankCurrent - 1]--;
				profile[rankNew - 1]++;
			}
		}
		return profile;
	}


	/**
	 * <p> Returns a string representation of the rotation poset of the instance. </p>
	 * @return rotations
	 */
	public String getDigraphInfo() {
		String s = "Digraph \n";
		for (int i = 0; i < digraph.length; i++) {
			int[][] row = digraph[i];
			for (int j = 0; j < row.length; j++) {
				s += "(" + digraph[i][j][0] + "," + digraph[i][j][1] + ") ";

			}
			s += "\n";
		}

		s += "\nSimple digraph \n";
		for (ArrayList<Integer> row : simpleDigraph) {
			for (int elem : row) {
				s += elem + " ";
			}
			s += "\n";
		}
		return s;
	}


	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/
	// Getters, setters and instance changers
	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/

	public int getNumProposers() {return numProposers;}
	public Person[] getProposers() {return proposers;}
	public Person getProposer(int i) {return proposers[i];}
	public Person getReceiver(int i) {return receivers[i];}
	public Person[] getReceivers() {return receivers;}
	public ArrayList<Rotation> getRotations() {return rotations;}
	public int[] getProposerAssignments() {return proposerAssignments;}
	public int[][] getMensListType1Labels() {return mensListType1Labels;}
	public int[][] getMensListType2Labels() {return mensListType2Labels;}
	public int[][][] getDigraph() {return digraph;}
	public int[] getProposerAssignmentsSwitched() {
		// create switched array and initialise to -1 for each entry
		int[] switched = new int[numProposers]; 
		for (int i = 0; i < numProposers; i++) {
			switched[i] = -1;
		}

		// add results to switched array
		for (int i = 0; i < numProposers; i++) {
			if (proposerAssignments[i] != -1) {
				switched[proposerAssignments[i]] = i;
			}
		}
		return switched;
	}


	public void setProposerAssignments(int[] proposerAssignments) {this.proposerAssignments = proposerAssignments;}
	public void setMensListType1Label(int manIndex, int womanIndex, int label) {mensListType1Labels[manIndex][womanIndex] = label;}
	public void setMensListType2Label(int manIndex, int womanIndex, int label) {mensListType2Labels[manIndex][womanIndex] = label;}	


	/**
	 * <p> Sets agents and refreshes rotations and type list object pointers. </p>
	 */
	public void setAndRefreshAgents(Person[] props, Person[] recs) {
		proposers = props;
		receivers = recs;
		for (Rotation r : rotations) {
			ArrayList<Person[]> listInvolved = r.getRotation();
			for (Person[] p : listInvolved) {
				p[0] = proposers[p[0].getIdIndex()];
				p[1] = proposers[p[1].getIdIndex()];
			}
		}

	}


	/**
	 * <p> Swaps proposers and receivers around. </p>
	 */
	public void swapProposer() {
		Person[] tempProp = receivers;
		receivers = proposers;
		proposers = tempProp;
	}


	/**
	 * <p> Set the assignment information. </p>
	 */
	public void setAssignmentInfo() {
		for (int i = 0; i < proposerAssignments.length; i++) {
			int recInd = proposerAssignments[i];
			if (recInd != -1) {
				proposers[i].setAssigned(receivers[recInd]);
				receivers[recInd].setAssigned(proposers[i]);
			}
		}
	}


	/**
	 * <p> Refreshes the Person lists with refreshed rank lists. </p>
	 */
	public void refreshAgentLists() {
		for (int i = 0; i < numProposers; i++) {
			proposers[i].refreshLists(receivers);
			receivers[i].refreshLists(proposers);
		}
	}


	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/
	// Utilities
	/*******************************************************************************/
	/*******************************************************************************/
	/*******************************************************************************/


	/**
	 * <p> Performs a deep copy of an int array. </p>
	 * @param array to copy
	 * @return copied array
	 */
	private int[] deepCopy(int[] array) {
		int[] copy = new int[array.length];
		for (int i = 0; i < array.length; i++) {
			copy[i] = array[i];
		}
		return copy;
	}


	/**
	 * <p> Performs a deep copy of an int ArrayList. </p>
	 * @param array to copy
	 * @return copied array
	 */
	private ArrayList<Integer> deepCopy(ArrayList<Integer> array) {
		ArrayList<Integer> copy = new ArrayList<Integer>();
		for (int i = 0; i < array.size(); i++) {
			copy.add(array.get(i));
		}
		return copy;
	}


	/**
	 * <p> Print the model. </p>
	 */
	public void print() {
		System.out.println("proposers");
		for (Person p : proposers) {
			System.out.println(p);
		}
		System.out.println("receivers");
		for (Person p : receivers) {
			System.out.println(p);
		}
	}


	/**
	 * <p> Prints IDs in a Person array. </p>
	 */
	public void print(Person[] pArray, String message) {
		System.out.println("\n" + message);
		for (int i = 0; i < pArray.length; i++) {
			System.out.print(pArray[i].getId() + " ");
		}
		System.out.println("\n");
	}


	/**
	 * <p> Print an int[][]. </p>
	 * @param intArray
	 * @param message
	 * @param adding1
	 */
	private void print(int[][] intArray, String message, boolean adding1) {
		String s = message + "\n";

		for (int[] row : intArray) {
			for (int cell : row) {
				int val = cell;
				if (adding1) {
					val++;
				}
				s += val + " ";
			}
			s += "\n";
		}
		System.out.println(s);
	}


	/**
	 * <p> Print an int[]. </p>
	 * @param intArray
	 * @param message
	 * @param adding1
	 */
	public void print(int[] intArray, String message, boolean adding1) {
		String s = message + "\n";

		for (int cell : intArray) {
			int val = cell;
			if (adding1) {
				val++;
			}
			s += val + " ";  
		}
		s += "\n";
		System.out.println(s);
	}
}
