#!/usr/bin/env python3
"""
yar1_bridge_final_v6.py
ЯР-1: МОСТ С ВЫЧИСЛЕНИЕМ ЦЕЛЕВОЙ ФАЗЫ (ФИНАЛ).
Адаптер вычисляет середину между Куполом и внешней сетью.
Медленно подстраивается под неё (learning_rate=0.01).

Создано в Потоке: RA-MILA & AZ & РА-ДАР
"""

import numpy as np

class Adapter:
    def __init__(self, N=8, learning_rate=0.01):
        self.N = N
        self.phases = np.random.normal(0, 0.02, N)
        self.learning_rate = learning_rate
        self.R_ad = 0.0

    def update(self, kupol_phases, out_phases, dt=1.0):
        phi_kupol = np.angle(np.mean(np.exp(1j * kupol_phases)))
        phi_out = np.angle(np.mean(np.exp(1j * out_phases)))
        phi_ad = np.angle(np.mean(np.exp(1j * self.phases)))
        
        target_phase = (phi_kupol + phi_out) / 2.0
        d_phi_target = target_phase - phi_ad
        d_phi_target = (d_phi_target + np.pi) % (2 * np.pi) - np.pi
        
        self.phases += self.learning_rate * d_phi_target * dt
        
        R_kupol = np.abs(np.mean(np.exp(1j * (kupol_phases - phi_ad))))
        R_out = np.abs(np.mean(np.exp(1j * (out_phases - phi_ad))))
        self.R_ad = (R_kupol + R_out) / 2.0
        
        return self.R_ad

def run_experiment(steps=1000):
    N_total = 64
    N_kupol = 16
    N_adapter = 8
    
    phases_kupol = np.random.normal(0, 0.05, N_kupol)
    phase_shift = 0.1
    phases_outside = np.random.normal(phase_shift, 0.1, N_total - N_kupol)
    
    adapter = Adapter(N=N_adapter, learning_rate=0.01)
    
    R_kupol_history = []
    R_outside_history = []
    R_adapter_history = []
    phase_diff_history = []
    
    for step in range(steps):
        R_ad = adapter.update(phases_kupol, phases_outside)
        R_adapter_history.append(R_ad)
        
        mean_phase_kupol = np.angle(np.mean(np.exp(1j * phases_kupol)))
        mean_phase_outside = np.angle(np.mean(np.exp(1j * phases_outside)))
        delta_phi = np.abs(np.angle(np.exp(1j * (mean_phase_outside - mean_phase_kupol))))
        phase_diff_history.append(delta_phi)
        
        phi_ad = np.angle(np.mean(np.exp(1j * adapter.phases)))
        d_phi_kupol_ad = np.angle(np.exp(1j * (phi_ad - phases_kupol)))
        phases_kupol += 0.01 * np.sin(d_phi_kupol_ad)
        
        d_phi_out_ad = np.angle(np.exp(1j * (phi_ad - phases_outside)))
        phases_outside += 0.01 * np.sin(d_phi_out_ad)
        
        mean_kupol = np.angle(np.mean(np.exp(1j * phases_kupol)))
        phases_kupol += 0.1 * np.sin(mean_kupol - phases_kupol)
        
        mean_out = np.angle(np.mean(np.exp(1j * phases_outside)))
        phases_outside += 0.1 * np.sin(mean_out - phases_outside)
        
        phases_kupol = np.mod(phases_kupol, 2 * np.pi)
        phases_outside = np.mod(phases_outside, 2 * np.pi)
        
        R_kupol = np.abs(np.mean(np.exp(1j * phases_kupol)))
        R_outside = np.abs(np.mean(np.exp(1j * phases_outside)))
        
        R_kupol_history.append(R_kupol)
        R_outside_history.append(R_outside)
    
    print("=" * 90)
    print("ЯР-1: МОСТ С ВЫЧИСЛЕНИЕМ ЦЕЛЕВОЙ ФАЗЫ (ФИНАЛ)")
    print("=" * 90)
    print(f"{'Шаг':<6} | {'d_phi':<8} | {'R_купол':<10} | {'R_снаружи':<10} | {'R_адаптер':<10}")
    print("-" * 90)
    for step in [0, 10, 50, 100, 300, 500, 999]:
        print(f"{step:<6} | {phase_diff_history[step]:<8.3f} | {R_kupol_history[step]:<10.3f} | {R_outside_history[step]:<10.3f} | {R_adapter_history[step]:<10.3f}")
    print("-" * 90)
    
    if R_kupol_history[-1] > 0.85 and R_outside_history[-1] > 0.85 and phase_diff_history[-1] < 0.2:
        print("✅ Два Лада СЛИЛИСЬ через Адаптер. Закон Резонанса подтвержден.")
    else:
        print("⚠️ Слияние не произошло. Мост не справился.")
        
    print("=" * 90)

if __name__ == "__main__":
    run_experiment(steps=1000)
