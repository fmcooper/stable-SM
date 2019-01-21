package code;
import java.io.*;
import java.util.*;
import java.math.*;

/**
*	Runs a given instance over the Extended Gale-Shapley algorithm. </p>
*
* @author Frances
*/

public class Main_GS {
	/* <p>Start time in milliseconds.</p> */
	static BigInteger startTimeTot;


	/**
	* <p> Help message. </p>
	*/
	public static void helpAndExit() {
		System.out.println();
		System.out.println("This class runs a given instance over the Gale-Shapley algorithm.");
		System.out.println();
		System.out.println("Using this program:");
		System.out.println("$ java Main_GS [-h] <instance file name> <true/false>");
		System.out.println("true or false indicates whether the proposers / receivers are swapped");
		System.out.println();
		System.exit(0);
	}


	/**
	* <p> Main method. Runs a single instance. </p>
	*/
	public static void main(String args[]) {
		startTimeTot = new BigInteger("" + System.currentTimeMillis());

		// input checks
		String fileName = "";
		String swapString = "";
		boolean swap = false;
		File f = null;
		try {
			fileName = args[0];
			f = new File(fileName);
			
			swapString = args[1];
			if (fileName.equals("-h") || swapString.equals("-h") || (!swapString.equals("true") && !swapString.equals("false"))) {
				helpAndExit();
			}
			else {
				if (swapString.equals("true")) {
					swap = true;
				}
			}
		}
		catch (Exception e) {
			System.out.println("Input name error");
			helpAndExit();
		}

		// check for upstream issue
		boolean upstream = Util_FileIO.upstreamTimeout(f);
		if (upstream) {
			System.exit(4);
		}


		// create the model 
		BigInteger startTimeMod = new BigInteger("" + System.currentTimeMillis()); 
		Model model = Util_FileIO.readFile(f);

		if (swap) {
			model.swapProposer();
		}
		
		// set the time and date instance variable in the model
		Util_FileIO.createCal();
		String easyResults = Util_FileIO.getCal(false) + "\n";
		
		model.timeAndDate = easyResults;

		if (model == null) {
			System.out.println("** error: the file " + f.getName() + " is incompatable");
			helpAndExit();
		}
		BigInteger endTimeMod = new BigInteger("" + System.currentTimeMillis());
		BigInteger timeTakenMod = endTimeMod.subtract(startTimeMod);

		// run the approximation algorithm recording start and end times
		BigInteger startTimeAlg = new BigInteger("" + System.currentTimeMillis());
		GaleShapleyExtended alg = new GaleShapleyExtended(model);
		BigInteger endTimeAlg = new BigInteger("" + System.currentTimeMillis());
		BigInteger timeTakenAlg = endTimeAlg.subtract(startTimeAlg);		

		// retrieve results
		BigInteger startTimeRes = new BigInteger("" + System.currentTimeMillis());
		// NOT REQUIRED FOR THIS EXPERIMENT
		BigInteger endTimeRes = new BigInteger("" + System.currentTimeMillis());
		BigInteger timeTakenRes = endTimeRes.subtract(startTimeRes);
		
		// output results
		System.out.println(model.getUseableInstance(swap) + "\n");
		System.out.println("");
		System.out.println("Updated preference list above: can be reinput into program.");
		System.out.println("Duration_ModCreation_milliseconds: " + timeTakenMod);
		System.out.println("Duration_GetSolution_milliseconds: " + timeTakenAlg);
		System.out.println("Duration_CollectRes_milliseconds: " + timeTakenRes + "\n");
		System.out.println("RawResults: \n" + model.getRawResults() + "\n");

		BigInteger endTimeTot = new BigInteger("" + System.currentTimeMillis());
		BigInteger timeTakenTot = endTimeTot.subtract(startTimeTot);
		System.out.println("Duration_Total_milliseconds: " + timeTakenTot + "\n");
	}	
}
