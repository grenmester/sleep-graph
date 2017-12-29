.PHONY: all
all:
	python parse.py

.PHONY: clean
clean:
	rm -f output.md
	rm -f time-output.md
