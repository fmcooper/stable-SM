package code;
import java.io.*;
import java.util.*;
import java.math.*;

/**
*	Finds all stable matchings for a given instance. </p>
*
* @author Frances
*/

public class Main_Motivation {
	/* <p>Start time in milliseconds.</p> */
	static BigInteger startTimeTot;


	/**
	* <p> Help message. </p>
	*/
	public static void helpAndExit() {
		System.out.println();
		System.out.println("This class finds all stable matchings for a given instance.");
		System.out.println();
		System.out.println("Using this program:");
		System.out.println("$ java Main_GetStableMatchings [-h] <inst file name> <propOpt file name> <recOpt file name>");
		System.out.println();
		System.exit(0);
	}


	/**
	* <p> Main method. Runs a single instance. </p>
	*/
	public static void main(String args[]) {
		startTimeTot = new BigInteger("" + System.currentTimeMillis());

		// input checks
		String originalFileName = "";
		String prefsFileName = "";
		String manOptFileName = "";
		String womanOptFileName = "";
		File originalFile = null;
		File prefsFile = null;
		File manOptFile = null;
		File womanOptFile = null;
		try {
			originalFileName = args[0];
			manOptFileName = args[1];
			womanOptFileName = args[2];
		
			if (originalFileName.equals("-h") || manOptFileName.equals("-h") || womanOptFileName.equals("-h")) {
				helpAndExit();
			}
			originalFile = new File(originalFileName);
			manOptFile = new File(manOptFileName);
			womanOptFile = new File(womanOptFileName);
		}
		catch (Exception e) {
			System.out.println("Input name error");
			helpAndExit();
		}

		prefsFile = womanOptFile; // take preferences from the GS lists in the womans optimal file as these may be more reduced

		// check for upstream issue
		boolean upstream = Util_FileIO.upstreamTimeout(originalFile) || Util_FileIO.upstreamTimeout(manOptFile) || Util_FileIO.upstreamTimeout(womanOptFile);
		if (upstream) {
			System.exit(4);
		}

		// create the models
		BigInteger startTimeMod = new BigInteger("" + System.currentTimeMillis()); 
		// model 1 for the non reversed instance (man-optimal)
		Model model1 = Util_FileIO.readFile(prefsFile);
		int[] assignments1 = Util_FileIO.inputRawResult(manOptFile);
		model1.setProposerAssignments(assignments1);
		model1.setAssignmentInfo();

		// model2 for the reversed instance (woman-optimal)
		Model model2 = Util_FileIO.readFile(prefsFile);
		model2.swapProposer();
		int[] assignments2 = Util_FileIO.inputRawResult(womanOptFile);
		model2.setProposerAssignments(assignments2);
		model2.setAssignmentInfo();
		
		// set the time and date instance variable in the model
		Util_FileIO.createCal();
		String easyResults = Util_FileIO.getCal(false) + "\n";
		model1.timeAndDate = easyResults;
		model2.timeAndDate = easyResults;

		if (model1 == null || model2 == null) {
			System.exit(3);
		}
		BigInteger endTimeMod = new BigInteger("" + System.currentTimeMillis());
		BigInteger timeTakenMod = endTimeMod.subtract(startTimeMod);

		// run the minimal differences algorithm recording start and end times
		BigInteger startTimeAlg = new BigInteger("" + System.currentTimeMillis());
		MinimalDifferences alg = new MinimalDifferences(model1, model2);

		// reset preferences back to original for stats
		Model modelOriginal = Util_FileIO.readFile(originalFile);
		model1.setAndRefreshAgents(modelOriginal.getProposers(), modelOriginal.getReceivers());
		
		BigInteger endTimeAlg = new BigInteger("" + System.currentTimeMillis());
		BigInteger timeTakenAlg = endTimeAlg.subtract(startTimeAlg);		

		// retrieve results
		BigInteger startTimeRes = new BigInteger("" + System.currentTimeMillis());
		// NOT REQUIRED FOR THIS EXPERIMENT
		BigInteger endTimeRes = new BigInteger("" + System.currentTimeMillis());
		BigInteger timeTakenRes = endTimeRes.subtract(startTimeRes);
		
		// output results
		System.out.println(model1.getResultsWithoutMatchings());
		System.out.println();
		// System.out.println(model1.getDigraphInfo());
		System.out.println("Duration_ModCreation_milliseconds: " + timeTakenMod);
		System.out.println("Duration_GetSolution_milliseconds: " + timeTakenAlg);
		System.out.println("Duration_CollectRes_milliseconds: " + timeTakenRes + "\n");

		BigInteger endTimeTot = new BigInteger("" + System.currentTimeMillis());
		BigInteger timeTakenTot = endTimeTot.subtract(startTimeTot);
		System.out.println("Duration_Total_milliseconds: " + timeTakenTot + "\n");
	}	
}
