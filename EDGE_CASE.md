# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) For the get stats function, getting stats from a database with no students would result in a divide by zero error when calculating the average mark (sum of all marks / number of marks)
2) I account for this by checking for how many marks are in the mark list of all student marks and if the length of this array is 0, then there are no student marks or even students in the database to which I force output stat values of 0 and none for all stats.