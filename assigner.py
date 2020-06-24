import kivy
import random
import xlsxwriter


from kivy.core.window import Window
from kivy.config import Config

from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty

import webbrowser

"""
The root window of the program.
Primarily responsible for assigning jobs and accessing other pages of the program.
Can be accessed in kivy using root (not self!)
"""
class MainWindow(Screen):

    """
    Uses webbrowser library to open up to my GitHub
    Used for the 'GitHub button' in the main menu
    """
    def open_GitHub(self):
        webbrowser.open('https://github.com/anthonyjdearmas')

    """
    Returns all available jobs from data/jobs.txt
    """
    def get_Jobs(self):
        return WindowManager.jobs

    """
    Returns all available people that can be assigned to a job from data/people.txt
    """
    def get_People(self):
        return WindowManager.people

    """
    Assigns each person in the list a job and calls certain export functions depending on
    what settings the user has toggled.
    """
    def assign_Jobs(self):
        temp_jobs = WindowManager.jobs[:]
        if len(temp_jobs) < len(WindowManager.people):
            temp_jobs += ( len(WindowManager.people) -  len(temp_jobs) ) * ["No Job"]
        for person in WindowManager.people:
            selected_job = random.choice(temp_jobs)
            temp_jobs.remove(selected_job)
            WindowManager.job_assignments[person] = selected_job
        if WindowManager.textfile_export and not WindowManager.excelfile_export:
            self.exporttxtfile_Assignments(WindowManager.job_assignments)
            self.showpop_jobsassigned()
        if not WindowManager.textfile_export and WindowManager.excelfile_export:
            self.exportexcelfile_Assignments(WindowManager.job_assignments)
            self.showpop_jobsassigned()

    """
    Writes job assignments to an excel file located in data.assignments/assignments.xlsx
    """
    def exportexcelfile_Assignments(self, job_dict):
            assignments_exl = xlsxwriter.Workbook("data/assignments/assignments.xlsx")
            assignments_sheet = assignments_exl.add_worksheet()

            assignments_sheet.write("A1", "✓")
            assignments_sheet.write("B1", "Person")
            assignments_sheet.write("C1", "Job")
            row = 0
            for k, v in job_dict.items():
                row += 1
                assignments_sheet.write(row, 1, k)
                assignments_sheet.write(row, 2, v)
                assignments_sheet.set_column(0, 0, 5) 
                assignments_sheet.set_column(1, 1, 20) 
                assignments_sheet.set_column(2, 2, 35) 
            assignments_exl.close()            

    """
    Writes job assignments to an excel file located in data/assignments/assignments.txt
    """
    def exporttxtfile_Assignments(self, job_dict):
            job_assignments_text = open("data/assignments/assignments.txt", "w")
            for k, v in job_dict.items():
                job_assignments_text.write(k + " = " + v + '\n')
            job_assignments_text.close()

    """
    Creates the pop up menu to type in a job's name to ADD them to the list of jobs that people can be assigned to.
    """
    def showpop_jobsassigned(self):
        jobs_assigned = PopUpJobsAssigned()
        jobs_assignedpopupWindow = Popup(title="Success!", content=jobs_assigned, size_hint=(None, None), size=(200, 200))
        jobs_assignedpopupWindow.open()

"""
Pop up window object that is created to indicate that jobs were assigned successfully
"""
class PopUpJobsAssigned(FloatLayout):
    pass


