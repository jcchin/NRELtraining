Recording Data from your Runs
=============================================================

Running an optimization in OpenMDAO is great, but it's not really useful unless you can record the
results.  In OpenMDAO, data recording is done through a special type of object called a
`CaseRecorder.` OpenMDAO comes  with a number of different kinds of CaseRecorders built into the
standard library, but you could also design your own if you have special needs. 

From ``openmdao.lib.casehandlers.api`` you have a variety of options, such as:

* **JSONCaseRecorder:** Dumps all case data to a JSON file
* **BSONCaseRecorder:** Saves all case data to a BSON file
* **CSVCaseRecorder:** Saves all case data to a CSV file

Drivers and CaseRecorders
-------------------------------------------------------------

CaseRecorder objects are used by drivers to record the information from your runs. In OpenMDAO, a
case  is the relevant data from any single run of a driver through its workflow. So in our actuator
disk example,  a case represents one iteration of the optimizer. 


An assembly can have multiple case recorders associated with it at the same time.


Setting Up Case Recording
-------------------------------------------------------------
We'll use the Betz limit optimization in order to demonstrate case recording.
Let's output all of the case data in JSON and CSV format.

To do this, import the `Betz_limit` assembly, as well as OpenMDAO's JSON and CSV
case recorders:

::

    from betz_limit import Betz_Limit
    from openmdao.lib.casehandlers.api import JSONCaseRecorder, CSVCaseRecorder


Now, create an instance of the `Betz_limit` assembly

::

    assembly = Betz_Limit()


Next, create instances of the JSON and CSV case recorders. As an argument,
both take the filename of where you would like the outputted data to be recorded:

:: 

    JSON_recorder = JSONCaseRecorder('bentz_limit.json')
    CSV_recorder = CSVCaseRecorder('bentz_limit.csv')


Set both recorders to the assembly by placing them both within the assembly's 
recorder list:

::

    assembly.recorders = [JSON_recorder, CSV_recorder]


Finally run the optimization just as before:

:: 

    assembly.run()


This will populate the two files set above with the case data from the 
optimization.


Reading Data From The Case Recorder Output
-------------------------------------------------
In the example above, case data was written to JSON and CSV files. These
are plain-text file formats which can be read-in and post processed in a wide variety
of ways. But OpenMDAO also has built-in capabilities for reading in 
these file types and making the recorded data available for queries and post-processing.
This is accomplished through use of the `CaseDataset` object.

First, import the CaseDataset object from OpenMDAO:

::

    from openmdao.lib.casehandlers.api import CaseDataset

Next, create a CaseDataset object with the filename to be imported, as well as
the case data ouput type ('json', 'csv', etc.):

::

    cds = CaseDataset("bentz_limit.json", 'json')


we can now perform queries directly on the data. For example, to list the name
of all variables in the data:

::

    cds.data.var_names().fetch()

To query for the values of specific variables across cases:

::

    variables = ["aDisc.a", "aDisc.Cp"]

    our_data = cds.data.vars(variables).fetch()

We can print, plot, and analyze this data directly:

::

    import matplotlib.pyplot as plt

    for area, cp in our_data:
        plt.plot(area, cp, "ko")
        plt.xlabel("a")
        plt.ylabel("Cp")
        
    plt.show()











    