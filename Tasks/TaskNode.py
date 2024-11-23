
import random
from enum import Enum

class TaskStatus(Enum):
    DONE = "done"
    NOT_DONE = "not_done"
    LATE = "late"

class Task:
    def __init__(self, id, name, priority, reminders, text_content, course_tag, difficulty_rating, initial_date, deadline=None, dependencies=None, tags=None, notes=None):
        self.id = id
        self.name = name
        self.status = TaskStatus.NOT_DONE
        self.priority = priority
        self.reminders = reminders
        self.text_content = text_content
        self.course_tag = course_tag
        self.difficulty_rating = difficulty_rating
        self.initial_date = initial_date
        self.deadline = deadline
        self.dependencies = dependencies if dependencies else []
        self.tags = tags if tags else []
        self.notes = notes if notes else []

class Node:
    def __init__(self, task, height):
        self.task = task
        self.height = height
        self.forward = [None] * height
        self.backward = None

class SkipList:
    def __init__(self, max_level=16):
        self.max_level = max_level
        self.header = Node(None, max_level)
        self.level = 1

    def random_level(self):
        level = 1
        while random.random() < 0.5 and level < self.max_level:
            level += 1
        return level

    def insert(self, task):
        new_level = self.random_level()
        if new_level > self.level:
            for i in range(self.level, new_level):
                self.header.forward[i] = None
            self.level = new_level
        node = Node(task, new_level)
        update = [None] * self.max_level
        x = self.header
        for i in range(self.level - 1, -1, -1):
            while x.forward[i] and x.forward[i].task.priority < task.priority:
                x = x.forward[i]
            update[i] = x
        for i in range(new_level):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
        if node.forward[0]:
            node.forward[0].backward = node

    def delete(self, task):
        update = [None] * self.max_level
        x = self.header
        for i in range(self.level - 1, -1, -1):
            while x.forward[i] and x.forward[i].task.priority < task.priority:
                x = x.forward[i]
            update[i] = x
        x = x.forward[0]
        if x and x.task == task:
            for i in range(self.level - 1, -1, -1):
                if update[i].forward[i]!= x:
                    break
                update[i].forward[i] = x.forward[i]
            while self.level > 1 and self.header.forward[self.level - 1] is None:
                self.level -= 1

    def print_tasks(self):
        x = self.header.forward[0]
        while x:
            print(f"Priority: {x.task.priority}, Task: {x.task.name}")
            x = x.forward[0]

# Example usage:
sl = SkipList()
task1 = Task(1, "Task 1", 5, [], "Task 1 content", "Course 1", 3, "2022-01-01", deadline="2022-01-15")
task2 = Task(2, "Task 2", 3, [], "Task 2 content", "Course 1", 2, "2022-01-05")
task3 = Task(3, "Task 3", 8, [], "Task 3 content", "Course 2", 4, "2022-01-10", deadline="2022-01-20")

sl.insert(task1)
sl.insert(task2)
sl.insert(task3)

sl.print_tasks()

sl.delete(task2)

sl.print_tasks()