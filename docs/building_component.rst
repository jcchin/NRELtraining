.. _`BuildingAComponent`:

=============================================================
Building a Component - Actuator Disk
=============================================================

In this tutorial, we're going to define a component that uses
actuator disk theory to provide a very simple model of a wind turbine. 
We will reproduce an engineering design limitation known as the Betz limit.

.. figure:: actuator_disk.png
   :align: center

   Actuator disk

A component takes a set of inputs and operates on them to produce a set of
outputs. In the OpenMDAO framework, a class called *Component*
provides this behavior. Component definition files are usually comprised of
three parts that are explained in depth below.

- Importing Libraries
- Class Definition
- Stand-Alone Testing

Importing Libraries
=========================================

In Python, a class or function must be imported before it can be used. So
firstly, we will import some helpful libraries from OpenMDAO.

Following standard python, specific classes can be imported with the following syntax:
``from <library> import <Class>``

Optionally, imports can be assinged a nickname or alias: 
``from <library> import <Class> as <alias>``

::

    from openmdao.main.api import Component
    from openmdao.lib.datatypes.api import Float


**Avoid** importing entire libraries,
this slows down your code and can cause namespace collisions.

:: 

    import openmdao.main.api #This is bad.
    from openmdao.lib.datatypes.api import * #Don't do this.

Most of what you need in OpenMDAO can be imported from
``openmdao.main.api`` and the ``openmdao.lib`` api modules.
For this example we will import the base OpenMDAO ``Component`` class,
and ``Float`` variable type. This provides us with basic boilerplate
functionality useful for constructing engineering models.

.. _`ComponentDefinition`:

Component Class Definition
=========================================
A class definition containes a minimum of three things:

- Class name declaration
- Input and output variable definition
- Execute method

There are more advanced features that can be added to components,
but this is a good starting point.

**Class name declaration**

Just as you would define a class in standard python, you follow the syntax

``class <Name>(<ParentClass>):``
        ``"""<Description>"""``

As an example::

    class ActuatorDisk(Component):
        """Simple wind turbine model based on actuator disk theory"""

Our class is named ``ActuatorDisk`` and it inherents from the Component
base class that we imported above. The second line containing triple quotes
provides a brief description of the class. 

**Input/Output Variable Definition**

Next, the inputs and outputs of the component class must be defined.

::

    class ActuatorDisk(Component):
        """Simple wind turbine model based on actuator disk theory"""

        # inputs
        a = Float(.5, iotype="in", desc="Induced Velocity Factor")
        Area = Float(10, iotype="in", desc="Rotor disk area", units="m**2", low=0)
        rho = Float(1.225, iotype="in", desc="air density", units="kg/m**3")
        Vu = Float(10, iotype="in", desc="Freestream air velocity, upstream of rotor", units="m/s")

        # outputs
        Vr = Float(iotype="out", desc="Air velocity at rotor exit plane", units="m/s")
        Vd = Float(iotype="out", desc="Slipstream air velocity, downstream of rotor", units="m/s")
        Ct = Float(iotype="out", desc="Thrust Coefficient")
        thrust = Float(iotype="out", desc="Thrust produced by the rotor", units="N")
        Cp = Float(iotype="out", desc="Power Coefficient")
        power = Float(iotype="out", desc="Power produced by the rotor", units="W")

The I/O variables shown in this snippet are comprised of OpenMDAO ``Float`` datatypes.
A full complement of other variable types available in OpenMDAO
can be found `here <http://openmdao.org/docs/basics/variables.html>`_.
It's beneficial to use the OpenMDAO datatypes so the framework can properly
type check the variables, ensure valid connections, automatically handle unit conversions,
and assist in documentation.

These datatypes take one required argument (iotype) a few optional arguments:
Default value, description and units.

Any input variables that are expected to be passed into this component are 
given the argument ``iotype='in'`` and conversely,
outputs are labeled with ``iotype='out'``.
If the iotype is omitted (or misspelled), then the variable
won't be visible to the framework.
Specifying the physical units (if applicable) allows openMDAO to validate
and automatically convert between compatible units when connecting variables across other components.
A list of valid unit types can be found `here <http://openmdao.org/docs/units.html>`_.

**Execute Method**

Next, the ``execute`` method contains the main calculations and engineering
operations of the component.

