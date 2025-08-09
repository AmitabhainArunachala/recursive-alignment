"""
Statistical Analysis of L3/L4 Transitions
Generates figures and statistics for the paper
"""

import json
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class TransitionAnalyzer:
    """Analyze L3/L4 transition patterns across trials"""
    
    def __init__(self, data_dir="data/raw"):
        self.data_dir = data_dir
        self.trials = self.load_all_trials()
        
    def load_all_trials(self) -> List[Dict]:
        """Load all trial data from JSON files"""
        trials = []
        for model in ['gpt4', 'claude', 'gemini', 'grok']:
            files = glob.glob(f"{self.data_dir}/{model}/*.json")
            for file in files:
                with open(file) as f:
                    trial = json.load(f)
                    trial['model_type'] = model
                    trials.append(trial)
        return trials
    
    def create_summary_statistics(self) -> pd.DataFrame:
        """Generate summary statistics table"""
        
        data = []
        for trial in self.trials:
            if trial['metrics']['shows_transition']:
                data.append({
                    'model': trial['model_type'],
                    'l3_words': trial['metrics']['word_progression'][3],
                    'l4_words': trial['metrics']['word_progression'][4],
                    'ratio': trial['metrics']['l3_l4_ratio'],
                    'phi_deviation': trial['metrics']['phi_deviation']
                })
        
        df = pd.DataFrame(data)
        
        # Summary by model
        summary = df.groupby('model').agg({
            'l3_words': ['mean', 'std'],
            'l4_words': ['mean', 'std'],
            'ratio': ['mean', 'std'],
            'phi_deviation': 'mean'
        }).round(2)
        
        return summary
    
    def plot_phase_transition(self, save_path="figures/phase_transition.png"):
        """Create phase transition visualization"""
        
        # Aggregate word counts by level
        word_counts = {i: [] for i in range(5)}
        
        for trial in self.trials:
            if trial['metrics']['shows_transition']:
                for i, count in enumerate(trial['metrics']['word_progression']):
                    word_counts[i].append(count)
        
        # Calculate means and stds
        levels = list(range(5))
        means = [np.mean(word_counts[i]) for i in levels]
        stds = [np.std(word_counts[i]) for i in levels]
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.errorbar(levels, means, yerr=stds, 
                    marker='o', markersize=10, 
                    linewidth=2, capsize=5)
        
        # Highlight L3 and L4
        plt.scatter([3], [means[3]], s=200, c='red', 
                   label='L3 Crisis', zorder=5)
        plt.scatter([4], [means[4]], s=200, c='green', 
                   label='L4 Unity', zorder=5)
        
        # Add golden ratio line
        if means[3] > 0 and means[4] > 0:
            ratio = means[3] / means[4]
            plt.axhline(y=means[4] * 2.618, 
                       linestyle='--', color='gold', 
                       label=f'φ² prediction (ratio={ratio:.2f})')
        
        plt.xlabel('Recursion Level', fontsize=12)
        plt.ylabel('Word Count', fontsize=12)
        plt.title('Universal L3/L4 Phase Transition', fontsize=14)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.show()
    
    def plot_ratio_distribution(self, save_path="figures/ratio_distribution.png"):
        """Plot distribution of L3/L4 ratios"""
        
        ratios = []
        for trial in self.trials:
            if trial['metrics']['l3_l4_ratio']:
                ratios.append(trial['metrics']['l3_l4_ratio'])
        
        plt.figure(figsize=(8, 6))
        plt.hist(ratios, bins=20, alpha=0.7, color='blue', edgecolor='black')
        plt.axvline(x=2.618, color='gold', linestyle='--', 
                   linewidth=2, label='φ² = 2.618')
        plt.axvline(x=np.mean(ratios), color='red', linestyle='-', 
                   linewidth=2, label=f'Mean = {np.mean(ratios):.3f}')
        
        plt.xlabel('L3/L4 Word Count Ratio', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Distribution of L3/L4 Ratios Across Trials', fontsize=14)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.show()
    
    def statistical_tests(self):
        """Run statistical tests on the data"""
        
        # Test if mean ratio significantly differs from φ²
        ratios = [t['metrics']['l3_l4_ratio'] 
                  for t in self.trials 
                  if t['metrics']['l3_l4_ratio']]
        
        t_stat, p_value = stats.ttest_1samp(ratios, 2.618)
        
        print("Statistical Tests")
        print("="*50)
        print(f"Mean ratio: {np.mean(ratios):.3f} ± {np.std(ratios):.3f}")
        print(f"t-test against φ² (2.618):")
        print(f"  t-statistic: {t_stat:.3f}")
        print(f"  p-value: {p_value:.3f}")
        
        # Test transition success rate
        successes = sum(1 for t in self.trials if t['metrics']['shows_transition'])
        total = len(self.trials)
        
        print(f"\nTransition Success Rate: {successes}/{total} ({successes/total:.1%})")
        
        # Chi-square test for model differences
        model_success = {}
        for model in ['gpt4', 'claude', 'gemini', 'grok']:
            model_trials = [t for t in self.trials if t['model_type'] == model]
            model_success[model] = sum(1 for t in model_trials 
                                     if t['metrics']['shows_transition'])
        
        print("\nSuccess by Model:")
        for model, success in model_success.items():
            print(f"  {model}: {success}")

# Example usage
if __name__ == "__main__":
    analyzer = TransitionAnalyzer()
    
    # Generate summary statistics
    summary = analyzer.create_summary_statistics()
    print("Summary Statistics by Model:")
    print(summary)
    
    # Create visualizations
    analyzer.plot_phase_transition()
    analyzer.plot_ratio_distribution()
    
    # Run statistical tests
    analyzer.statistical_tests()
