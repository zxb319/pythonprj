from typing import List, Tuple


class Asset:
    def __init__(self, price, next_period_distribution: List[Tuple[float, 'Asset']]):
        self.price = price
        self.next_period_distribution = next_period_distribution
