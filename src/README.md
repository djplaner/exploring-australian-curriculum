<!--
 Copyright (C) 2023 David Jones
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.
 
 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->

# Australian Curriculum class hierarchy

These are the Python classes that I use to parse RDF files provided by [the Australian Curriculum site](https://v9.australiancurriculum.edu.au/machine-readable-australian-curriculum).

See the [memex folder](../memex/) for some source code using these classes for a real purpose.

## Introduction

You start by creating an `australianCurriculum` object. You then add RDF files (currently it only works on _learning area_ RDF files) to it using the `addRdfFile` method. 

```python
   ac = australianCurriculum()

    for file in args.rdffile:
        ac.addRdfFile(file)
```

The `australianCurriculum` object then provides "pythonic" access to all the standard Australian Curriculum objects. The following table summarises and also demonstrates the simple hierarchy that exists. Each AC object has a matching Python class.

| AC Object | Python Class| Description |
| --- | --- | --- |
| Learning Area | `acLearningArea` | One of the [8 learning areas](https://v9.australiancurriculum.edu.au/f-10-curriculum/f-10-curriculum-overview/learning-areas) (e.g. Mathematics, Technologies) |
| Subject | `acSubject` | Every learning area includes subjects. Some only have one (e.g. Mathematics, English) and others have multiple (e.g. Technologies, Humanities and Social Sciences) |
| Year level | `acYearLevel` | Each subject is then divided into year (grade) levels (or bands), each year level (band) contains the following components |
| Description | Attribute of `acYearLevel` | An overview of the expected learning experience for the year level |
| Achievement Standards | `acAchievementStandard` | A list describing the expected quality of learning students should be able to demonstrate by the end of the year level | 
| Strands and Sub-strands | `acStrand` & `acSubStrand` | The content descriptions for a subject/year level are divided further into either strands or strands/sub-strands |
| Content Descriptions | `acContentDescription` | A list of specific knowledge, understanding and skills students will learn |
| Content elaborations | `acElaboration` | Additional suggestions/illustrations of how to teach particular content descriptions |
| Achievement standard components | `acAchievementStandardComponent` | The achievement standard broken up into separate components and associated with specific content descriptions |

The remaining classes are

- `acAustralianCurriculum` - the top level object that contains all the learning areas and is responsible for parsing the RDF files and constructing the Python data structures
- `acNode` - the base class for all the other classes