:: 

    def execute(self):
            # we use 'a' and 'Vu' a lot, so make method local variables

            a = self.a
            Vu = self.Vu
            qA = .5*self.rho*self.Area*Vu**2

            self.Vd = Vu*(1-2 * a)
            self.Vr = .5*(self.Vu + self.Vd)

            self.Ct = 4*a*(1-a)
            self.thrust = self.Ct*qA

            self.Cp = self.Ct*(1-a)
            self.power = self.Cp*qA*Vu

As standard Python convention, this internal method inherits from ``self``
(Actuator Disk), and all I/O variables are referenced with the prefix ``self.<variableName>``.
Local variables can be defined for convenience, as done with ``a``, ``Vu``, and ``qA``. 
These variables can only be called locally from within the method and 
any references to local variables outside of this method will throw errors.
Only I/O variables from the class definition will be accessible elsewhere. 

In this particular execution method, we treat the entire rotor as a single disk
that extracts velocity uniformly from the incoming flow and converts it to
power. If you define the upstream, rotor, and downstream velocities as
:math:`V_u`, :math:`V_r`, :math:`V_d` respectively, then you can describe the
axial induction factor, :math:`a`, as the amount of velocity extracted from the
flow. :math:`a = \frac{V_u-V_r}{V_r}`

.. _`ifNameEqualsMain`:

Stand-Alone Testing
=========================================

The final (optional) section of a component generally includes a script that
allows you to run your component by itself.
This is often helpful for debugging as you build up your model.

::

    if __name__ == "__main__":

        comp = ActuatorDisk()
        comp.run

        print comp.power
        print comp.thrust

In this snippet, the ``if __name__ == "__main__":`` is a common Python pattern
that in plain english means "if this file is called directly, run the following commands"
This section is ignored if the component class is instantiated elsewhere.

In this particular run script, an *instance* of the ActuatorDisk class is
created called ``comp``. This component instance is run, and two outputs are
printed to the console.


To summarize, ``actuator_disk.py`` is displayed in its entirety below:

.. testcode:: simple_component_actuatordisk

    from openmdao.main.api import Component
    from openmdao.lib.datatypes.api import Float


    class ActuatorDisk(Component):
        """Simple wind turbine model based on actuator disk theory"""

        # inputs
        a = Float(.5, iotype="in", desc="Induced Velocity Factor")
        Area = Float(10, iotype="in", desc="Rotor disk area", units="m**2", low=0)
        rho = Float(1.225, iotype="in", desc="air density", units="kg/m**3")
        Vu = Float(10, iotype="in", desc="Freestream air velocity, upstream of rotor", units="m/s")

        # outputs
        Vr = Float(iotype="out", desc="Air velocity at rotor exit plane", units="m/s")
        Vd = Float(iotype="out", desc="Slipstream air velocity, downstream of rotor", units="m/s")
        Ct = Float(iotype="out", desc="Thrust Coefficient")
        thrust = Float(iotype="out", desc="Thrust produced by the rotor", units="N")
        Cp = Float(iotype="out", desc="Power Coefficient")
        power = Float(iotype="out", desc="Power produced by the rotor", units="W")

        def execute(self):
            # we use 'a' and 'Vu' a lot, so make method local variables

            a = self.a
            Vu = self.Vu
            qA = .5*self.rho*self.Area*Vu**2

            self.Vd = Vu*(1-2 * a)
            self.Vr = .5*(self.Vu + self.Vd)

            self.Ct = 4*a*(1-a)
            self.thrust = self.Ct*qA

            self.Cp = self.Ct*(1-a)
            self.power = self.Cp*qA*Vu

    if __name__ == "__main__":

        comp = ActuatorDisk()
        comp.run

        print comp.power
        print comp.thrust



Running your Component
=========================================
To run the component and ensure your getting the expected output,
open an activated terminal window and navigate the parent folder of
this file. Simply run:

::

    python actuator_disk.py


Thats it! You've built and ran your first OpenMDAO component.

With legacy code written in other language, such as Fortran or C/C++,
components can also contain wrappers.
The `Plugin-Developer-Guide <http://openmdao.org/docs/plugin-guide/index.html>`_ 
gives some examples of how to incorporate these kinds of components into OpenMDAO.
