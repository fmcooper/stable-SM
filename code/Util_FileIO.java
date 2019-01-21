package code;
import java.io.*;
import java.util.*;
import java.util.ArrayList;

/**
* <p> This class contains functions to read an SMI instance from a file and crete a Model instance, along
* with other IO functions. </p>
*
* @author Frances
*/
public abstract class Util_FileIO {
	private static Calendar calendar;
	private static int maxPrefLength;

	// cannot be instantiated - this is a utility class
	private Util_FileIO() {
	}


	/**
	* <p> Returns whether the given file contains a timeout. </p>
	* @param file 		the file to input data from
	*/
	public static boolean upstreamTimeout(File file) {
		FileReader fr = null;
		try {
			try {			
				// opens file and create a scanner on that file
				fr = new FileReader (file);
				Scanner scan = new Scanner(fr);
				String line = scan.nextLine();
				if (line.contains("timeout")) {
					return true;
				}
			}
			// closes file if it was successfully opened
			finally {
				if (fr != null) {fr.close();}
			}
		}
		// catches IO exception
		catch (Exception e) {
			// error message if problem with input file
			// suppressed since error is handled as an exit code
			//System.out.println("Error in reading from file: " + file.toString());
		}
		return false;
	}


	/**
	* <p> Input the instance from the file and create a Model. </p>
	* @param file 		the file to input data from
	* @return the created Model instance
	*/
	public static Model readFile(File file) {
		int numProposers = 0;
		int[][] proposersPrefs = new int[1][1];
		int[][] receiversPrefs = new int[1][1];

		FileReader fr = null;
		try {
			try {			
				// opens file and create a scanner on that file
				fr = new FileReader (file);
				Scanner scan = new Scanner(fr);
				// input the number of men
				numProposers = scan.nextInt();
				scan.nextLine();
				proposersPrefs = new int[numProposers][];
				receiversPrefs = new int[numProposers][];

				
				// input men preferences
				for (int i = 0; i < numProposers; i++) {
					String prefListString = scan.nextLine();
					String[] prefSplit = prefListString.split("[ :]+");
					int[] prefList = new int[prefSplit.length - 1];

					for (int j = 1; j < prefSplit.length; j++) {		
						int index = j - 1;	
						prefList[index] = (Integer.parseInt(prefSplit[j]) - 1);
					}
					proposersPrefs[i] = prefList;
				}

				// input women preferences
				for (int i = 0; i < numProposers; i++) {
					String prefListString = scan.nextLine();
					String[] prefSplit = prefListString.split("[ :]+");
					int[] prefList = new int[prefSplit.length - 1];

					for (int j = 1; j < prefSplit.length; j++) {		
						int index = j - 1;	
						prefList[index] = (Integer.parseInt(prefSplit[j]) - 1);
					}
					receiversPrefs[i] = prefList;
				}	

				Model model = new Model(numProposers, proposersPrefs, receiversPrefs);
				return model;
			}
			// closes file if it was successfully opened
			finally {
				if (fr != null) {fr.close();}
			}
		}
		// catches IO exception
		catch (Exception e) {
			// error message if problem with input file
			// suppressed since error is handled as an exit code
			//System.out.println("Error in reading from file: " + file.toString());
		}
		return null;
	}


	/**
	* <p> Input results from a file. </p>
	* @param file 		the file to input results from
	* @return the array of integers representing proposer assignments
	*/
	public static int[] inputRawResult(File file) {
		FileReader fr = null;
		int[] result = new int [0];
		String resultsline = "";
		try {
			try {				
				// opens file and create a scanner on that file
				fr = new FileReader (file);
				Scanner scan = new Scanner(fr);

				boolean found = false;
				
				while (!found) {
					if (scan.hasNextLine()) {
						String line = scan.nextLine();
						String [] lineSplit = line.split(" ");
						if (lineSplit[0].equals("RawResults:")) {
							resultsline = scan.nextLine();
							found = true;
						}
					}
					else {
						break;
					}
				}
				if (!found) {
					return null;
				}
			}

			// closes file if it was successfully opened
			finally {
				if (fr != null) {fr.close();}
			}
		}
		// catches IO exception
		catch (Exception e) {

			// error message if problem with input file
			System.out.println("Error from file: " + file.toString());
		}

		String [] resultslineSplit = resultsline.split(" ");
		result = new int [resultslineSplit.length];

		for (int i = 0; i < resultslineSplit.length; i++) {
			int receiver = Integer.parseInt(resultslineSplit[i]);
			receiver--;
			result[i] = receiver;
		}

		return result;
	}


