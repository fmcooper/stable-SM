package code;
import java.util.ArrayList;


/**
 * <p> Person object, characterising men and women. </p>
 *
 * @author Frances
 */
public class Person {

	/** <p> Preference list of this person </p> */
	private ArrayList<Person> preferenceList;
	/** <p> Preference list index </p> */
	private int currentPrefIndex;
	/** <p> Person ID </p> */
	private int id;
	/** <p> Person ID index = Person ID - 1 </p> */
	private int idIndex;
	/** <p> Preferences held as a rank list </p> */
	private int[] rankList;
	/** <p> This persons assigned partner </p> */
	private Person assigned;
	/** <p> A tag used in the minimal differences algorithm </p> */
	private boolean mark;

	/** <p> Copies of the original preference and rank list </p> */
	private int[] noChangesPreferenceList;
	private int[] noChangesRankList;


	/**
	 * <p> Constructor - sets the instance variables. </p>
	 * @param idIndex		
	 * @param preferenceList 
	 * @param rankList
	 */
	public Person(int idIndex, ArrayList<Person> preferenceList, int[] rankList) {
		this.preferenceList = preferenceList;
		this.idIndex = idIndex;
		this.id = idIndex + 1;
		this.currentPrefIndex = -1;
		assigned = null;
		this.rankList = rankList;
		mark = false;
	}


	/**
	 * <p> Refreshes preference and rank lists. </p>
	 * @param 
	 */
	public void refreshLists(Person[] otherAgentList) {
		// refresh preference list
		ArrayList<Person> newPrefList = new ArrayList<Person>();
		for (int i = 0; i < noChangesPreferenceList.length; i++) {
			newPrefList.add(otherAgentList[noChangesPreferenceList[i]]);
		}
		preferenceList = newPrefList;

		// refresh rank list
		int[] newRankList = new int[noChangesRankList.length];
		for (int i = 0; i < noChangesRankList.length; i++) {
			newRankList[i] = noChangesRankList[i];
		}
		rankList = newRankList;
	}

	
	/**
	 * <p> Returns the next preference list Person according to the preference list index. </p>
	 *
	 * @return next person
	 */
	public Person getNextReceiver() {
	 	currentPrefIndex ++;
	 	if (preferenceList.size() <= currentPrefIndex);
	 	return preferenceList.get(currentPrefIndex);
	}


	/**
	 * <p> Returns whether this person likes the given person more than their currently assigned person. </p>
	 * @param proposer
	 *
	 * @return prefers
	 */
	public boolean likes(Person proposer) {
		if (getRank(proposer) == 0) {
			return false;
		}
		if (assigned == null) {
			return true;
		}
		return getRank(proposer) < getRank(assigned);
	}


	/**
	 * <p> Returns the rank of the given person. </p>
	 * @param other
	 *
	 * @return rank
	 */
	public int getRank(Person other) {
		return rankList[other.idIndex] + 1;
	}


	/**
	 * <p> Removes worse proposers from just after the assigned person in preference list. </p>
	 */
	public void removeWorseProposers() {
		int toDelFrom = rankList[assigned.getIdIndex()] + 1;
		int lengthPrefListOrig = preferenceList.size();

		for (int i = toDelFrom; i < lengthPrefListOrig; i++) {
			Person personToDelete = preferenceList.get(toDelFrom);

			// remove from rank lists
			rankList[personToDelete.getIdIndex()] = -1;
			personToDelete.getRankList()[this.getIdIndex()] = -1;

			// remove from preference list
			preferenceList.remove(toDelFrom);
		}
	}


	/**
	 * <p> Removes worse proposers from just after the given person in preference list. 
	 * Also, removes this person from that preference list as well. </p>
	 * @param person
	 */
	public void removeWorseProposersMD(Person man) {
		int toDelFrom = rankList[man.getIdIndex()] + 1;
		int lengthPrefListOrig = preferenceList.size();

		for (int i = toDelFrom; i < lengthPrefListOrig; i++) {
			Person personToDelete = preferenceList.get(toDelFrom);

			// remove from rank lists
			rankList[personToDelete.getIdIndex()] = -1;
			personToDelete.getRankList()[this.getIdIndex()] = -1;
			//System.out.println("     removing " + personToDelete.getId());

			// remove from preference list
			preferenceList.remove(toDelFrom);
			personToDelete.getPreferenceList().remove(this);
		}
	}


	/**
	 * <p> Removes the given person from the preference list. Could be made faster. </p>
	 */
	public void remove(Person p) {
		for (int i = 0; i < preferenceList.size(); i++) {
			if (preferenceList.get(i) == p) {
				preferenceList.remove(i);
			}
		}
	}


	/**
	 * <p> Getters and setters. </p>
	 */
	public ArrayList<Person> getPreferenceList() {return preferenceList;}
	public Person getPreferenceListPersonAt(int id) {return preferenceList.get(id);}
	public int[] getRankList() {return rankList;}
	public Person getAssigned() {return assigned;}
	public int getIdIndex() {return idIndex;}
	public int getId() {return id;}
	public int getCurrentPrefIndex() {return currentPrefIndex;}
	public boolean getMark() {return mark;}
	public void setPreferenceList(ArrayList<Person> prefList) {preferenceList = prefList;}
	public void setRankList(int[] rankList) {this.rankList = rankList;}
	public void setAssigned(Person assigned) {this.assigned = assigned;}
	public void mark() {mark = true;}
	public void unmark() {mark = false;}
	public void setCurrentPrefIndex(int currentPrefIndex) {this.currentPrefIndex = currentPrefIndex;}
	public void setNoChangesPreferenceList(int[] prefList) {this.noChangesPreferenceList = prefList;}
	public void setNoChangesRankList(int[] rankList) {this.noChangesRankList = rankList;}
	

	/**
	 * <p> Utilities. </p>
	 */
	public String toString() {
		String s = "" + id + ":";
		for (Person p : preferenceList) {
			s += " " + p.getId();
		}
		return s;
	}
}
