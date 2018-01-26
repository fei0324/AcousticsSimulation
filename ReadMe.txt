ReadMe for auto cropping program

1)unzip file to location that you want to run it from
2)open comand line
3)change directory to location you have unzipped it to
4)type "python autoMain.py"
5)enter the information it asks for

each input file should be all the rounds of a recording session for one point.
each out put file should be the recording for a specific point and a specific position.

I set the program to crop the new file at 0.5 second before the signal reached the point at 
which it triggered the program to cut.  This was done because the old recordings had a wide range
of volumes of strikes.  With the pendulum data this 0.5 second delay can be removed.

Input file naming convention:
p1series.wav, p2series.wav, ....

Output file naming convention:
triMr1p1.wav, triMr1p2.wav, .... triMr2p1.wav, triMr2p2, ....


Also:
1) The namming convention can be quickly modified to include recording session number and date
2) An explination of the algorithum for triggering the cut point is included in the 
notes of autocropper.py


