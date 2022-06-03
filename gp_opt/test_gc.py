import makerun


makerun.make_all(1, None, None)
Job = makerun.GC_job(1, None, None)
Job.run()
