package correctness;
import java.io.*;
import java.util.*;
import java.math.*;
import code.*;


/**
 *	<p>Tests the stability of an SM instance result (depending on tag may also test that
 * all stable matchings are found using an IP). </p>
 *
 * @author Frances
 */

public class Main_Tester {
	/**<p>The model of the instance.</p>*/
	private static Model model;
	private static ArrayList<int[]> stableMatchings;



	/**
	* <p> Help message. </p>
	*/
	public static void helpAndExit() {
		System.out.println();
		System.out.println("This class tests that the results file is a stable matching that adheres to upper and lower quotas");
		System.out.println("If a true tag is given then will also check that all stable matchings are found using an IP.");
		System.out.println();
		System.out.println("Using this program:");
		System.out.println("$ java Main_Tester [-h] <instance file name> <results file name> <true/false (IP tag)>");
		System.out.println();
		System.exit(0);
	}


	/**
	* <p> Main method. </p>
	*/
	public static void main(String args[]) {
		// input
		String instinput = "";
		String resinput = "";
		File instf = null;
		File resf = null;
		boolean bruteForce = false;
		try {
			instinput = args[0];
			resinput = args[1];
			String bfString = args[2];

			if (instinput.equals("-h") || resinput.equals("-h") || (!bfString.equals("true") && !bfString.equals("false"))) {
				helpAndExit();
			}
			else {
				if (bfString.equals("true")) {
					bruteForce = true;
				}
			}

			instf = new File(instinput);
			resf = new File(resinput);
		}
		catch (Exception e) {
			System.out.println("Input error");
			helpAndExit();
		}

		// check for upstream issue
		boolean upstream = Util_FileIO.upstreamTimeout(instf) || Util_FileIO.upstreamTimeout(resf);
		if (upstream) {
			System.exit(4);
		}

		// create the model
		model = Util_FileIO.readFile(instf);

		// set the assignments in the model from the results file
		stableMatchings = Util_FileIO.inputAllStable(resf);

		if (model == null || stableMatchings == null) {
			System.exit(3);
		}

		else {
			// for each potential stable matching perform correctness tests
			int numPassedAcceptability = 0;
			int numPassedCapacity = 0;
			int numPassedStability = 0;

			for (int smInd = 0; smInd < stableMatchings.size(); smInd++) {
				int[] sm = stableMatchings.get(smInd);
				model.setProposerAssignments(sm);
				model.setAssignmentInfo();

				if (checkAcceptability(model)) {
					numPassedAcceptability++;
				}
				if (checkCapacity(model)) {
					numPassedCapacity++;
				}
				if (checkStable(model)) {
					numPassedStability++;
				}
			}

			// set the time and date instance variable in the model
			Util_FileIO.createCal();
			String easyResults = Util_FileIO.getCal(false) + "\n";
			model.timeAndDate = easyResults;


			// check correctness and output
			System.out.println("\nStable_correctness_tests: " + easyResults);
			System.out.println("Stable_numStableMatchings: " + stableMatchings.size());
			System.out.println("Stable_numPassedAcceptability: " + numPassedAcceptability);
			System.out.println("Stable_numPassedCapacity: " + numPassedCapacity);
			System.out.println("Stable_numPassedStability: " + numPassedStability);

			// bruteForce then output the number of stable matchings found by brute force
			if (bruteForce) {
				BigInteger startTimeBF = new BigInteger("" + System.currentTimeMillis());
				System.out.println("");
				System.out.println("NumFound_bruteForce: " + getNumStable());
				BigInteger endTimeBF = new BigInteger("" + System.currentTimeMillis());
				BigInteger timeTakenBF = endTimeBF.subtract(startTimeBF);
				System.out.println("Duration_bruteForce_ms: " + timeTakenBF);
			}

		}
	}


	/**
	 * <p>Checks that the man and women pairs find each other acceptable.</p>
	 * @param model
	 * @return if all agents have acceptable partners
	 */
	public static boolean checkAcceptability(Model model) {
		for (int i = 0; i < model.getProposerAssignments().length; i++) {
			if (model.getProposerAssignments()[i] != -1) {
				int propInd = i;
				int recInd = model.getProposerAssignments()[i];
				if (model.getReceivers()[recInd].getRankList()[propInd] == -1) {
					return false;
				}
			}	
		}
		return true;
	}


	/**
	 * <p>Checks that the assignment adheres to upper and lower quotas.</p>
	 * @return if the assignment adheres to upper and lower quotas
	 */
	public static boolean checkCapacity(Model model) {
		boolean[] recAssigned = new boolean[model.getNumProposers()];
		for (int i = 0; i < model.getProposerAssignments().length; i++) {
			if (model.getProposerAssignments()[i] != -1) {
				if (recAssigned[model.getProposerAssignments()[i]] == true) {
					return false;
				}
				recAssigned[model.getProposerAssignments()[i]] = true;
			}
		}
		return true;
	}


	/**
	 * <p>Checks that the assignment is stable.</p>
	 * @return if the assignment is stable
	 */
	public static boolean checkStable(Model model) {
		// assume stable until proven otherwise
		boolean isStable = true;

		// for each proposer
		for (int propInd = 0; propInd < model.getProposerAssignments().length; propInd++) {
			// find the project assignment and lecturer assignment
			int receiver = model.getProposerAssignments()[propInd];
			int[] propRankList = model.getProposers()[propInd].getRankList();
			int rank = -1;
			if (receiver != -1) {
				rank = propRankList[receiver];
			}

			// for all student project pairs in the students preference list decide whether it is a blocking pair
			ArrayList<Person> propPrefList = model.getProposers()[propInd].getPreferenceList();
			for (int prefInd = 0; prefInd < rank; prefInd++) {
				int recInd = propPrefList.get(prefInd).getIdIndex();
				if (model.getReceivers()[recInd].likes(model.getProposers()[propInd])) {
					isStable = false;
					// System.out.println("** blocking");
					// System.err.println("** blocking");
				}
			}
		}
		return isStable;
	}


	/**
	 * <p>Returns the number of stable matchings in an instance found by brute force.</p>
	 * @return number of stable matchings
	 */
	public static int getNumStable() {
		// initialise the matching to test to take a value of 1 for every element
		int[] matchingToTest = new int[model.getNumProposers()];
		for (int i = 0; i < matchingToTest.length; i++) {
			matchingToTest[i] = 0;
		}

		boolean completed = false;
		int numStableMatchings = 0;

		// test all possible matchings
		while(!completed) {
			model.setProposerAssignments(matchingToTest);
			model.setAssignmentInfo();

			boolean acc = checkAcceptability(model);
			boolean cap = checkCapacity(model);
			boolean sta = checkStable(model);

			if (acc && cap && sta) {
				numStableMatchings ++;
			}
			completed = addOne(matchingToTest);
		}
		
		return numStableMatchings;
	}


	/**
	 * <p>Helper method for the brute force method to return the number of stable matchings.
	 * Returns the matching with 1 added when viewed as a number. </p>
	 * @return whether it is possible to add 1 to the matching when viewed as a number
	 */
	public static boolean addOne(int[] matching) {
		boolean allFull = true;
		for (int i = 0; i < matching.length; i++) {
			if (matching[i] < matching.length - 1) {
				allFull = false;
			}
		}
		// if all matching elements are at their maximum then return true
		if (allFull) {
			return true;
		}

		boolean added = false;
		for (int i = matching.length - 1; i >= 0; i--) {
			if (!added) {
				if (matching[i] != matching.length - 1) {
					matching[i]++;
					added = true;
				}
				else {
					matching[i] = 0;
				}
			}
		}
		return false;
	}
}
