import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to parse the log file using regular expressions
def parse_log_file(file_path):
    log_pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+-\s+(?P<user>\w+)\s+\[(?P<time>[^\]]+)\]\s+"(?P<request>[^"]+)"\s+(?P<status>\d+)\s+(?P<size>\d+)'
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(log_pattern, line)
            if match:
                logs.append(match.groupdict())
    return logs

# Function to convert parsed logs into a pandas DataFrame for easier analysis
def logs_to_dataframe(logs):
    df = pd.DataFrame(logs)
    df['status'] = df['status'].astype(int)
    df['size'] = df['size'].astype(int)
    return df

# Function to analyze the data and find 404 errors
def analyze_errors(df):
    errors_404 = df[df['status'] == 404]
    return errors_404

# Function to find the top IP addresses by number of requests
def top_ip_addresses(df, top_n=10):
    return df['ip'].value_counts().head(top_n)

# Combined visualization of 404 errors and top IP addresses with annotations
def visualize_combined(ip_counts, total_404):
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 404 errors
    sns.barplot(x=["Total 404 Errors"], y=[total_404], palette="Reds", ax=ax[0])
    ax[0].set_title('Total Number of 404 Errors')
    ax[0].set_ylabel('Count')

    # Plot top IP addresses by number of requests
    sns.barplot(x=ip_counts.values, y=ip_counts.index, palette="viridis", ax=ax[1])
    ax[1].set_title('Top IPs by Number of Requests')
    ax[1].set_xlabel('Number of Requests')
    ax[1].set_ylabel('IP Address')

    # Add custom text at the bottom of the plots, with proper spacing
    plt.figtext(0.5, 0.02, f"Total 404 errors: = {total_404}", ha="center", fontsize=12, color="red")
    plt.figtext(0.5, 0.06, f"Number of requests from {ip_counts.index[0]} = {ip_counts.iloc[0]}", ha="center", fontsize=12, color="blue")

    plt.tight_layout(pad=3.0)
    plt.show()

# Main execution block
if __name__ == "__main__":
    log_file_path = "./access.log.txt"   # Update this path to your log file
    logs = parse_log_file(log_file_path)
    df = logs_to_dataframe(logs)

    # Analyze and visualize
    errors_404 = analyze_errors(df)
    print(f"Total 404 errors: {len(errors_404)}")

    ip_counts = top_ip_addresses(df)
    visualize_combined(ip_counts, len(errors_404))