"""
The configuration window of the program.
All if not almost all job proccesses are handled through this class.
"""
class SettingsWindow(Screen):
    # These need to be here for threading purposes!
    pretty_list_people = StringProperty("")
    pretty_list_jobs = StringProperty("")

    """
    Returns all available jobs from data/jobs.txt
    """
    def get_Jobs(self):
        return WindowManager.jobs
    
    """
    Returns all available people that can be assigned to a job from data/people.txt
    """
    def get_People(self):
        return WindowManager.people
    
    """
    Adds '\n' char to the list of people for displaying people in the configuration window
    """
    def Pretty_Print_People(self, ppl_list):
        self.pretty_list_people = ""
        for person in ppl_list:
            self.pretty_list_people += person + "\n"
    
    """
    Adds '\n' char to the list of jobs for displaying jobs in the configuration window
    """
    def Pretty_Print_Jobs(self, job_list):
        self.pretty_list_jobs = ""
        for job in job_list:
            self.pretty_list_jobs += job + "\n"

    """
    Creates the pop up menu to type in a person's name to ADD them to the list of people who can be assigned a job.
    """
    def showpop_addperson(self):
        addperson = Popupaddperson()
        addpersonpopupWindow = Popup(title="Add Person", content=addperson, size_hint=(None, None), size=(200, 200))
        addpersonpopupWindow.open()

    """
    Creates the pop up menu to type in a person's name to REMOVE them to the list of people who can be assigned a job.
    """
    def showpop_removebro(self):
        removebro = PopupRemovePerson()
        removebropopupWindow = Popup(title="Remove Person", content=removebro, size_hint=(None, None), size=(200, 200))
        removebropopupWindow.open()

    """
    Creates the pop up menu to type in a job's name to ADD them to the list of jobs that people can be assigned to.
    """
    def showpop_addjob(self):
        addjob = PopupAddJob()
        addjobpopupWindow = Popup(title="Add Job", content=addjob, size_hint=(None, None), size=(200, 200))
        addjobpopupWindow.open()

    """
    Creates the pop up menu to type in a job's name to REMOVE them to the list of jobs that people can be assigned to.
    """
    def showpop_removejob(self):
        removejob = PopupRemoveJob()
        removejobpopupWindow = Popup(title="Remove Job", content=removejob, size_hint=(None, None), size=(200, 200))
        removejobpopupWindow.open()

    """
    Enables text file import and disables excel file export
    """
    def enableexport_text(self):
        WindowManager.textfile_export = True
        WindowManager.excelfile_export = False

    """
    Enables excel file import and disables text file export
    """
    def enableexport_excel(self):
        WindowManager.textfile_export = False
        WindowManager.excelfile_export = True

"""
The menu that pops up to add a new person.
It will append the new person to the end of the list of people.

After adding a person, it will create a pop up window that indicates a person was
successfully added to the list of people.
"""
class Popupaddperson(FloatLayout):
    # This needs to be here for threading purposes!
    person_name = ObjectProperty(None)

    """
    Returns all available people that can be assigned to a job from data/people.txt
    """
    def get_People(self):
        return WindowManager.people

    """
    Appends a person to the list of people
    """
    def append_Newperson(self):
        if self.person_name.text != "" and self.person_name.text not in self.get_People():
            people_txtlist = open("data/people.txt", "a+")
            people_txtlist.seek(0)
            data = people_txtlist.read(100)
            if len(data) > 0 :
                people_txtlist.write("\n")
            people_txtlist.write(self.person_name.text)
            people_txtlist.close()
            self.get_People().append(self.person_name.text)
            
            self.notify_Personadded()
            self.person_name.text = ""
    """
    Creates a pop up window to indicate that a new person was successfully added
    """
    def notify_Personadded(self):
        personaddsuccess = PopupPersonAdded()
        personaddsuccessWindow = Popup(title="Success", content=personaddsuccess, size_hint=(None, None), size=(200, 200))
        personaddsuccessWindow.open()

"""
Pop up window object that is created to indicate that a new person was successfully added
"""
class PopupPersonAdded(FloatLayout):
    pass

"""
The menu that pops up to remove a person.

After removing a person, it will create a pop up window that indicates a person was
successfully removed from the list of people.
"""
class PopupRemovePerson(FloatLayout):
    person_name = ObjectProperty(None)

    """
    Returns all available people that can be assigned to a job from data/people.txt
    """
    def get_People(self):
        return WindowManager.people
    
    """
    Re-adds all people to the list except the one who is being removed
    """
    def remove_Person(self):
        if self.person_name.text in self.get_People():
            open('data/people.txt', 'w').close()
            people_txtlist = open("data/people.txt", "a")
            pos = 0
            for person in self.get_People():
                if person != self.person_name.text:
                    pos += 1
                    if ( pos == (len(self.get_People()) - 1) ):
                        people_txtlist.write(person)
                    else:
                        people_txtlist.write(person + "\n")
            people_txtlist.close()
            self.get_People().remove(self.person_name.text)
            self.notify_Personremoved()
            self.person_name.text = ""

    """
    Creates a pop up window to indicate that a new person was successfully removed
    """
    def notify_Personremoved(self):
        personremovesuccess = PopUpPersonRemoved()
        personremovesuccessWindow = Popup(title="Success", content=personremovesuccess, size_hint=(None, None), size=(200, 200))
        personremovesuccessWindow.open()

