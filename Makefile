NOW=$(shell date +%Y%m%d)

JQVER=1.9.1

floatingbits_$(NOW).zip: floatingbits.html scripts/jquery-$(JQVER).min.js
	zip $@ floatingbits.html scripts/jquery-$(JQVER).min.js
	
