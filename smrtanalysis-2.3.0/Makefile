HGAP_CUTOFF=7800

space :=
space +=

CPUS=4

all : quiver.fasta

.SECONDARY :

.PHONY : clean

quiver.fasta : data/polished_assembly.fasta.gz
	gunzip -c $< | sed 's/|quiver//' > $@

data/polished_assembly.fasta.gz : input.xml HGAP_Assembly_Advanced.2.xml
	. $(SMRT_ROOT)/current/etc/setup.sh && smrtpipe.py --distribute --params=$(word 2,$^) xml:$<

input.xml : input.start.fofn
	. $(SMRT_ROOT)/current/etc/setup.sh && fofnToSmrtpipeInput.py $< > $@

ifeq ($(KEEP_VECTOR), true)
HGAP_Assembly_Advanced.2.xml :
	sed 's/HGAP_CUTOFF/$(HGAP_CUTOFF)/' $(MAKEDIR)/HGAP_Assembly_Advanced.2.xml.vector.template > $@
else
HGAP_Assembly_Advanced.2.xml : whitelist.txt
	sed 's#ABSOLUTE_PATH#$(shell pwd)#' $(MAKEDIR)/HGAP_Assembly_Advanced.2.xml.template \
		| sed 's/HGAP_CUTOFF/$(HGAP_CUTOFF)/' > $@

whitelist.txt : vector.align input.start.fofn
	. $(SMRT_ROOT)/current/etc/setup.sh && python $(MAKEDIR)/whitelist.py $^ > $@

vector.align : input.start.fofn
	 qsub -sync y -cwd -N screen_vector -q all.q -pe serial $(CPUS) -l mfree=3G -S /bin/bash $(MAKEDIR)/screen_vector.sh $(MAKEDIR) $< $@ $(CPUS)
endif

clean :
	rm -f filtered_longreads.fasta* index* metadata.rdf noop quiver.fasta toc.xml variants.* align* smrt.lock seeds* HGAP_Assembly_Advanced.2.xml
	rm -rf data/ log/ movie_metadata/ reference/ results/ workflow/ corrected*
