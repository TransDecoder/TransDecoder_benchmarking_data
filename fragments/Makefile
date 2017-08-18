

ORGS=a_thaliana d_melanogaster m_musculus s_pombe

analyze:
	@for i in $(ORGS); do \
    echo "Running example in $$i..."; \
    (cd $$i; $(MAKE) analyze) || exit $$?; done

clean:
	@for i in $(ORGS); do \
    echo "Running example in $$i..."; \
    (cd $$i; $(MAKE) clean) || exit $$?; done
