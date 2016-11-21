
package no.priv.garshol.duke.comparators;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import no.priv.garshol.duke.Comparator;

/**
 * An implementation of the XSDDateTimeComparator
 * datetimes are expected to be in the format of yyyy-MM-dd'T'HH:mm:ssz
 */
public class XSDDateTimeComparator implements Comparator {
    
    public static final long HOUR = 3600*1000;
    
    @Override
    public double compare(String s1, String s2) {
        return similarity(s1, s2);
    }

    @Override
    public boolean isTokenized() {
        return true; // I guess?
    }

    /**
     * Returns normalized score, with 0.0 meaning no similarity at all,
     * and 1.0 meaning full equality.
     * if d1-6H< d2 < d1+6H 
     */
    public static double similarity(String s1, String s2) {
       
        DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssz");
        
        try {
            Date d1 = df.parse(s1.replaceAll("\\+", "GMT+"));
            Date d2 = df.parse(s2.replaceAll("\\+", "GMT+"));
  
            if( d1.equals(d2) ) return 1.0;
            
            if ( d2.after( new Date(d1.getTime() - 6*HOUR) ) && d2.before(new Date(d1.getTime() + 6*HOUR)))
                return 1;
                        
        } catch (ParseException e) {
            e.printStackTrace();
        }
        
        return 0;
    }

}