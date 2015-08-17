This script gets a list of Aleph Bib Numbers and OCLC numbers for those Aleph Bib Numbers

Next, it checks against worldcat to see if an advanced search for the OCLC number returns the passed number. If it returns a different number, the implication is that the OCLC number passed has been merged. We would want to update our local catalog with the surviving OCLC number.

The complication is that the surviving OCLC number may already be in our catalog so we'd create a duplicate for that OCLC number. So, we check against the union catalog to see if an OCLC number search for the surviving OCLC number returns any good results. If not, then we can update the OCLC (manually). If it does return results, then we'd need to sort out the duplicate issue.

The FLVC Union Catalog URL used is:
http://union.catalog.fcla.edu/ux.jsp?fl=bo&st='+str(goodOCLCNum)+'&ix=nu&S=0921439321283054&fl=bo

The WorldCat URL used is:
http://www.worldcat.org/search?q=no%3A'+str(oclcNum)+'&qt=advanced&dblist=638

as a note, if for any reason the FLVC value can't be converted to an integer, we assume it is part of the DDA program and so not actually in the catalog.

please contact me with any questions at @EthanDF on Twitter or via this account. My work email is fenichele AT fau DOT EDU