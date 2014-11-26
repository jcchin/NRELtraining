

Building an Assembly- Unconstrained Optimization for the Betz Limit
=============================================================
We're going to set up an optimization to look for Betz's limit. This is a well-known result that
states that for a wind turbine, as you try  to extract more and more velocity from the incoming
wind, the best you can do is to extract about 60% of the power from the wind. This result comes from
an analysis of the equations used to build  our ActuatorDisk component. We'll try to use an
optimizer to confirm that our component returns the correct value for Betz's limit.

Components are connected to form a larger model using a construct in 
OpenMDAO called an ``Assembly``. Unlike components, assemblies can be nested in even
larger assemblies. Although nesting assemblies often makes sense from an
organizational persepctive, there are computational trade-offs to be considered.
These trade-offs are beyond the scope of this tutorial, but it's generally
advisable to keep models somewhat shallowly nested.

Assembly files are comprised of the same three parts as a component files.

- Importing Libraries
- Class Definition
- Stand-Alone Testing

While importing and testing work exactly the same as :ref:`components <BuildingAComponent>`,
the assembly class definition requires a configure method
(as opposed to an execute method in components).

Assembly Class Definition
-----------------------
An assembly class definition containes a minimum of three things:

- Class name declaration
- Input and output variable definition
- Configure method

**Class name declaration**

As an example::

    from openmdao.main.api import Assembly

    class Betz_Limit(Assembly):
        """Simple wind turbine assembly to calculate the Betz Limit"""

Our class is named ``Betz_Limit`` and it inherents from the Assembly
base class that we imported above.

**Input/Output Variable Definition**

Next, the inputs and outputs of the component class must be defined.

::

    class Betz_Limit(Assembly):
        """Simple wind turbine assembly to calculate the Betz Limit"""

        # Inputs
        a = Float(.5, iotype="in", desc="Induced Velocity Factor")

        # Outputs
        Vr = Float(iotype="out", desc="Air velocity at rotor exit plane", units="m/s")

So far so easy, this looks almost exactly like a component. However, the
configuration method introduces a few new OpenMDAO concepts.

Configuring Assemblies
-----------------------

OpenMDAO assemblies contain a *method* (function) called configure, it inherits
from it's own class ``self`` and contains general information about the
assemblies internal structure and solver behavior.
An assembly configuration usually includes:

::

    def configure(self):
        """things to be configured go here"""

- Adding component/assembly instances
- Specifying the driver
- Connecting components/assemblies to each other

Let's walk through the reasoning and syntax for each aspect.

**Adding component/assembly instances**

Although we've defined a component class we need to create an *instance* of the
object, just as we did in the :ref:`component testing script <ifNameEqualsMain>`.
If you're unfamiliar with object oriented programming, class definitions are
analogous to blueprints or templates for a design.
Instances represent actualized objects created from the blueprint or template.

As an example,
    ``jeff = teacher()``

    ``tristan = teacher()``

creates two instances, named ``jeff`` and ``tristan``, derived from the same
class: ``teacher``. We've already used this concept when creating float
instances in the previous component :ref:`tutorial <ComponentDefinition>`.

``a = Float(.5, iotype="in", desc="Induced Velocity Factor")``

creates an instance of the ``Float`` class called ``a``, with *arguments* within
the parentheses.

Likewise, this assembly class (or blueprint/template) definition contains
at least one of instance of a sub-assembly or sub-component.

::

    def configure(self):

        aDisk = self.add('actDisk', ActuatorDisk())

This line does a few things, it creates an instance of the ``ActuatorDisk()``
class called ``actDisk``, adds it to the 'Betz_Limit' assembly and creates a
local variable called ``aDisk``. It is perfectly fine (and often much more
convenient) to name the local variable the same as the instance name.


    ``aDisk = self.add('actDisk', ActuatorDisk())``  <--  works

    ``aDisk = self.add('aDisk', ActuatorDisk())`` <-- also works

    ``self.add('aDisk', ActuatorDisk())``  <--is the same as above,
    but no local variable is created

as discussed earlier, if a local variable isn't created, the variable is
referenced with the ``self.<variableName>`` prefix. Remember to import any
classes that you instantiate at the top of the assembly file. Adding
sub-assemblies follows the exact same syntax.

**Specifying the driver**

OpenMDAO provides a selection of `optimization algorithms 
<http://openmdao.org/docs/tutorials/optimization/optimizers.html>`_ to drive
assemblies towards a specified objective. These drop-in algorithms are know as 
*drivers*. Although a default driver is automatically configured, the user may
select a different driver, following the same syntax as adding components:

