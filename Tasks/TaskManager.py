from dataclasses import dataclass, asdict, field
from datetime import datetime, date
import yaml
import os
from typing import Dict, List, Optional
import math
import random
from enum import Enum

class TaskStatus(Enum):
    DONE = "done"
    NOT_DONE = "not_done"
    LATE = "late"

@dataclass
class Task:
    id: int
    name: str
    priority: float
    # reminders: List[str]
    text_content: str
    course_tag: str
    initial_date: datetime

    deadline: Optional[datetime] = None
    status: TaskStatus = TaskStatus.NOT_DONE
    difficulty_rating: int = 1 # Default difficulty rating
    
    def calculate_priority(self, current_date: date = None) -> float:
        if current_date is None:
            current_date = date.today()
        
        priority = self.difficulty_rating * 2
        
        if self.deadline:
            days_until_deadline = (self.deadline.date() - current_date).days
            
            if days_until_deadline <= 0:
                priority += 10
                self.status = TaskStatus.LATE
            else:
                deadline_factor = 10 / (1 + math.exp(days_until_deadline / 7))
                priority += deadline_factor
        
        self.priority = priority
        return priority

    # Both functions facilitate serialization for YAML
    # Do Not Touch Unless You Know What You're Doing
    def to_dict(self) -> dict:
        """Convert Task to dictionary for serialization"""
        data = asdict(self)
        data['status'] = self.status.value
        data['initial_date'] = self.initial_date.strftime('%Y-%m-%d')
        data['deadline'] = self.deadline.strftime('%Y-%m-%d') if self.deadline else None
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create Task from dictionary representation"""
        data['status'] = TaskStatus(data.get('status', TaskStatus.NOT_DONE.value))
        data['initial_date'] = datetime.strptime(data['initial_date'], '%Y-%m-%d')
        data['deadline'] = datetime.strptime(data['deadline'], '%Y-%m-%d') if data.get('deadline') else None
        
        required_fields = ['id', 'name', 'text_content', 'course_tag', 'initial_date']
        for field_name in required_fields:
            if field_name not in data:
                raise ValueError(f"Missing required field: {field_name}")
            
        return cls(**data)

# Just a node in the skip list that has a task
class Node:
    def __init__(self, task: Task, height: int):
        self.task = task
        self.height = height
        self.forward = [None] * height
        self.backward = None


class SkipList:
    def __init__(self, max_level: int = 16):
        self.max_level = max_level
        self.header = Node(None, max_level)
        self.level = 1
        self._size = 0 # Number of tasks in a skip list / course

    def __len__(self) -> int:
        return self._size

    def random_level(self) -> int:
        level = 1
        while random.random() < 0.5 and level < self.max_level:
            level += 1
        return level

    # def update_task_priority(self, task: Task) -> None:
    #     """Update task priority without removing and reinserting"""
    #     x = self.header
    #     for i in range(self.level - 1, -1, -1):
    #         while x.forward[i] and x.forward[i].task.id < task.id:
    #             x = x.forward[i]
    #         if x.forward[i] and x.forward[i].task.id == task.id:
    #             x.forward[i].task = task
    #             return

    def insert(self, task: Task) -> None:
        """Insert a task into the skip list"""
        if self.search(task.id):
            raise ValueError(f"Task with ID {task.id} already exists.")
        new_level = self.random_level()
        if new_level > self.level:
            self.level = new_level

        node = Node(task, new_level)
        update = [self.header] * self.max_level
        x = self.header

        # Find proper position for new node
        for i in range(self.level - 1, -1, -1):
            while x.forward[i] and x.forward[i].task.id < task.id:
                x = x.forward[i]
            update[i] = x

        # Insert node at all levels
        for i in range(new_level):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

        self._size += 1
        
    # Some function here to remove a node
    def remove(self, task_id: int) -> None:  # Corrected argument name
        """Remove a task from the skip list."""
        update = [self.header] * self.max_level
        x = self.header

        for i in range(self.level - 1, -1, -1):
            while x.forward[i] and x.forward[i].task.id < task_id:
                x = x.forward[i]
            update[i] = x

        if x.forward[0] and x.forward[0].task.id == task_id:
            for i in range(self.level):  # Iterate through all levels
                if update[i].forward[i] and update[i].forward[i].task.id == task_id:
                    update[i].forward[i] = update[i].forward[i].forward[i]

            while self.level > 1 and self.header.forward[self.level - 1] is None:
                self.level -= 1

            self._size -= 1
        else:
            raise ValueError("Task not found in the skip list")
    
    # Some function here to search for the task
    def search(self, task_id: int) -> Optional[Task]:
        x = self.header
        for i in range(self.level - 1, -1, -1):
            while x.forward[i] and x.forward[i].task.id < task_id:
                x = x.forward[i]
        x = x.forward[0]
        if x and x.task.id == task_id:
            return x.task
        return None


class CourseManager:
    """Handles operations for a single course's task list"""
    def __init__(self, course_name: str, storage_dir: str):
        self.course_name = course_name
        self.storage_path = os.path.join(storage_dir, f"{course_name}.yaml")
        self.skip_list = SkipList()
        self.completed_tasks = 0
        self.load()

    def load(self) -> None:
        """Load tasks from YAML file"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                tasks_data = yaml.safe_load(f) or []
                for task_data in tasks_data:
                    task = Task.from_dict(task_data)
                    self.skip_list.insert(task)


    def save(self) -> None:
        """Save tasks to YAML file"""
        tasks = []
        current = self.skip_list.header.forward[0]
        while current:
            tasks.append(current.task.to_dict())
            current = current.forward[0]
        
        with open(self.storage_path, 'w') as f:
            yaml.dump(tasks, f)

    ###########################
    # TASK SPECIFIC FUNCTIONS #
    ###########################

    # Should only be one single insertion, as multiple task insertion is not a thing
    def update_priorities(self, current_date: date) -> None:
        """Update priorities of all tasks"""
        current = self.skip_list.header.forward[0]
        while current:
            current.task.calculate_priority(current_date)
            current = current.forward[0]
            
    # Some function here to update a task
    def update_task(self, updated_task: Task) -> None:  # Pass the whole Task object
        """Updates an existing task in the skip list."""
        old_task = self.skip_list.search(updated_task.id)
        if old_task:
            self.skip_list.remove(updated_task.id)
            # Check if priority-relevant fields have changed. If they do, recalculate priority
            if old_task.deadline != updated_task.deadline or old_task.difficulty_rating != updated_task.difficulty_rating: 
                updated_task.calculate_priority()
            self.skip_list.insert(updated_task)
            self.save()
        else:
            raise ValueError(f"Task with ID {updated_task.id} not found.")
    
    def insert_task(self, task: Task) -> None:
        self.skip_list.insert(task)
        self.save()
    
    # Some function here to remove a task
    def remove_task(self, task_id: int) -> None:  # Use task_id
        """Removes a task from the skip list."""
        try:
            self.skip_list.remove(task_id)
            self.save()
        except ValueError:
            raise ValueError(f"Task with ID {task_id} not found.")
    
    # Some function here to mark a task as complete
    def mark_task_complete(self, task_id: int) -> None:
        """Marks a task as complete."""
        task = self.skip_list.search(task_id)
        if task:
            if not task.status:  # Check if task is already complete
                task.status = TaskStatus.DONE
                self.completed_tasks += 1
                self.save()
        else:
            raise ValueError(f"Task with ID {task_id} not found.")
    
    # Some function here to mark a task as incomplete
    def mark_task_incomplete(self, task_id: int) -> None:
        """Marks a task as incomplete."""
        task = self.skip_list.search(task_id)
        if task:
            if task.status == TaskStatus.DONE:  # Check if task is already incomplete
                task.status = TaskStatus.NOT_DONE
                self.completed_tasks -= 1  # Decrement completed task counter.
                self.save()
        else:
            raise ValueError(f"Task with ID {task_id} not found.")
    
    # Some function here to return the total count of tasks in the course, just return the skip list size
    def task_amount(self) -> int:
        """Returns the total number of tasks in the course."""
        return len(self.skip_list)
    
    # Some function here to return the number of completed tasks
    def get_completed_task_count(self) -> int:
        """Returns the number of completed tasks."""
        return self.completed_tasks
    
    # Some function here to return the number of incomplete tasks, mostly likely just the difference between completed and total
    def get_incomplete_task_count(self) -> int:
        """Returns the number of incomplete tasks."""
        return self.task_amount() - self.completed_tasks

### Should initialize the moment the program starts ###
class TaskManager:
    """Main task management system"""
    def __init__(self, storage_dir: str = "courses"):
        self.storage_dir = storage_dir
        self.courses: Dict[str, CourseManager] = {}
        self.last_update_date = None
        self.lifetime_tasks = 0
        self.next_task_id = 1  # To generate unique task IDs
        self.load_next_task_id()
        
        # Ensure storage directory exists
        os.makedirs(storage_dir, exist_ok=True)
        
        self.load_metadata()
        self.load_courses()

    def load_next_task_id(self):
        """Load next task ID from metadata."""
        metadata_path = os.path.join(self.storage_dir, "metadata.yaml")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = yaml.safe_load(f)
                self.next_task_id = metadata.get('next_task_id', 1) # Default to 1 if not found
                
    def load_metadata(self) -> None:
        metadata_path = os.path.join(self.storage_dir, "metadata.yaml")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = yaml.safe_load(f) or {}
                last_update_str = metadata.get('last_update')
                if last_update_str:
                    self.last_update_date = datetime.strptime(last_update_str, '%Y-%m-%d').date()
                else:
                    self.last_update_date = date.today()
                self.next_task_id = metadata.get('next_task_id', 1)
                self.lifetime_tasks = metadata.get('lifetime_tasks', 0)
        else:
            self.last_update_date = date.today()
            self.next_task_id = 1
            self.lifetime_tasks = 0
            self.save_metadata()

    
    def save_metadata(self) -> None:
        """Save metadata including next task ID."""
        metadata = {
            'last_update': self.last_update_date.strftime('%Y-%m-%d'),
            'next_task_id': self.next_task_id,
            'lifetime_tasks': self.lifetime_tasks
        }
        metadata_path = os.path.join(self.storage_dir, "metadata.yaml")
        with open(metadata_path, 'w') as f:
            yaml.dump(metadata, f)

    def save_all(self) -> None:
        """Save all courses"""
        for course in self.courses.values():
            course.save()

    def add_course(self, course_name: str) -> None:
        """Adds a new course."""
        if course_name in self.courses:
            raise ValueError(f"Course '{course_name}' already exists.")
        if course_name == "":
            course_name = "general"
        self.courses[course_name] = CourseManager(course_name, self.storage_dir)
        self.save_all()  # Save the new course to disk

    def remove_course(self, course_name: str) -> None:
        """Removes a course and its associated tasks."""
        if course_name not in self.courses:
            raise ValueError(f"Course '{course_name}' not found.")

        del self.courses[course_name]  # Remove from memory
        filepath = os.path.join(self.storage_dir, f"{course_name}.yaml")
        if os.path.exists(filepath):
            os.remove(filepath)  # Remove from disk

    def get_courses(self) -> List[str]:
        """Returns a list of all course names."""
        return list(self.courses.keys())

    def load_courses(self) -> None:
        """Load all course managers"""
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".yaml") and filename != "metadata.yaml":
                course_name = filename[:-5]
                self.courses[course_name] = CourseManager(
                    course_name, self.storage_dir
                )
    
    def generate_task_id(self) -> int:
        """Generate a unique task ID."""
        task_id = self.next_task_id
        self.next_task_id += 1
        self.save_metadata()  # Save updated ID immediately
        return task_id
    
    def add_task(self, course_name: str, task_data: dict) -> Task:
        """Adds a task to a course."""
        if course_name == "":
            course_name = "general"
            task_data['course_tag'] = course_name
        else:
            task_data['course_tag'] = course_name  # Ensure correct course tag
            
        if course_name not in self.courses:
            self.courses[course_name] = CourseManager(course_name, self.storage_dir)

        task_data['id'] = self.generate_task_id()  # Assign a unique ID


        task = Task.from_dict(task_data)
        task.calculate_priority()
        self.courses[course_name].insert_task(task)
        self.lifetime_tasks += 1 #increment lifetime tasks by 1.
        return task

    def move_task(self, task_id: int, from_course: str, to_course: str) -> bool:
        if from_course not in self.courses or to_course not in self.courses:
            return False

        task = self.courses[from_course].skip_list.search(task_id)
        if task:
            self.courses[from_course].remove_task(task_id)
            task.course_tag = to_course or "general"
            self.courses[to_course].insert_task(task)
            self.save_all()
            return True
        return False


    def update_priorities(self) -> None:
        """Update priorities for all tasks if necessary"""
        today = date.today()
        if self.last_update_date != today:
            for course in self.courses.values():
                course.update_priorities(today)
            self.last_update_date = today
            self.save_metadata()
            self.save_all()
    
    # Some function here that to retrieve a list of tasks depending upon the deadline. 
    def get_tasks_by_deadline(self, course_name: str, days: int) -> List[Task]:
        """Retrieve tasks with deadlines within the specified number of days."""
        if course_name not in self.courses:
            return []

        today = date.today()
        deadline_tasks = []
        current = self.courses[course_name].skip_list.header.forward[0]
        while current:
            if current.task.deadline:
                # Use the deadline directly without parsing
                deadline = current.task.deadline.date()
                days_until_deadline = (deadline - today).days
                if 0 <= days_until_deadline <= days:  # Include tasks due today and within 'days'
                    deadline_tasks.append(current.task)
            current = current.forward[0]
        return deadline_tasks

    
    # Some Function here that retrieves tasks based on priority.
    def get_tasks_by_priority(self, course_name: str, top_n: int = None) -> List[Task]:
        """Retrieve tasks sorted by priority."""
        if course_name not in self.courses:
            return []

        tasks = []
        current = self.courses[course_name].skip_list.header.forward[0]
        while current:
            tasks.append(current.task)
            current = current.forward[0]
        tasks.sort(key=lambda task: task.priority, reverse=True)  # Sort in descending priority
        return tasks[:top_n] if top_n else tasks
    
