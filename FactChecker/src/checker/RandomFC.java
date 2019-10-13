package checker;

import java.util.Random;

public class RandomFC {
	private Random rnd;
	
	public RandomFC() {
		rnd = new Random();
	}
	
	public double checkFact(String subject, String predicate, String object) {
		return rnd.nextDouble()*2-1;
	}
}
