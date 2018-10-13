import numpy as np

def any_close_to(base_item, target_list, atol=1e-8, rtol=0):
    """Iterates through a list of points and checks if any are close to the base point."""
    # https://eklitzke.org/generator-comprehensions-and-using-any-and-all-in-python
    return any(np.linalg.norm(base_item - target_item) < atol for target_item in target_list)

def both_close_to(base_item1, base_item2, target_list, atol=1e-8, rtol=0):
    """Checks if two points are both close to any in a target list of points."""
    return any(np.linalg.norm(base_item1 - target_item) < atol for target_item in target_list) and any(np.linalg.norm(base_item2 - target_item) < atol for target_item in target_list)
