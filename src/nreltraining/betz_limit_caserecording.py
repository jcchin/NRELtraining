from betz_limit import Betz_Limit
from openmdao.lib.casehandlers.api import JSONCaseRecorder, CSVCaseRecorder


assembly = Betz_Limit()

JSON_recorder = JSONCaseRecorder('betz_limit.json')
CSV_recorder = CSVCaseRecorder('betz_limit.csv')

assembly.recorders = [JSON_recorder, CSV_recorder]

assembly.run()

    