package code;
import java.util.*;


/**
* <p> The minimal differences algorithm to list all rotations of an instance. </p>
* <p> The Stable Marriage Problem - Gusfield and Irving (1989), pg 110. O(n^2) time. </p>
* 
* @author Frances
*/
public class MinimalDifferences {
	/** <p> Model of the instance. </p>*/
	Model model;
	/** <p> Proposer (man) optimal stable matching. </p>*/
	int[] matchingM0;
	/** <p> Receiver (woman) optimal stable matching. </p>*/
	int[] matchingMz;


	/**
	* <p> Constructor. </p>
	* @param first model
	* @param second model
	*/
	public MinimalDifferences(Model model1, Model model2) {
		this.model = model1;
		matchingM0 = model.getProposerAssignments();
		matchingMz = model2.getProposerAssignmentsSwitched();
		run();
	}


	/** <p> Minimal-Differences algorithm. </p> */
	public void run() {
		// creating a stack that will hold men related to a particular rotation
		Stack<Person> st = new Stack<Person>();
		int x = 0; // the current man number
		int numProp = model.getNumProposers();
		int[] matchingMi = new int[numProp]; // the current matching
		for (int index = 0; index < numProp; index++) {
			matchingMi[index] = matchingM0[index];
		}

		// main while loop
		while (x < numProp) {

			// if the stack is empty
			if (st.isEmpty()) {
				// find a man which has a different assignment in M0 and Mz
				while((x < numProp) && (matchingMi[x] == matchingMz[x])) {
					x = x + 1;
				}
				// if we have a man who has a different assignment then push them onto the stack
				if (x < numProp) {
					Person man = model.getProposer(x);
					man.mark();
					st.push(man);
				}
			}

			// if the stack is not empty
			if (!st.isEmpty()) {
				Person firstMan = st.peek();

				// defns on pg 87 of book
				// s is the first woman on m's list such that w strictly prefers m to their partner in Mi
				Person s = model.getS(firstMan, matchingMi);
				
				// get the man that s is currently assigned to
				Person m = model.getAssignedForWoman(s, matchingMi);

				// get all the men who will be involved in this rotation
				while (m.getMark() == false) {
					st.push(m);
					m.mark();
					s = model.getS(m, matchingMi);

					if (s != null) {
						m = model.getAssignedForWoman(s, matchingMi);
					}	
				}
				
				// get the first pair of the rotation
				Person topMan = st.pop();
				topMan.unmark();
				Rotation r = new Rotation();
				r.add(topMan, model.getAssignedForMan(topMan, matchingMi));

				// get the rest of the rotating pairs
				while (topMan != m) {
					topMan = st.pop();
					topMan.unmark();
					r.add(topMan, model.getAssignedForMan(topMan, matchingMi));
				}

				// rotate the current matching by the found rotation
				matchingMi = r.rotate(matchingMi);
				model.getRotations().add(r);
				// update the preference lists after this rotation
				r.updatePrefs();
			}
		}
	}
}
