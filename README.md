 <img src="https://i.gyazo.com/800d16eb6795b275ad9fcb403c9e7625.png" height="199" width="721">


# What do I use this for?
This program was meant to assign jobs to a set of people randomly. You can then print out the assigned jobs via an excel or text file. This is faster and fairer than trying to assign jobs manually using pen and paper. A scenario where this program would be useful is assigning house mates in a college dorm weekly clean up jobs.

# How do I run It
You need python installed to run this program. Keep in mind that this program was developed using Python 2.7, but it should function properly on the latest versions of Python. To open the GUI, extract the files to your desired location and run the .py file, **assigner.py**. If you do not want to run the file through the command line every time, you can create a batch file that will do it for you! Below is the code to do that:

    @echo  off
    python "C:\Users\Anthony DeArmas\Desktop\assigner\assigner.py" %*
    pause
    exit
**Note that this example is for having the files in a folder named 'assigner' on my Desktop! You need to replace the file path of the files for it to work for you.**
# Primary features
 - An aesthetic and intuitive user interface
 - The ability to add and remove people and jobs through the menu rather than adding them through the data files
 - Basic data saving so you don't have to type in names every time
 - A 'fair' job assigning algorithm that prevents people from getting assigned the same job every time (despite there being a chance of that happening in reality)


