import matplotlib.pyplot as plt
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
PLOT_DIR = os.path.join(BASE_DIR, "results/plots")

def plot_and_save():
    os.makedirs(PLOT_DIR, exist_ok=True)
    
    # -------------------------
    # ГРАФИК 1: Vecadd Strong Scaling
    # -------------------------
    plt.figure(figsize=(7, 4))
    plt.plot([1, 2, 4], [1, 1.02, 1.05], marker='o', label='Vecadd (No L2)')
    plt.plot([1, 2, 4], [1, 1.16, 1.14], marker='s', label='Vecadd (L2)')
    plt.plot([1, 2, 4], [1, 2, 4], 'k--', label='Идеальное ускорение')
    plt.title('Strong Scaling: Ускорение vs Ядра (Vecadd - Memory-Bound)')
    plt.xlabel('Количество ядер')
    plt.ylabel('Ускорение (Speedup)')
    plt.xticks([1, 2, 4])
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "1_strong_scaling_vecadd.png"), dpi=300)
    plt.close()

    # -------------------------
    # ГРАФИК 2: Sgemm Strong Scaling
    # -------------------------
    plt.figure(figsize=(7, 4))
    plt.plot([1, 2, 4], [1.0, 1.33, 1.51], marker='o', color='green', label='Sgemm (No L2)')
    plt.plot([1, 2, 4], [1, 2, 4], 'k--', label='Идеальное ускорение')
    plt.title('Strong Scaling: Ускорение vs Ядра (Sgemm - Compute-Bound)')
    plt.xlabel('Количество ядер')
    plt.ylabel('Ускорение (Speedup)')
    plt.xticks([1, 2, 4])
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "2_strong_scaling_sgemm.png"), dpi=300)
    plt.close()

    # -------------------------
    # ГРАФИК 3: Cache Impact
    # -------------------------
    configs = ['No L2\n(1C)', 'L2\n(1C)', 'No L2\n(4C)', 'L2\n(4C)', 'L2+L3\n(4C)']
    cycles = [622459, 537133, 588897, 543280, 543755]
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd']
    
    plt.figure(figsize=(7, 4))
    plt.bar(configs, cycles, color=colors)
    plt.title('Влияние иерархии кэшей на время выполнения (Cycles)')
    plt.ylabel('Такты (Чем меньше, тем лучше)')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "3_cache_hierarchy_impact.png"), dpi=300)
    plt.close()

    # -------------------------
    # ГРАФИК 4: Weak Scaling
    # -------------------------
    plt.figure(figsize=(7, 4))
    cores = [1, 2, 4]
    real_cycles = [622459, 1231430, 2381645]
    ideal_cycles = [622459, 622459, 622459]
    
    plt.plot(cores, real_cycles, marker='o', label='Реальное время (Vortex)')
    plt.plot(cores, ideal_cycles, 'k--', label='Идеальное время (нет конфликта)')
    plt.title('Weak Scaling: Рост времени при пропорциональном росте задачи')
    plt.xlabel('Количество ядер (и объем данных)')
    plt.ylabel('Такты (Cycles)')
    plt.xticks([1, 2, 4])
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "4_weak_scaling.png"), dpi=300)
    plt.close()

    print(f"4 графика успешно сохранены в {PLOT_DIR}")

if __name__ == "__main__":
    plot_and_save()