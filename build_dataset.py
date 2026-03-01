import pandas as pd

# -------- SETTINGS --------
NUM_LEGIT = 300
NUM_PHISH = 300

# -------- LOAD LEGITIMATE DATA --------

tranco = pd.read_csv("dataset/tranco_legit.csv")
tranco.columns = ["rank", "domain"]



# Take top N legit domains
legit = tranco.head(NUM_LEGIT).copy()
legit["url"] = "https://" + legit["domain"]
legit["label"] = 1

legit_final = legit[["url", "label"]]

# -------- LOAD PHISHING DATA --------
phish = pd.read_csv("dataset/phishtank_phishing.csv")

# Some phishtank files contain many columns; we only need 'url'
if "url" not in phish.columns:
    raise Exception("URL column not found in phishing dataset!")

phish = phish.head(NUM_PHISH).copy()
phish["label"] = -1

phish_final = phish[["url", "label"]]

# -------- MERGE --------
dataset = pd.concat([legit_final, phish_final])

# Remove duplicates
dataset.drop_duplicates(subset=["url"], inplace=True)

# Remove nulls
dataset.dropna(inplace=True)

# Shuffle dataset
dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

# -------- SAVE FINAL DATASET --------
dataset.to_csv("dataset/urls_dataset.csv", index=False)

print("Dataset built successfully!")
print("Total samples:", len(dataset))
print(dataset.head())