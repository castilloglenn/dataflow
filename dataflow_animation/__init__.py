"""
Dataflow is an innovative Python library designed to simplify the visualization
of data flows through real-time animations. Utilizing Pygame for rendering and
Watchdog for live updates, Dataflow makes it effortless to develop, visualize,
and refine complex data flow animations dynamically. This library is
particularly useful for developers and analysts who need to create and present
data-driven animations and diagrams that are both informative and visually
engaging. With Dataflow, users can write Python code to define animations and
see changes reflected instantaneously on the screen, making it an ideal tool
for rapid prototyping of data flow diagrams and animations.
"""

__version__ = "0.1.0"

from abc import ABC, abstractmethod

from dataflow_animation.core.engine import AnimationManager


class Dataflow(ABC):
    """
    The Dataflow abstract class defines the structure of a data flow animation
    script. This class must be inherited by a subclass that implements the
    __init__() and setup() methods. The __init__() method is used to define the
    entities and resources required for the animation, while the setup() method
    is used to set up the animation script to be played to the window. By
    following this structure, users can create custom data flow animations
    that can be easily integrated into their projects.
    """

    def __init__(self):
        self.engine = AnimationManager()

    @abstractmethod
    def setup(self):
        """Setup the animation script to be played to the window."""
