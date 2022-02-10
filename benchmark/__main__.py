# Builtin modules
import timeit, zlib, pickle, marshal
from os.path import dirname
from copy import deepcopy
from statistics import median
from functools import partial
from typing import Any
# Third party modules
import fsPacker
from fsPacker.fallback import dumps as pyDumps, loads as pyLoads
# Local modules
# Program
def benchmark(dumpFn:Any, loadsFn:Any, data:Any, name:str, counter:int=1000, repeat:int=4) -> None:
	print("  {}".format(name))
	packedData = dumpFn(data)
	print("    packed data size: {:>9} byte".format(len(packedData)))
	res = timeit.repeat("fn(data)", number=counter, repeat=repeat, globals={"fn":dumpFn, "data":data})
	print("    dump : best: {:.8F} <- median avg: {:.8F} - average: {:.8F} -> worst: {:.8F}".format(
		min(res),
		median(res),
		sum(res)/repeat,
		max(res),
	))
	res = timeit.repeat("fn(data)", number=counter, repeat=repeat, globals={"fn":loadsFn, "data":packedData})
	print("    loads: best: {:.8F} <- median avg: {:.8F} - average: {:.8F} -> worst: {:.8F}".format(
		min(res),
		median(res),
		sum(res)/repeat,
		max(res),
	))

def startBatch(i:int, data:Any, counter:int) -> None:
	print("Batch {}# started".format(i))
	benchmark(pickle.dumps, pickle.loads, data, "pickle", counter, 32)
	benchmark(marshal.dumps, marshal.loads, data, "marshal", counter, 32)
	for version in range(1, fsPacker.HIGHEST_VERSION + 1):
		benchmark(
			partial(fsPacker.dumps, version=version),
			fsPacker.loads,
			data,
			"FSPacker version {}".format(version),
			counter,
			32,
		)
		if fsPacker.ACCELERATION_IS_AVAILABLE:
			benchmark(
				partial(pyDumps, version=version),
				pyLoads,
				data,
				"FSPacker PURE PYTHON version {}".format(version),
				counter,
				32,
			)
	print("")
	
data = deepcopy(pickle.loads(zlib.decompress(open("{}/testData1.dat".format(dirname(__file__)), 'rb').read())))
startBatch(1, data, 1)
data = deepcopy(pickle.loads(zlib.decompress(open("{}/testData2.dat".format(dirname(__file__)), 'rb').read())))
startBatch(2, data, 1)
data = deepcopy([data, {"data":(data, data)}])
startBatch(3, data, 1)
data = { "jsonrpc":"2.0", "id":"00000000000", "method":"sampleMethod", "params":[True, "Joe", 88] }
startBatch(4, data, 1000)
