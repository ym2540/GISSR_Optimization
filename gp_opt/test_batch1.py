from makerun import GC_batch

jobs = [{"storm_id": 1, "topo_id": 2, "x":4.2, "phi": None}]
Batch = GC_batch(jobs)
Batch.create_all()
Batch.run()
