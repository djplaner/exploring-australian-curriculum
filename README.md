# Exploring the Australian Curriculum

The [Australian Curriculum](https://australiancurriculum.edu.au/) specifies what Australian students from the Foundation year to Year 10 should be taught. It is a complex set of information shared via a fairly usable website. To truly understand and leverage the Australian Curriculum teachers and schools need to integrate its content into their daily activity. Not a straight forward process.

This project has three initial goals:

1. Explore how the Australian Curriculum can be made more [generative](https://djplaner.github.io/memex/sense/nodt/generativity/).
2. Offer a purposeful reason to explore different [Python](https://www.python.org/) based technologies in service of that goal.
3. Explore various useful applications of a generative Australian Curriculum to teachers and schools.

## What might some useful applications be?

### Making connections between disconnected learning areas

Boaler (2015) argues

> Curriculum standards often work against connection making, as they present mathematics as a list of disconnected topics. But teachers can and should restore the connections by always talking about and valuing them and asking students to think about and discuss connections. (p. 184)

What interfaces might help enable this connection making? To enable the necessary gathering and weaving?

### Making connections in general

Boaler (2015) also offers [a collection of norms/advice](https://djplaner.github.io/memex/sense/Teaching/Mathematics/teaching-mathematics-for-a-growth-mindset/#opening-mathematics) to help teach mathematics. In theory, something like this (or other pedagogical/other frameworks) could also be useful in terms of connections with/to/from the curriculum and its components.

Question being how to enable ad hoc connection maps between the different components in the curriculum? For separate purposes.

Perhaps the very essence of gather/weave.





## Current Status

| Date | Progress |
| --- | --- |
| 27 Aug 2023 | Initial experiments with Datasette (generate and explore sqlite database with v8.4 curriculum) and Streamlit (initial experiment using that database). |



## Use

1. Set up virtual env.

    `source env/bin/activate`

2. Install requirements.

    `pip install -r requirements.txt`

3. Create database 

    ```bash
    cd datasette
    sh generate.sh
    ```

4. Run datasette and follow instructions
   
    `datasette curriculum.db`


## References

Boaler, J., & Dweck, C. (2015). *Mathematical Mindsets: Unleashing Students' Potential Through Creative Math, Inspiring Messages and Innovative Teaching*. John Wiley & Sons, Incorporated.