	/**
	* <p> Input all stable matchings from a file. </p>
	* @param file 		the file to input results from
	* @return stable matchings
	*/
	public static ArrayList<int[]> inputAllStable(File file) {
		FileReader fr = null;
		ArrayList<int[]> matchings = null;
		String resultsline = "";
		try {
			try {				
				// opens file and create a scanner on that file
				fr = new FileReader (file);
				Scanner scan = new Scanner(fr);

				boolean finishedScanning = false;
				while (!finishedScanning) {
					if (scan.hasNextLine()) {
						String line = scan.nextLine();
						if (line.equals("stable_matching_list:")) {
							boolean finishedSMs = false;
							matchings = new ArrayList<int[]>();
							while (!finishedSMs) {
								resultsline = scan.nextLine();
								if (resultsline.equals("")) {
									finishedSMs = true;
									finishedScanning = true;
								}
								else {
									String [] resultslineSplit = resultsline.split(" ");
									int[] result = new int [resultslineSplit.length];

									for (int i = 0; i < resultslineSplit.length; i++) {
										int receiver = Integer.parseInt(resultslineSplit[i]);
										receiver--;
										result[i] = receiver;
									}
									matchings.add(result);
								}
							}
						}
					}
					else {
						break;
					}
				}
			}

			// closes file if it was successfully opened
			finally {
				if (fr != null) {fr.close();}
			}
		}
		// catches IO exception
		catch (Exception e) {

			// error message if problem with input file
			System.out.println("Error from file: " + file.toString());
		}

		return matchings;
	}



	/**
	* <p> Input the number of stable matchings from a file. </p>
	* @param file 		the file to input results from
	* @return number of stable matchings
	*/
	public static int inputNumStable(File file) {
		FileReader fr = null;
		ArrayList<int[]> matchings = new ArrayList<int[]>();
		String resultsline = "";
		try {
			try {				
				// opens file and create a scanner on that file
				fr = new FileReader (file);
				Scanner scan = new Scanner(fr);

				boolean finishedScanning = false;
				while (!finishedScanning) {
					if (scan.hasNextLine()) {
						String line = scan.nextLine();
						String[] lineSpl = line.split("[ \t]+");
						if (lineSpl[0].equals("numStableMatchings:")) {
							return Integer.parseInt(lineSpl[1]);
						}
					}
					else {
						break;
					}
				}
			}

			// closes file if it was successfully opened
			finally {
				if (fr != null) {fr.close();}
			}
		}
		// catches IO exception
		catch (Exception e) {

			// error message if problem with input file
			System.out.println("Error from file: " + file.toString());
		}

		return -1;

	}


	/**
	*<p>Create a calendar object.</p>
	*/
	public static void createCal() {
		calendar = new GregorianCalendar();
	}


	/**
	*<p>Return a short or long version of the calendar's time.</p>
	*/
	public static String getCal(boolean shortCal) {
		int year = calendar.get(Calendar.YEAR);
		int month = calendar.get(Calendar.MONTH) + 1;
		int day = calendar.get(Calendar.DAY_OF_MONTH);
		int hour = calendar.get(Calendar.HOUR_OF_DAY);
		int minute = calendar.get(Calendar.MINUTE);
		int second = calendar.get(Calendar.SECOND);

		if (shortCal) {
			return "" + year + "," + month + "," + day + "_" + hour + "," + minute + "," + second;
		}
		else {
			return "Date: " + year + "/" + month + "/" + day + "  Time: " + hour + ":" + minute + ":" + second;
		}	
	}


	/**
	 * <p> Print an int[][]. </p>
	 * @param intArray
	 * @param message
	 */
		private static void print(int[][] intArray, String message) {
			String s = message + "\n";

			for (int[] row : intArray) {
				for (int cell : row) {
					s += cell + " ";
				}
				s += "\n";
			}
			System.out.println(s);
		}


	/**
	 * <p> Print an int[]. </p>
	 * @param intArray
	 * @param message
	 */
	public static void print(int[] intArray, String message) {
		String s = message + "\n";

		for (int cell : intArray) {
			s += cell + " ";  
		}
		s += "\n";
		System.out.println(s);
	}
}
