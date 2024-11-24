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
    reminders: List[str]
    text_content: str
    course_tag: str
    difficulty_rating: int
    initial_date: str
    deadline: Optional[str] = None
    dependencies: List[int] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.NOT_DONE

    def calculate_priority(self, current_date: date = None) -> float:
        """Calculate task priority based on difficulty and deadline proximity"""
        if current_date is None:
            current_date = date.today()
        
        # Base priority from difficulty (1-5 scale)
        priority = self.difficulty_rating * 2
        
        # Add deadline factor if deadline exists
        if self.deadline:
            deadline_date = datetime.strptime(self.deadline, '%Y-%m-%d').date()
            days_until_deadline = (deadline_date - current_date).days
            
            if days_until_deadline <= 0:
                # Past deadline tasks get very high priority
                priority += 10
                self.status = TaskStatus.LATE
            else:
                # Exponentially increase priority as deadline approaches
                deadline_factor = 10 / (1 + math.exp(days_until_deadline / 7))
                priority += deadline_factor
        
        self.priority = priority
        return priority

    def to_dict(self) -> dict:
        """Convert Task to dictionary for serialization"""
        data = asdict(self)
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create Task from dictionary representation"""
        # Convert status string to enum
        data['status'] = TaskStatus(data['status'])
        return cls(**data)

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
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def random_level(self) -> int:
        level = 1
        while random.random() < 0.5 and level < self.max_level:
            level += 1
        return level

    def update_task_priority(self, task: Task) -> None:
        """Update task priority without removing and reinserting"""
        x = self.header
        for i in range(self.level - 1, -1, -1):
            while x.forward[i] and x.forward[i].task.id < task.id:
                x = x.forward[i]
            if x.forward[i] and x.forward[i].task.id == task.id:
                x.forward[i].task = task
                return

    def insert(self, task: Task) -> None:
        """Insert a task into the skip list"""
        new_level = self.random_level()
        if new_level > self.level:
            self.level = new_level

        node = Node(task, new_level)
        update = [self.header] * self.max_level
        x = self.header

        # Find proper position for new node
        for i in range(self.level - 1, -1, -1):
            while x.forward[i] and x.forward[i].task.priority < task.priority:
                x = x.forward[i]
            update[i] = x

        # Insert node at all levels
        for i in range(new_level):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

        self._size += 1

class CourseManager:
    """Handles operations for a single course's task list"""
    def __init__(self, course_name: str, storage_dir: str):
        self.course_name = course_name
        self.storage_path = os.path.join(storage_dir, f"{course_name}.yaml")
        self.skip_list = SkipList()
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

    def update_priorities(self, current_date: date) -> None:
        """Update priorities of all tasks"""
        current = self.skip_list.header.forward[0]
        while current:
            current.task.calculate_priority(current_date)
            current = current.forward[0]

class TaskManager:
    """Main task management system"""
    def __init__(self, storage_dir: str = "courses"):
        self.storage_dir = storage_dir
        self.courses: Dict[str, CourseManager] = {}
        self.last_update_date = None
        
        # Ensure storage directory exists
        os.makedirs(storage_dir, exist_ok=True)
        
        self.load_metadata()
        self.load_courses()

    def load_metadata(self) -> None:
        """Load last update date from metadata file"""
        metadata_path = os.path.join(self.storage_dir, "metadata.yaml")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = yaml.safe_load(f)
                self.last_update_date = datetime.strptime(
                    metadata['last_update'], '%Y-%m-%d'
                ).date()
        else:
            self.last_update_date = date.today()
            self.save_metadata()

    def save_metadata(self) -> None:
        """Save last update date to metadata file"""
        metadata = {'last_update': self.last_update_date.strftime('%Y-%m-%d')}
        metadata_path = os.path.join(self.storage_dir, "metadata.yaml")
        with open(metadata_path, 'w') as f:
            yaml.dump(metadata, f)

    def load_courses(self) -> None:
        """Load all course managers"""
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".yaml") and filename != "metadata.yaml":
                course_name = filename[:-5]
                self.courses[course_name] = CourseManager(
                    course_name, self.storage_dir
                )

    def update_priorities(self) -> None:
        """Update priorities for all tasks if necessary"""
        today = date.today()
        if self.last_update_date != today:
            for course in self.courses.values():
                course.update_priorities(today)
            self.last_update_date = today
            self.save_metadata()
            self.save_all()

    def save_all(self) -> None:
        """Save all courses"""
        for course in self.courses.values():
            course.save()

    def move_task(self, task_id: int, from_course: str, to_course: str) -> bool:
        """Move a task between courses"""
        if from_course not in self.courses or to_course not in self.courses:
            return False

        # Find and remove task from source course
        source = self.courses[from_course].skip_list
        current = source.header.forward[0]
        task = None
        
        while current:
            if current.task.id == task_id:
                task = current.task
                source.delete(task)
                break
            current = current.forward[0]

        if task:
            # Update course tag and insert into destination course
            task.course_tag = to_course
            self.courses[to_course].skip_list.insert(task)
            self.save_all()
            return True
            
        return False