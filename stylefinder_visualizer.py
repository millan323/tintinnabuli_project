import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px

# Load dataset
df = pd.read_csv("stylefinder_features.csv")
df.dropna(inplace=True)

# Remove Cantus outlier
df = df[~df["filename"].str.contains("Cantus", case=False)]

# Select relevant features
features = [
    "total_notes",
    "pitch_range",
    "avg_interval",
    "note_density",
    "avg_duration",
]
X = df[features]

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df["PC1"] = X_pca[:, 0]
df["PC2"] = X_pca[:, 1]


# Group labeling function
def assign_group_and_label(row):
    name = row["filename"]
    if "Reise" in name:
        return "Millner - Reise"
    elif "Stufen" in name:
        return "Millner - Stufen"
    elif "Road" in name:
        return "Millner - Road"
    elif "Soteria" in name:
        return "Millner - Soteria"
    elif "Messiaen" in name:
        return "Messiaen"
    elif "Fratres" in name or "Spiegel" in name or "Alina" in name:
        return "Pärt"
    elif "Glass" in name or "Reich" in name:
        return "Minimalism"
    elif "Grecki" in name:
        return "Górecki"
    elif "Chad_Lawson" in name or "Lawson" in name:
        return "Chad Lawson"
    else:
        return "Other"


df["group"] = df.apply(assign_group_and_label, axis=1)

# Plot
fig = px.scatter(
    df,
    x="PC1",
    y="PC2",
    color="group",
    hover_data=["filename"],
    title="StyleFinder PCA: Millner Works vs Influences",
    labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2"},
    opacity=0.85,
)
fig.update_layout(legend_title_text="Group", height=700)
fig.show()
