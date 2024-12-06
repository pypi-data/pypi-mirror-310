import time
from collections import deque
from typing import List, Literal

from typing_extensions import TypedDict


class Model(TypedDict):
    name: str
    priority: Literal['high', 'medium', 'low']
    limit: int


class ModelRotator:
    """
    A rotator to manage rate-limited LLMs with priority-based scheduling.

    Example:
        models = [
            {"name": "model1", "priority": "high", "limit": 30},
            {"name": "model2", "priority": "medium", "limit": 20},
        ]
        rotator = ModelRotator(models)
        next_model = rotator.get_next_model()
    """

    def __init__(self, models: List[Model]):
        """
        Initializes the rotator with models and their configurations.

        Args:
            models (list[Model]): List of models with their configuration.
        """
        self.models = models
        for model in self.models:
            if not all(key in model for key in ('name', 'priority', 'limit')):
                raise ValueError("Each model must have 'name', 'priority', and 'limit' keys.")
            if model['priority'] not in {'high', 'medium', 'low'}:
                raise ValueError(f"Invalid priority: {model['priority']}. Must be 'high', 'medium', or 'low'.")
            model['timestamps'] = deque()
        self.priority_map = {'high': 1, 'medium': 2, 'low': 3}

    def _prune_old_timestamps(self, model):
        """Remove timestamps older than 60 seconds."""
        now = time.time()
        while model['timestamps'] and now - model['timestamps'][0] > 60:
            model['timestamps'].popleft()

    def get_next_model(self) -> str | None:
        """
        Schedules the next available model based on priority and rate limits.

        Returns:
            str: The name of the selected model for the next call, or None if all are exhausted.
        """
        # Sort models by priority and availability
        self.models.sort(key=lambda x: (self.priority_map[x['priority']], len(x['timestamps'])))
        
        now = time.time()
        for model in self.models:
            self._prune_old_timestamps(model)
            
            if len(model['timestamps']) < model['limit']:
                model['timestamps'].append(now)
                return model['name']
        
        return None

    def get_state(self) -> List[dict]:
        """Returns the current state of all models."""
        return [
            {
                'name': model['name'],
                'priority': model['priority'],
                'limit': model['limit'],
                'current_usage': len(model['timestamps'])
            }
            for model in self.models
        ]
