# Builtin modules
import timeit, zlib, pickle, marshal
from os.path import dirname
from statistics import median
# Third party modules
import fsPacker
# Local modules
# Program
def benchmark(dumpFn, loadsFn, data, name, counter=1000, repeat=4) -> None:
	print("  {}".format(name))
	q = dumpFn(data)
	print("    dump size: {:>9} byte".format(len(q)))
	res = timeit.repeat("fn(data)", number=counter, repeat=repeat, globals={"fn":dumpFn, "data":data})
	print("    dump : best: {:.8F} <- median: {:.8F} - average: {:.8F} -> worst: {:.8F}".format( min(res), median(res), sum(res)/repeat, max(res)))
	res = timeit.repeat("fn(data)", number=counter, repeat=repeat, globals={"fn":loadsFn, "data":q})
	print("    loads: best: {:.8F} <- median: {:.8F} - average: {:.8F} -> worst: {:.8F}".format( min(res), median(res), sum(res)/repeat, max(res)))
	return None

print("Test data one [1 times]")
testData1 = pickle.loads(zlib.decompress(open("{}/testData1.dat".format(dirname(__file__)), 'rb').read()))
benchmark(pickle.dumps, pickle.loads, testData1, "pickle", 1, 32)
benchmark(marshal.dumps, marshal.loads, testData1, "marshal", 1, 32)
benchmark(fsPacker.dumps, fsPacker.loads, testData1, "FSPacker", 1, 32)

print("Test data two [1 times]")
testData2 = pickle.loads(zlib.decompress(open("{}/testData2.dat".format(dirname(__file__)), 'rb').read()))
benchmark(pickle.dumps, pickle.loads, testData2, "pickle", 1, 32)
benchmark(marshal.dumps, marshal.loads, testData2, "marshal", 1, 32)
benchmark(fsPacker.dumps, fsPacker.loads, testData2, "FSPacker", 1, 32)

print("Test data three [1000 times]")
testData2 = { "jsonrpc":"2.0", "id":"00000000000", "method":"sampleMethod", "params":[True, "Joe", 88] }
benchmark(pickle.dumps, pickle.loads, testData2, "pickle", 1000, 32)
benchmark(marshal.dumps, marshal.loads, testData2, "marshal", 1000, 32)
benchmark(fsPacker.dumps, fsPacker.loads, testData2, "FSPacker", 1000, 32)
