# cc-turtle-bot
# Copyright (C) 2015 Collin Eggert
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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