from time import process_time, time
from apsim_client import ApsimClient, PropertyType

# client = ApsimClient()
# for i in range(0, 50):
#     # popns = range(2, 10)
#     popns = [2, 10]
#     for popn in popns:
#         changes = dict()
#         changes['[SowingRule].Script.Population'] = popn
#         outputNames = ['Sorghum.SowingData.Population', 'Yield', 'Biomass']
#         table = 'HarvestReport'
#         ip = "127.0.0.1"
#         port = 27746

#         outputs = client.run(changes, outputNames, table, ip, port)
#         print(outputs)

outputNames = ['Yield', 'SimulationName']
outputTypes = [PropertyType.DOUBLE, PropertyType.STRING]
tableName = 'HarvestReport'

runner = ApsimClient()

startTime = time()

numIter = 10

for i in range(0, numIter):
    iterStart = time()
    outputs = runner.run(dict(), outputNames, outputTypes, tableName, "127.0.0.1", 27746)
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