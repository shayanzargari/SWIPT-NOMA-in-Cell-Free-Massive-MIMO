from dataclasses import dataclass


@dataclass
class SimulationConfig:
    area_size: float = 1000.0
    num_aps: int = 32
    num_users_min: int = 2
    num_users_max: int = 20
    user_step: int = 2
    monte_carlo: int = 200

    bandwidth: float = 1e6
    noise_power_dbm: float = -94
    tx_power_dbm: float = 30

    path_loss_exp: float = 3.7
    shadow_std_db: float = 8.0

    swipt_efficiency: float = 0.8
    power_split: float = 0.3

    noma_alpha_far: float = 0.8
    noma_alpha_near: float = 0.2

    seed: int = 42
