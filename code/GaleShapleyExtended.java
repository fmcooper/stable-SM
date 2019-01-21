package code;
import java.util.Random;
import java.util.ArrayList;

/**
 * <p> TAlgorithm to find the proposer-oriented stable matching. </p>
 * <p> The Extended Gale Shapley Algorithm - Gusfield and Irving (1989), pg 16. </p>
 * 
 * @author Frances
 *
 */
public class GaleShapleyExtended {

	/** <p>The model instance.</p> */
	private Model model;


	/**
	 * <p> Constructor for the algorithm - runs the algorithm. </p>
	 * 
	 * @param instanceModel
	 */
	public GaleShapleyExtended(Model model) {
		this.model = model;
		run();
	}

	/**
	 * <p> Gale-Shapley algorithm. <\p>
	 * 
	 */
	public void run() {
		Person[] proposers = model.getProposers();

		// set all proposers to be currently ready to propose
		ArrayList<Person> ready = new ArrayList<Person>();
		for (Person proposer : proposers) {
			ready.add(proposer);
		}

		// while there are still proposers left let them propose
		while (ready.size() != 0) {
			Person proposer = ready.remove(0);
			boolean accepted = false;

			// find the next receiver - must accept them in Extended Gale Shapley (or none if they reach end of pref list)
			while(!accepted && proposer.getPreferenceList().size() != proposer.getCurrentPrefIndex() + 1) {
				Person receiver = proposer.getNextReceiver();

				if (receiver.getRankList()[proposer.getIdIndex()] != -1) {
					propose(proposer, receiver, ready);
					accepted = true;
				}
			}
		}

		// add results to the model
		int[] results = model.getProposerAssignments();
		for (int i = 0; i < proposers.length; i++) {
			Person assigned = proposers[i].getAssigned();
			if (assigned == null) {
				results[i] = 0;
			}
			else {
				results[i] = proposers[i].getAssigned().getId();
			}		
		}
	}


	/**
	 * <p> Proposer proposes to receiver. <\p>
	 * @param proposer
	 * @param receiver
	 * @param ready
	 */
	private boolean propose(Person proposer, Person receiver, ArrayList<Person> ready) {
		Person oldProposer = receiver.getAssigned();
		if (oldProposer != null) {
			if (oldProposer.getPreferenceList().size() != oldProposer.getCurrentPrefIndex() + 1) {
				ready.add(receiver.getAssigned());
			}
			oldProposer.setAssigned(null);
		}
		proposer.setAssigned(receiver);
		receiver.setAssigned(proposer);

		// remove worse proposers from the receivers list
		receiver.removeWorseProposers();

		return true;
	}
}
