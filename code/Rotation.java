package code;
import java.util.*;

/**
 * <p> Rotation object, characterises a rotation of a matching. </p>
 *
 * @author Frances
 */
public class Rotation {

	/** <p> Preference list of this person </p> */
	private ArrayList<Person[]> rotation;


	/**
	 * <p> Constructor - sets the instance variables. </p>
	 */
	public Rotation() {
		rotation = new ArrayList<Person[]>();
	}


	/**
	 * <p> Adds a man, woman pair to the rotation. </p>
	 * @param man 
	 * @param woman
	 */
	public void add(Person man, Person woman) {
		Person[] couple = {man, woman};
		rotation.add(0, couple);

	}


	/**
	 * <p> Rotate the given matching about this rotation and return the resultant matching. </p>
	 * @param matching
	 */
	public int[] rotate(int[] matching) {
		int firstWoman = rotation.get(0)[1].getIdIndex();
		for (int i = 0; i < rotation.size() - 1; i++) {
			int man = rotation.get(i)[0].getIdIndex();
			int nextwoman = rotation.get(i+1)[1].getIdIndex();
			matching[man] = nextwoman;
		}

		int lastMan = rotation.get(rotation.size() - 1)[0].getIdIndex();
		matching[lastMan] = firstWoman;

		return matching;
	}

	
	/**
	 * <p> Update the preferences of each pair in the rotation. </p>
	 */
	public void updatePrefs() {
		for (int i = 0; i < rotation.size() - 1; i++) {
			Person man = rotation.get(i)[0];
			Person woman = rotation.get(i + 1)[1];

			woman.removeWorseProposersMD(man);
		}
		// first woman last man
		rotation.get(0)[1].removeWorseProposersMD(rotation.get(rotation.size() - 1)[0]);
	}


	/**
	 * <p> Getters. </p>
	 */
	public ArrayList<Person[]> getRotation() {return rotation;}


	/**
	 * <p> Utilities. </p>
	 */
	public String getString(int i) {
		String s = "";
		s += "rotation_" + i + ": ";
		for (int j = 0; j < rotation.size(); j++) {
			Person[] couple = rotation.get(j);
			s += "(" + couple[0].getId() + ", " + couple[1].getId() + ") ";
		}
		return s;
	}
}
