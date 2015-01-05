from openmdao.lib.casehandlers.api import CaseDataset, caseset_query_to_html

import matplotlib.pyplot as plt

# Import case data set
cds = CaseDataset("bentz_limit.json", 'json')

# show all variable names
print cds.data.var_names().fetch()

# pick some that we want
variables = ["aDisc.a", "aDisc.Cp"]

# get all cases that have data for those variables
our_data = cds.data.vars(variables).fetch()


caseset_query_to_html(cds.data)

# make some plots
for area, cp in our_data:
    plt.plot(area, cp, "ko")
    plt.xlabel("a")
    plt.ylabel("Cp")
plt.show()