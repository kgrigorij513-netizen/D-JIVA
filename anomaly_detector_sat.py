import numpy as np
import matplotlib.pyplot as plt

def generate_satellite_signal(t, normal=True):
    noise_level = 0.1 if normal else 0.6
    return np.sin(2 * np.pi * 0.5 * t) + noise_level * np.random.normal(0, 1, size=t.shape)

def estimate_coherence(signal):
    autocorr = np.correlate(signal, signal, mode='full')
    norm = autocorr[len(autocorr)//2]
    if norm == 0: return 0.0
    R = autocorr[len(autocorr)//2 + 1] / norm
    return np.clip(R, 0, 1)

def run_detector():
    t = np.linspace(0, 10, 500)
    signals = [generate_satellite_signal(np.array([time]), normal=(time < 5))[0] for time in t]
    
    window = 50
    Rs = [estimate_coherence(np.array(signals[i-window:i])) for i in range(window, len(signals))]
    
    plt.figure(figsize=(10, 4))
    plt.plot(t[window:], Rs, label='Когерентность R')
    plt.axhline(0.85, color='red', linestyle='--', label='Порог R = 0.85')
    plt.title('Детектор аномалий D-JIVA')
    plt.legend()
    plt.savefig('anomaly_detection_plot.png')
    print("График сохранён как anomaly_detection_plot.png")

if __name__ == "__main__":
    run_detector()