"""
Pop up window object that is created to indicate that a new person was successfully removed
"""
class PopUpPersonRemoved(FloatLayout):
    pass

"""
The menu that pops up to add a job.

After adding a job, it will create a pop up window that indicates a job was
successfully added to the list of jobs.
"""
class PopupAddJob(FloatLayout):
    jobname = ObjectProperty(None)

    """
    Returns all available jobs from data/jobs.txt
    """
    def get_Jobs(self):
        return WindowManager.jobs

    """
    Appends a job to the list of jobs
    """
    def append_Newjob(self):
        if self.jobname.text != "" and self.jobname.text not in self.get_Jobs():
            jobs_list = open("data/jobs.txt", "a+")
            jobs_list.seek(0)
            data = jobs_list.read(100)
            if len(data) > 0 :
                jobs_list.write("\n")
            jobs_list.write(self.jobname.text)
            jobs_list.close()
            self.get_Jobs().append(self.jobname.text)
            
            self.notify_Jobadded()
            self.jobname.text = ""

    """
    Creates a pop up window to indicate that a new job was successfully added
    """
    def notify_Jobadded(self):
        jobaddsuccess = PopupJobAdded()
        jobaddsuccessWindow = Popup(title="Success", content=jobaddsuccess, size_hint=(None, None), size=(200, 200))
        jobaddsuccessWindow.open()

"""
Pop up window object that is created to indicate that a new job was successfully added
"""
class PopupJobAdded(FloatLayout):
    pass

"""
The menu that pops up to remove a job.

After removing a job, it will create a pop up window that indicates a job was
successfully removed from the list of jobs.
"""
class PopupRemoveJob(FloatLayout):
    jobname = ObjectProperty(None)

    """
    Returns all available jobs from data/jobs.txt
    """
    def get_Jobs(self):
        return WindowManager.jobs

    """
    Re-adds all jobs to the list except the one who is being removed
    """
    def remove_Job(self):
        if self.jobname.text in self.get_Jobs():
            jobs_list = open("data/people.txt", "a")
            pos = 0
            for job in self.get_Jobs():
                if job != self.jobname.text:
                    if ( pos == (len(self.get_Jobs()) - 1) ):
                        pos += 1
                        jobs_list.write(job)
                    else:
                        jobs_list.write(job + "\n")
            jobs_list.close()
            self.get_Jobs().remove(self.jobname.text)
            self.notify_Jobremoved()
            self.jobname.text = ""

    """
    Creates a pop up window to indicate that a new job was successfully removed
    """
    def notify_Jobremoved(self):
        jobremovesuccess = PopUpJobRemoved()
        jobremovesuccessWindow = Popup(title="Success", content=jobremovesuccess, size_hint=(None, None), size=(200, 200))
        jobremovesuccessWindow.open()

"""
Pop up window object that is created to indicate that a new job was successfully removed
"""
class PopUpJobRemoved(FloatLayout):
    pass


"""
The main window of the program
Initializes jobs and people as blank lists and job_assignments to be a blank dictionary.
Note: Text file export option is on by default.
"""
class WindowManager(ScreenManager):
    jobs = []
    people = []
    job_assignments = {}
    textfile_export = True
    excelfile_export = False

    people_txtlist = open("data/people.txt", "r")
    people = [line.strip() for line in people_txtlist]
    people_txtlist.close()

    assignable_jobs = open("data/jobs.txt", "r")
    jobs = [line.strip() for line in assignable_jobs]
    assignable_jobs.close()

kv = Builder.load_file("Assigner.kv")

class Assigner(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        Window.borderless = True
        return kv

if __name__ == "__main__":
    Assigner().run()