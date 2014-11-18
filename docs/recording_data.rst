Recording Data from your Runs
=============================================================

Running an optimization in OpenMDAO is great, but it's not really useful unless you can record the
results.  In OpenMDAO, data recording is done through a special type of object called a
`CaseRecorder.` OpenMDAO comes  with a number of different kinds of CaseRecorders built into the
standard library, but you could also design your own if you have special needs. 

From ``openmdao.lib.casehandlers.api`` you can get:

* **DumpCaseRecorder:** Dumps all case data to stdout
* **CSVCaseRecorder:** Saves all case data to csv file
* **DBCaseRecorder:** Saves all case data to a SQLite database
* **ListCaseRecorder:** Saves all case data in memory to a Python list

Drivers and CaseRecorders
-------------------------------------------------------------

CaseRecorder objects are used by drivers to record the information from your runs. In OpenMDAO, a
case  is the relevant data from any single run of a driver through its workflow. So in our actuator
disk example,  a case represents one iteration of the optimizer. 

Drivers have a slot, called `recorders`, which can accept any number of CaseRecorder objects. For
every iteration, each recorder in the slot will get handed the case to save in its own
way. This gives you the freedom to  save your case data in multiple ways simultaneously. 

Trying it out
-------------------------------------------------------------

If you open up the Betz Limit project from the :ref:`previous tutorial <uncon-opt>`, double-click
on ``driver``,  and then select the ``Slots`` tab, you can see the empty ``recorders`` slot. To add a
recorder, first filter the Library by `record` and drag the ``DumpCaseRecorder`` into the empty
slot. Just accept all the default settings that pop up in  the dialog. 

.. figure:: dump_recorder_slot.png
   :align: center

When you drop that in, notice that a new empty space  opens up to the right of your
``DumpCaseRecorder``. This is where you could put another recorder if you wanted to. Let's drop  a
``CSVCaseRecorder`` in there. Just accept all the default settings in the dialog that pops up here as
well. Now right-click on the assembly and select ``run`` from the menu. 

The first thing you'll notice is a bunch of text streaming through the console window at the bottom
of the screen that looks  something like this: 

:: 

    Case: 1
       uuid: 424ee13d-627c-11e2-bdac-a82066196c38
       inputs:
          ad.a: 0.5
       outputs:
          Objective: -0.5


That is the output from the dump case recorder. If you want to see the csv file you recorded, just
take a look at the Files  tab. You will see two files have shown up there. One is called
``cases.csv`` and the other will have a name like ``cases_-01-19_16-10-17.csv``.  These two
files will be identical. What happens is that the CSVCaseRecorder archives all its case
files with an additional date-time stamp in the name as it creates them. The most recent one will
be ``cases.csv`` (or whatever name you told it to use), and all the older ones will still be 
accessible from the date-time stamped files.
