"""
Make your own FASTQ files based off of a string
Created by Lilly Shatford-Adams on 12/2/2022 

I wanted a way to create FASTQ files for testing. 
Modify the string, and it will output the normal FASTQ format with high QalityScores
"""
#Header name 
header = "bmp"
#Modify the original String
string = "atgc"
Ustring = string.upper()

#Get Quality Score
qualityScoreList = []
for i in string: 
  replaced = i.replace(i, "I") 
  qualityScoreList.append(replaced)
qualityScore = "".join(qualityScoreList)

#Format like a FASTQ
print (f"@{header}\n{Ustring}\n+\n{qualityScore}")

"""
Does it work?

print ("orig string: ", string)
print ("uppercased: ", Ustring)
print ("with QS: ", qualityScore)
"""