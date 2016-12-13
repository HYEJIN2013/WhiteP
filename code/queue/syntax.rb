all_queues = ["test", "schedule", "process"]

QUEUES = "*"
# ["test", "schedule", "process"]

QUEUES = "test,schedule"
# ["test", "schedule"]

QUEUES = "*~test"
# ["schedule", "process"]

QUEUES = "*~test;process"
# ["schedule"]
