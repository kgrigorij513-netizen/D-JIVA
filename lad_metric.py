import numpy as np

def measure_lad(R, gamma, R_threshold=0.85, gamma_threshold=7):
    """
    Проверка бифуркационного порога D-JIVA.
    Возвращает True, если система в режиме устойчивой самоорганизации.
    """
    in_lad = (R >= R_threshold) and (gamma >= gamma_threshold)
    D = 1 - R**2
    return in_lad, D

if __name__ == "__main__":
    R, gamma = 0.87, 8
    in_lad, D = measure_lad(R, gamma)
    print(f"Режим 'Лад': {in_lad}")
    print(f"Декогеренция D = {D:.4f}")
