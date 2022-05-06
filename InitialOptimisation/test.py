from time import process_time, time
from apsim_client import ApsimClient, PropertyType

client = ApsimClient()
# popns = range(2, 10)
popns = [2, 10]
for popn in popns:
    changes = dict()
    changes['[Sow on a fixed date].Script.Population'] = popn
    outputNames = ['Yield', 'Biomass']
    outputTypes = [PropertyType.DOUBLE, PropertyType.DOUBLE]
    table = 'HarvestReport'
    ip = "127.0.0.1"
    port = 27746

    outputs = client.run(changes, outputNames, outputTypes,  table, ip, port)
    print(outputs)

"""

outputNames = ['Yield', 'SimulationName']
outputTypes = [PropertyType.DOUBLE, PropertyType.STRING]
tableName = 'HarvestReport'

runner = ApsimClient()

startTime = time()

numIter = 10

for i in range(0, numIter):
    iterStart = time()
    changes = dict()
    changes['[SowingRule].Script.Population'] = 3
    outputs = runner.run(changes, outputNames, outputTypes, tableName, "127.0.0.1", 27746)
    iterEnd = time()
    print('Iter %d duration: %.2fs' % (i, iterEnd - iterStart))
    print(outputs)

endTime = time()
duration = endTime - startTime

print('Ran %d iterations in %.2fs.' % (numIter, duration))

# self.assertEqual(len(outputNames), len(outputs.columns))
# simulationNameColumn = outputs[outputNames[0]]
# self.assertEqual(1, len(simulationNameColumn))
# self.assertAlmostEqual('Simulation', simulationNameColumn[0])
"""

