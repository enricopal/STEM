
package no.priv.garshol.duke.comparators;

import static junit.framework.Assert.assertEquals;

import org.junit.Before;
import org.junit.Test;

public class XSDDateTimeComparatorTest {
  private XSDDateTimeComparator comp;

  @Before
  public void setup() {
    this.comp = new XSDDateTimeComparator();
  }
  
  // tests for the comparator

  @Test
  public void testComparatorExact() {
    assertEquals(1.0, comp.compare("2016-09-21T12:57:57Z", "2016-09-21T12:57:57Z"));
  }

  @Test
  public void testComparatorWithin6H() {
    assertEquals(1.0, comp.compare("2016-09-21T12:57:57Z", "2016-09-21T13:57:57Z"));
  }

  
  
}