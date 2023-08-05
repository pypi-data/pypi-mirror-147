#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy <wxnacy@gmail.com>
# Description: 



from multitasker.models import task
from multitasker.models.base import Base, engine


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    tm = task.TaskModel(task_type = 'ss')
    print(tm.dict())
    tm.save()