::

    self.driver.add('driver', SLSQPdriver())

Many optimizers also contain tunable settings which can be found by searching
the `docs <http://openmdao.org/docs/srcdocs/packages/openmdao.lib.html#drivers>`_.

Many models will also contain `implicit iterations
<http://openmdao.org/docs/tutorials/implicit/index.html>`_ which require
multiple calculation loops before settling on a converged state. Adding solvers
follows the same syntax as drivers, and OpenMDAO provides both a `Broyden and 
Newton Solver <http://openmdao.org/docs/srcdocs/packages/openmdao.lib.html#drivers>`_.

Both drivers and solvers must be given control of a variable that it can modify
to achieve the user specified goal.

::

    self.driver.add_parameter('self.aDisk.a', low=0, high=1)
    self.driver.add_objective('-self.aDisk.Cp')

In this example, the driver is allowed to vary the variable ``a`` between 0 and
1 until ``Cp`` is maximized. Optimizers by default will try to minimize the
objective, so the objective is set to ``-Cp`` to get a
maximization. Likewise for solvers, *contraints* can be specified that must be
satisfied.

``self.solver.add_constraint('self.aDisk.Cp = 0')``

Finally, both drivers and solvers can optionally have a specified *workflow*, which 
determines the order in which components are executed.

::

    self.driver.workflow.add('aDisk')

Our simple example doens't have a particularly exciting workflow since there is
only one component. More complex models can provide the workflow as a python
list of strings.

``self.driver.workflow.add(['comp1','comp2','comp3'])``

**Connecting components/assemblies to each other**

With the drivers/solvers configured, the final step is to wire up connections
between the various components within the workflow. It's important to remember
that OpenMDAO distinguished between the dataflow and the workflow. The dataflow
describes which components communicate with others, but it says nothing about
when that communication happens. The order of execution is determined by the
workflow. Although the dataflow does not define the workflow, it can constrain
it. For example, if you have two components, `a` and `b`,  where `a` has an
output connected to the input of `b`, then you must run `a` before `b`.  In
most cases, the automatically created workflow will work just fine.  Just know
that if you need to modify the workflow to add a sub-solver loop or introduce
some metamodel training, the flexibility is there. Our simple one component
example doesn't require passing any variables, but this would be achieved with
the following syntax

``self.connect('comp1.a', 'comp2.a')``

In this example, the value of output variable ``a`` from ``comp1`` would be
passed to ``comp2``'s input variable ``a``. It is not necessary for connected
variables to share the same name, and OpenMDAO will automatically check for
compatible units.

As noted previously, only component variables with a specified ``iotype`` from
the component class definition can be connected. Local variables are not
accessible. Component variables within a parent assembly can be promoted up as
I/O variable at the parent's bounadary using the following syntax:

``self.create_passthrough('self.aDisk.Cp')``  <-- This promoted variable can now be referenced as ``self.a`` in parent connections.

This simplifies variable connections that must be accessible at the top-level
of nested assemblies.

Run the Optimization
---------------------------

To summarize, ``betz_limit.py`` is displayed in its entirety below:

.. testcode:: simple_assembly_betzlimit

    from openmdao.main.api import Assembly
    from openmdao.lib.drivers.slsqpdriver import SLSQPdriver
    from nreltraining.nreltraining import ActuatorDisk #Import components from the plugin

    class Betz_Limit(Assembly):
        """Simple wind turbine assembly to calculate the Betz Limit"""

        # Inputs would go here

        # Outputs would go here
        # Cp = Float(iotype="out", desc="Power Coefficient")

        def configure(self):
        """things to be configured go here"""

        aDisk = self.add('aDisk', ActuatorDisk())

        driver = self.driver.add('driver', SLSQPdriver())
        driver.add_parameter('aDisk.a', low=0, high=1)
        driver.add_objective('-aDisk.Cp')
        driver.workflow.add('aDisk')

        # self.connect('self.Cp', 'self.aDisk.cp') #promote Cp to the assembly output
        self.create_passthrough('self.aDisk.Cp') #shortcut for commented code above

    if __name__ == "__main__":

        assembly = Betz_Limit()
        assembly.run

        print assembly.Cp

Running ``python betz_limit.py`` from an activated terminal will show that the
optimizer found a value of approximately 1/3 for axial induction factor,
yielding a power coefficient just under .6. Congratulations! You have
just found Betz's limit. You can close down the project for now.

