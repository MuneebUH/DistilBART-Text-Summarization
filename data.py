import pandas as pd
from datasets import load_dataset

# Load dataset, select 200 emails, and convert to DataFrame
ds = load_dataset("argilla/FinePersonas-Conversations-Email-Summaries")
df = pd.DataFrame(ds['train']).sample(n=200, random_state=42)[["email", "summary"]]  # Limit to 200 samples

# Save to CSV
df.to_csv("emails.csv", index=False)

print("Data saved to 'emails.csv'")
