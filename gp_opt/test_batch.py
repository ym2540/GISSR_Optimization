import batch

Job = batch.StormTopoJob(0, 0)
Job.type = "./batch_jobs"
Controller = batch.HabaneroBatchController(jobs=[Job])
Controller.plot = False
Controller.wait = True
paths = Controller.run()
print(paths)