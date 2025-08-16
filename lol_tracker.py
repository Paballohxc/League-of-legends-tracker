import pandas as pd
import matplotlib.pyplot as plt
import os

# ========== LOAD DATA ==========
def load_data(filepath):
    return pd.read_csv(filepath)

# ========== ANALYSIS FUNCTIONS ==========
def winrate_by_champ(df):
    results = df.groupby('champion')['result'].value_counts().unstack().fillna(0)
    results['winrate'] = results['Win'] / (results['Win'] + results['Lose'])
    return results

def losses_by_enemy(df):
    losses = df[df['result'] == 'Lose']
    return losses['enemy_champion'].value_counts()

def avg_damage(df):
    return df.groupby('champion')['damage_dealt'].mean()

def best_counter(df):
    counters = df[df['result'] == 'Win']
    return counters.groupby(['enemy_champion'])['champion'].agg(lambda x: x.value_counts().idxmax())

# ========== REPORT GENERATION ==========
def generate_report(df, out_dir="out"):
    os.makedirs(out_dir, exist_ok=True)
    report_path = os.path.join(out_dir, "report.md")

    
    # Winrate by champ
    winrates = winrate_by_champ(df)
    
    # Losses by enemy champ
    enemy_losses = losses_by_enemy(df)
    
    # Average damage
    damages = avg_damage(df)
    
    # Best counters
    counters = best_counter(df)
    
    # Write report
    with open(report_path, "w") as f:
        f.write("# League of Legends Performance Report\n\n")

        f.write("## Winrates by Champion\n")
        f.write(winrates.to_markdown())
        f.write("\n\n")

        f.write("## Losses by Enemy Champion\n")
        f.write(enemy_losses.to_markdown())
        f.write("\n\n")

        f.write("## Average Damage by Champion\n")
        f.write(damages.to_markdown())
        f.write("\n\n")

        f.write("## Best Counters\n")
        f.write(counters.to_markdown())
        f.write("\n\n")

    # Save graphs
    winrates['winrate'].plot(kind='bar', title='Winrate by Champion')
    plt.ylabel('Winrate')
    plt.savefig(os.path.join(out_dir, "winrate_by_champ.png"))
    plt.close()

    enemy_losses.plot(kind='bar', title='Losses by Enemy Champion')
    plt.ylabel('Losses')
    plt.savefig(os.path.join(out_dir, "losses_by_enemy.png"))
    plt.close()

    print(f"Report generated at {report_path}")

# ========== MAIN ==========
if __name__ == "__main__":
    filepath = "sample_matches.csv"  # default dataset
    df = load_data(filepath)
    generate_report(df)
