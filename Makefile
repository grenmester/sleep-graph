.PHONY: all
all:
	python3 parse.py
	cp time-output.md bar-graph/data.csv

.PHONY: clean
clean:
	rm -f output.md
	rm -f time-output.md
