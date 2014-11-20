=============================================================
Using the OpenMDAO derivatives system
=============================================================

Many optimization algorithms make use of gradients. By default, OpenMDAO
will finite difference it during the calculation of the full model gradient. However, an optimization process can often be sped up by having a component supply its own derivatives.

In OpenMDAO, derivatives can be specified in the component API by following
these two steps:

::

   #  Define a ``list_deriv_vars`` function that tell openmdao which inputs and outputs you have derivatives w.r.t and of
   #. Define a ``provideJ`` method that calculates and returns the Jacobian.

Let's return to the actuator disc component, and show how derivatives can be specified:

.. testcode:: simple_component_actuatordisk_review

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

The two function we need to add are ``list_deriv_vars`` and ``provideJ``.

The first function indicates which derivatives you're proving.
The order that you provide the variables in is important. 

The second function calculates and returns a matrix (the Jacobian)
of the derivatives, evaluated at the current state of the model. The order of the columns is the same as set for the ``inputs`` portion of ``list_deriv_vars``, and the order of the rows is the same as the order of ``outputs``.

 