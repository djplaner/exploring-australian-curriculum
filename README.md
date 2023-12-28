# Exploring the Australian Curriculum

The [Australian Curriculum](https://australiancurriculum.edu.au/) specifies what Australian students from the Foundation year to Year 10 should be taught. It is a complex set of information shared via a fairly usable website. To truly understand and leverage the Australian Curriculum teachers and schools need to integrate its content into their daily activity. Not a straight forward process.

This project has three initial goals:

1. Explore how the Australian Curriculum can be made more [generative](https://djplaner.github.io/memex/sense/nodt/generativity/).
2. Offer a purposeful reason to explore different [Python](https://www.python.org/) based technologies in service of that goal.
3. Explore various useful applications of a generative Australian Curriculum to teachers and schools.

For more see [the project's design page](https://djplaner.github.io/memex/sense/Python/exploring-australian-curriculum/)

## Useful outputs

Late December 2023 see the first main "useful" output. An integration of the Australian Curriculum data into an instance of [the Foam personal knowledge management tool](https://foambubble.github.io/). A set of Python classes (see the `src` folder) were created to parse RDF files from the Australian Curriculum site and generate a set of markdown files as expected by Foam and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) (the static site generation used by this version of Foam). 

[The result](https://djplaner.github.io/memex/sense/Teaching/Curriculum/v9/v9-learning-areas/) is a set of pages that can be used to explore the Australian Curriculum in a more generative manner.

## Next steps?

- [X] Generating Python class for manipulating the Australian Curriculum structures
- [ ] Explore other uses of the classes as I start teaching
- [ ] Explore how the approach used by [WebGlossary.info](https://webglossary.info/) might be integrated with memex


## Current Status

| Date | Progress |
| --- | --- |
| [27 Aug 2023](https://djplaner.github.io/memex/sense/Python/exploring-oz-curriculum/001-exploring-oz-dev-log/) | Initial experiments with Datasette (generate and explore sqlite database with v8.4 curriculum) and Streamlit (initial experiment using that database). |
| [24 Sep 2023](https://djplaner.github.io/memex/sense/Python/exploring-oz-curriculum/002-exploring-oz-dev-log/) | Pondering what to do with the v9 Australian Curriculum. Discovering that the use of RDF/semantic web etc has complicated the reusability. Barrier to entry quite high. Many connections. |
| [Nov 2023](https://djplaner.github.io/memex/sense/Python/exploring-oz-curriculum/003-exploring-oz-dev-log/) | Failed experiments with Neo4J |
| [Early Dec 2023](https://djplaner.github.io/memex/sense/Python/exploring-oz-curriculum/004-exploring-oz-dev-log/) | Coming to grips with using `rdflib` to recurse the structure | 
| [Late Dec 2023](https://djplaner.github.io/memex/sense/Python/exploring-oz-curriculum/005-exploring-oz-dev-log/) | Python classes parsing AC Learning Area RDF files and generating [markdown pages used by Foam](https://djplaner.github.io/memex/sense/Teaching/Curriculum/v9/v9-learning-areas/) |



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