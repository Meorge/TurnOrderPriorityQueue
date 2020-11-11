from queue import PriorityQueue
import queue
from typing import List, Tuple, Any
from dataclasses import dataclass, field

@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)

    def __repr__(self) -> str:
        return f"{self.item}"

def make_copy_of_item(item):
    copy = PrioritizedItem(item.priority, make_copy_of_unit(item.item))
    return copy

def make_copy_of_unit(unit):
    copy = Unit(name=unit.name, speed=unit.speed)
    return copy

class Unit:
    speed: float
    name: str
    def __init__(self, name="Unit", speed=0.5):
        self.speed = speed
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name}"


class BattleQueue:
    def __init__(self):
        self.queue = PriorityQueue()

    def push(self, unit: Unit):
        self.queue.put(PrioritizedItem(unit.speed, unit))

    def pull(self, queue_to_use=None) -> PrioritizedItem:
        if queue_to_use == None:
            queue_to_use = self.queue

        # This is the top item from the priority queue.
        out_value: PrioritizedItem = queue_to_use.get()

        # We want to get the speed of the top item, and add it to every item.
        time_to_add = out_value.item.speed

        # We want to add it to the item we just pulled.
        out_value.priority += time_to_add
        queue_to_use.put(out_value)

        return out_value

    def get_expected_queue(self, number_of_steps = 10) -> List[PrioritizedItem]:
        out_value: List[PrioritizedItem] = []

        # create a copy of the queue
        queue_copy = PriorityQueue()
        for i in self.queue.queue:
            queue_copy.put(make_copy_of_item(i))

        # Basically do a bunch of pull()ing, but only on a COPY of the queue
        for i in range(number_of_steps):
            out_value.append(self.pull(queue_to_use=queue_copy))

        return out_value


def preview_queue():
    a = ""
    for i in q.get_expected_queue():
        a += str(i)
    print(f"Coming up: {a}")

def take_turn():
    preview_queue()
    print(f"Going now: {q.pull()}")

def set_speed(unit, amount):
    print(f"Setting {unit} speed to {amount}")
    unit.speed = amount

q = BattleQueue()

collin = Unit(name="A", speed=0.7)
enemy = Unit(name="B", speed=1.0)
enemy2 = Unit(name="C", speed=1.2)

q.push(collin)
q.push(enemy)
q.push(enemy2)


# Begin battle
take_turn()
take_turn()
take_turn()
# set_speed(collin, 0.4)
take_turn()
take_turn()
# set_speed(collin, 0.7)
take_turn()
take_turn()