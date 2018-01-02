.PHONY: all
all:
	python3 parse.py

.PHONY: clean
clean:
	rm -f output.md
	rm -f time-output.md
