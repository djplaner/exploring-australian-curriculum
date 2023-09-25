#!/bin/bash
# FILE: generate.sh
# PURPOSE: Use sqlite-utils to convert the CSV files in ../data to a SQLite database
#          with the following tables
#          - content_descriptors - 
#          - elaborations 
#            From CD Elb-Table 1.csv 
#            - establish primary key with content_descriptors
#            - remove elaborations column and LearningArea, Subject, Pathway, Sequence
#              Level, Strand, Substrand, Topic, Depth Study, Elective
#          - learning_areas
#            Same as elaborations, but only remove elaborations column
#          - cross_curriculum_priorities
#          - general_capabilities
#          - achievement_standards
#          
# 

#-- remove any existing database
rm oz_curriculum.db
#-- import the elaborations CSV
echo "Importing elaborations CSV"
sqlite-utils insert oz_curriculum.db elaborations "../data/v8.4/F-10 CD Elb-Table 1.csv" --csv -d

#-- CREATE content_descriptors
echo "\ncreate the content-descriptors table\n"
sqlite-utils extract oz_curriculum.db elaborations CdCode ContentDesc --table content_descriptors
# set the CdCode as the PrimaryKey
echo "\nset the CdCode as the PrimaryKey\n"
sqlite-utils transform oz_curriculum.db content_descriptors --pk CdCode

# CREATE the elaborations table
echo "\nRemake the elaborations table \n"
sqlite-utils drop-table oz_curriculum.db elaborations
# insert it again
sqlite-utils insert oz_curriculum.db elaborations "../data/v8.4/F-10 CD Elb-Table 1.csv" --csv -d
# remove the unnecessary columns Elaboration column
sqlite-utils transform oz_curriculum.db elaborations --drop ContentDesc \
   --drop Elective --drop "Depth Study" --drop Topic --drop Substrand --drop Strand \
    --drop Level --drop Sequence --drop Pathway --drop Subject --drop LearningArea
# modify the CdCode column to be a foreign key to the content_descriptors table
echo "\nMake CdCode the foreign key\n"
sqlite-utils add-foreign-key oz_curriculum.db elaborations CdCode content_descriptors CdCode

# CREATE the learning_areas table
echo "\nCreate learning_areas table \n"
# insert elaboratiosn CSV into learning_areas
sqlite-utils insert oz_curriculum.db learning_areas "../data/v8.4/F-10 CD Elb-Table 1.csv" --csv -d
# remove the unnecessary columns Elaboration column
sqlite-utils transform oz_curriculum.db learning_areas --drop ContentDesc --drop Elaboration
# modify the CdCode column to be a foreign key to the content_descriptors table
echo "\nMake CdCode the foreign key\n"
sqlite-utils add-foreign-key oz_curriculum.db learning_areas CdCode content_descriptors CdCode


#-- achievement_standards
echo "\nImporting achievement_standards CSV"
sqlite-utils insert oz_curriculum.db achievement_standards "../data/v8.4/F-10 AS-Table 1.csv" --csv -d
#-- general_capabilities
echo "\nImporting general_capabilities CSV"
sqlite-utils insert oz_curriculum.db general_capabilities "../data/v8.4/F-10 CD GC tagging-Table 1.csv" --csv -d
sqlite-utils add-foreign-key oz_curriculum.db general_capabilities CdCode content_descriptors CdCode
#-- cross_curriculum_priorities
echo "\nImporting cross_curriculum_priorities CSV"
sqlite-utils insert oz_curriculum.db cross_curriculum_priorities "../data/v8.4/F-10 CD CCP tagging-Table 1.csv" --csv -d
sqlite-utils add-foreign-key oz_curriculum.db cross_curriculum_priorities CdCode content_descriptors CdCode

