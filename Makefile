

RUNTYPES=complete fragments

analyze:
	@for i in $(RUNTYPES); do \
    (cd $$i; $(MAKE) analyze) || exit $$?; done

clean:
	@for i in $(RUNTYPES); do \
    (cd $$i; $(MAKE) clean) || exit $$?; done

