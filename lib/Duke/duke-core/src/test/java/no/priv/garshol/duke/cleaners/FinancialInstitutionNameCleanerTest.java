package no.priv.garshol.duke.cleaners;
import org.junit.Before;
import org.junit.Test;

import static junit.framework.Assert.assertEquals;

public class FinancialInstitutionNameCleanerTest {

	
	 private FinancialInstitutionNameCleaner cleaner;
	  
	  @Before
	  public void setup() {
	    cleaner = new FinancialInstitutionNameCleaner();
	  }
	  
	  @Test
	  public void testEmpty() {
	    test("","");
	  }
	  
	  @Test
	  public void testIncorporated() {
	    test("Enrico bank inc", "Enrico bank incorporated");
	  }
     
	  @Test
	  public void testNationalAssociation() {
	    test("Enrico na", "Enrico national association");
	  }
	  
	  @Test
	  public void testFederalSavingBank() {
	    test("Enrico fsb", "Enrico federal saving bank");
	    
	  }
	  
	  @Test
	  public void testCorporation() {
	    test("Enrico corp", "Enrico corporation");
	    
	  }
	  
	  private void test(String s1, String s2) {
		    s1.equals(cleaner.clean(s2));
		  }

	
	
}
