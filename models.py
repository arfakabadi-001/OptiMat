class Material:
    """
    Represents a material and calculates its score
    using weighted normalized model with penalties.
    """

    def __init__(self, material_id, name, strength, density, cost,
                 max_temp, corrosion, sustainability):

        self.material_id = material_id
        self.name = name
        self.strength = strength
        self.density = density
        self.cost = cost
        self.max_temp = max_temp
        self.corrosion = corrosion
        self.sustainability = sustainability

    def calculate_score(self, min_strength, max_density, max_cost,
                        required_temp, weights):

        # Extract weights safely
        ws = weights['ws']
        wc = weights['wc']
        wd = weights['wd']
        wcor = weights['wcor']
        wsus = weights['wsus']

        # --- Normalization ---
        norm_strength = self.strength / (min_strength if min_strength != 0 else 1)
        norm_density = 1 - (self.density / max_density)
        norm_cost = 1 - (self.cost / max_cost)
        norm_temp = self.max_temp / required_temp
        norm_corrosion = self.corrosion / 10
        norm_sustainability = self.sustainability / 10

        base_score = (
            norm_strength * ws +
            norm_cost * wc +
            norm_density * wd +
            norm_corrosion * wcor +
            norm_sustainability * wsus
        )

        # --- Penalty system ---
        penalty = 0

        if self.strength < min_strength:
            penalty += ((min_strength - self.strength) / min_strength) * 0.5

        if self.density > max_density:
            penalty += ((self.density - max_density) / max_density) * 0.5

        if self.cost > max_cost:
            penalty += ((self.cost - max_cost) / max_cost) * 0.5

        if self.max_temp < required_temp:
            penalty += ((required_temp - self.max_temp) / required_temp) * 0.5

        final_score = base_score * (1 - penalty)

        return max(final_score, 0)
