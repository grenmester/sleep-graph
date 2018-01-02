# Sleep Graph

Plots your sleep data so you can visualize how much and when you sleep.

### Usage

Run the following commands.

    make
    python -m SimpleHTTPServer

You should now be able to view the graph at `localhost:8000`. We use `python -m
SimpleHTTPServer` to view the graph since d3 can't open `file://` extensions.
