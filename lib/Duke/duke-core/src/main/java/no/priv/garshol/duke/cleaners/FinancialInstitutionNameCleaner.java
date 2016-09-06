package no.priv.garshol.duke.cleaners;

import no.priv.garshol.duke.Cleaner;

//cleaner that removes common abbreviations and acronym in financial institution names

public class FinancialInstitutionNameCleaner implements Cleaner {

	@Override
	public String clean(String value) {
		
	        value = value.replaceAll("\\bco\\b", "company");
            
	        value = value.replaceAll("\\bcorp\\b", "corporation");

	        value = value.replaceAll("\\binc\\b ", "incorporated");
	        
	        value = value.replaceAll("\\binc\\b.", "incorporated");

	        value = value.replaceAll(" f.s.b. ", " federal savings bank ");
	       
	        value = value.replaceAll(" & ", " and ");
	        
	        value = value.replaceAll("\\bna\\b", "national association");
	                    
	        value = value.replaceAll("\\bfsb\\b ", "federal savings bank");

		return value;
	}
	
	

}
