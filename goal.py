import abc

class Task:
  __metaclass__ = abc.ABCMeta
  UNRESOLVED = 1
  IN_PROGRESS = 2
  RESOLVED = 3
  
  def __init__(self):
    pass
  
  @abc.abstractmethod
  def getRequiredItems(self):
    return
  
  @abc.abstractmethod
  def getStatus(self):
    return
  
  def isOrdered(self):
    return
  
  def getName(self):
    return
  
class Goal(Task):
  __metaclass__ = abc.ABCMeta
  
  def __init__(self):
    pass
  
class Action(Task):
  __metaclass__ = abc.ABCMeta
  
  def __init__(self):
    pass
  
class TaskManager:
  def __init__(self):
    self.tasks = []
    pass
  
  def addTask(self, task):
    self.tasks.append(task)
  
  def getOpenActions(self):
    for task in self.tasks:
      r = self.__resolveTasks(task)
      if len(r) > 0:
        return r
    return []
    
  def __resolveTasks(self, task):
    if task.getStatus() == Task.UNRESOLVED:
      if type(task) == Action:
        return [task]
      else:
        t = []
        for subtask in task.getRequiredItems():
          r = self.__resolveTasks(subtask)
          t.extend(r)
          if len(t) > 0 and task.isOrdered():
            return t
        return t
    else:
      return []
    
class Tier1(Goal):
  def __init__(self):
    return