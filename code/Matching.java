package code;
import java.util.ArrayList;

/**
 * <p> This class represents the matching in an SMI instance. </p>
 *
 * @author Frances
 */
public class Matching {  
	/** <p> Matching represented by receiver indices. </p>*/ 
	private int[] matching;
	/** <p> Proposer profile. </p>*/ 
	private int[] profileMen;
	/** <p> Receiver profile. </p>*/ 
	private int[] profileWomen;
	/** <p> Combined profile. </p>*/ 
	private int[] profile;
	/** <p> Egalitarian cost for proposers. </p>*/ 
	private int costMen;
	/** <p> Egalitarian cost for receivers. </p>*/ 
	private int costWomen;
	/** <p> Combined egalitarian cost. </p>*/ 
	private int cost;


	/**
	 * <p> Matching constructor. </p>
	 *
	 * @param matching
	 * @param profileMen
	 * @param profileWomen
	 * @param profile
	 * @param costMen
	 * @param costWomen
	 * @param cost
	 */
	public Matching(int[] matching, int[] profileMen, int[] profileWomen, int[] profile, int costMen, int costWomen, int cost) {
		this.matching = matching;
		this.profileMen = profileMen;
		this.profileWomen = profileWomen;
		this.profile = profile;
		this.costMen = costMen;
		this.costWomen = costWomen;
		this.cost = cost;
	}


	/**
	 * <p> Getters and setters. </p>
	 */
	public int[] getMatching() {return matching;}
	public int[] getProfileMen() {return profileMen;}
	public int[] getProfileWomen() {return profileWomen;}
	public int[] getProfile() {return profile;}
	public int getCostMen() {return costMen;}
	public int getCostWomen() {return costWomen;}
	public int getCost() {return cost;}
	public int getSexEqualCost() {
		if (costMen > costWomen) {
			return costMen - costWomen;
		}
		return costWomen - costMen;
	}
	public void setCostMen(int costMen) {this.costMen = costMen;}
	public void setCostWomen(int costWomen) {this.costWomen = costWomen;}
	public void setCost(int cost) {this.costMen = cost;}



	/**
	 * <p> Output. </p>
	 */
	public String getString(int i) {
		String s = "";
		s += "matching_" + i + ": " + stringOfArray(matching, true) + "\n";
		s += "profileMen_" + i + ": " + stringOfArray(profileMen, false) + "\n";
		s += "profileWomen_" + i + ": " + stringOfArray(profileWomen, false) + "\n";
		s += "profileCombined_" + i + ": " + stringOfArray(profile, false) + "\n";
		s += "costMen_" + i + ": " + costMen + "\n";
		s += "costWomen_" + i + ": " + costWomen + "\n";
		s += "costCombined_" + i + ": " + cost + "\n";
		s += "sexEquality_" + i + ": " + getSexEqualCost() + "\n";
		return s;
	}


	/**
	 * <p> Return the string of an Array. </p>
	 * @param intArray
	 * @param message
	 * @param adding1
	 */
	public String stringOfArray(int[] intArray, boolean adding1) {
		String s = "";

		for (int cell : intArray) {
			int val = cell;
			if (adding1) {
				val++;
			}
			s += val + " ";  
		}
		return s;
	}
}
