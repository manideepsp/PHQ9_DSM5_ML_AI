# %%
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# %%
from sqlalchemy.orm import aliased
import sys
sys.path.append('..')
from models import PHQ9Assessment, DSM5Assessment, User


results = (
    Session()
    .query(
        User.username,
        User.age,
        User.gender,
        User.industry,
        User.profession,
        PHQ9Assessment.responses,
        PHQ9Assessment.total_score,
        PHQ9Assessment.doctors_notes,
        PHQ9Assessment.patients_notes,
        DSM5Assessment.severity,
        DSM5Assessment.q9_flag,
        DSM5Assessment.mdd_assessment,
        DSM5Assessment.created_at
    )
    .outerjoin(PHQ9Assessment, User.user_id == PHQ9Assessment.user_id)
    .outerjoin(DSM5Assessment, User.user_id == DSM5Assessment.user_id)
    .all()
)

for row in results[:1]:
    print(row)


# %%
import pandas as pd

columns = [
    'username', 'age', 'gender', 'industry', 'profession',
    'phq9_responses', 'phq9_total_score', 'phq9_doctors_notes', 'phq9_patients_notes',
    'dsm5_severity', 'dsm5_q9_flag', 'dsm5_mdd_assessment', 'dsm5_created_at'
]

df = pd.DataFrame(results, columns=columns)
df.head(1)

# %%
phq9_df = df["phq9_responses"].apply(pd.Series)
phq9_df = phq9_df.add_prefix("phq9_q")
df_expanded = pd.concat([df, phq9_df], axis = 1)
df_expanded.head(1)


# %%
df["dsm5_mdd_assessment"].head(5)


# %%
import pandas as pd

# inspect unique raw values (shows hidden chars)
print([repr(x) for x in df_expanded['dsm5_mdd_assessment'].unique()])
print(df_expanded['dsm5_mdd_assessment'].value_counts(dropna=False))


# %%
df_expanded['age'] = df_expanded['age'].astype(int)
df_expanded['phq9_total_score'] = df_expanded['phq9_total_score'].astype(int)
df_expanded["dsm5_mdd_assessment"] = (
    df_expanded["dsm5_mdd_assessment"]
    .astype(str)
    .str.strip()            # remove whitespace
    .str.strip("'")         # remove single quotes
    .str.lower()
    .map({'true': True, 'false': False})
    .astype('bool')
)

df_expanded['dsm5_created_at'] = pd.to_datetime(df_expanded['dsm5_created_at'], utc=True)
df_expanded[['age', 'phq9_total_score', 'dsm5_created_at','dsm5_mdd_assessment']].dtypes

# %%
import pprint

pprint.pprint(df_expanded.iloc[1].to_dict())

# %%
# Select columns by name instead of integer index
selected_columns = [
	'username', 'age', 'gender', 'industry', 'profession',
	'phq9_total_score', 'phq9_doctors_notes', 'phq9_patients_notes',
	'dsm5_severity', 'dsm5_q9_flag', 'dsm5_mdd_assessment', 'dsm5_created_at',
	'phq9_q0', 'phq9_q1', 'phq9_q2', 'phq9_q3', 'phq9_q4', 'phq9_q5', 'phq9_q6', 'phq9_q7', 'phq9_q8'
]
df_expanded = df_expanded[selected_columns]

# %% [markdown]
# ## Feature Extraction, convert feilds to numericals
# 
# ### Label Encoding
# 

# %%
from sklearn.preprocessing import LabelEncoder

# Encode categorical columns
label_encoders = {}

# Columns to encode
categorical_cols = ['industry', 'profession', 'dsm5_severity']

for col in categorical_cols:
    le = LabelEncoder()
    df_expanded[col + '_enc'] = le.fit_transform(df_expanded[col].astype(str))
    label_encoders[col] = le
    # Save label mapping to CSV
    label_df = pd.DataFrame({
        col: le.classes_,
        col + '_enc': range(len(le.classes_))
    })
    label_df.to_csv(f'Labels\\label_mapping_{col}.csv', index=False)

# For boolean columns, convert to int (already bool, so just astype)
df_expanded['dsm5_q9_flag_enc'] = df_expanded['dsm5_q9_flag'].astype(int)
df_expanded['dsm5_mdd_assessment_enc'] = df_expanded['dsm5_mdd_assessment'].astype(int)

df_expanded[[col + '_enc' for col in categorical_cols] + ['dsm5_q9_flag_enc', 'dsm5_mdd_assessment_enc']].head()

# %% [markdown]
# # Need Simulated dates for timeseries
# 

# %%
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Generate random dates within the last year, with UTC timezone
date_range = pd.date_range(end=pd.Timestamp.today(tz='UTC'), periods=365)
df_expanded['sim_date'] = np.random.choice(date_range, size=len(df_expanded), replace=True)

# %% [markdown]
# ## Exploratory Analysis
# 

# %%
print(df_expanded.shape)
print(df_expanded.dtypes)
print(df_expanded.isnull().sum())
print(df_expanded.describe(include='all'))


# %% [markdown]
# ### Age distribution
# 

# %%
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 3))


plt.hist(df_expanded['age'], bins=20, edgecolor="black")
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()


# %% [markdown]
# ### Gender distribution
# 

# %%
plt.figure(figsize=(5, 3))
df_expanded['gender'].value_counts().plot(kind="bar", edgecolor="black")
plt.title("Gender Distribution")
plt.show()


# %% [markdown]
# ### Industry and profession
# 

# %%
df_expanded['industry'].value_counts().head(10).plot(kind="barh", edgecolor="black")
plt.title("Top 10 Industries")
plt.show()

plt.figure(figsize=(10, 15))
df_expanded['profession'].value_counts().head(50).plot(kind="barh", color="green", edgecolor="black")
plt.title("Top 10 Professions")
plt.show()


# %% [markdown]
# ### PHQ-9 Scores Analysis
# 
# #### Total Score Distribution
# 

# %%
plt.hist(df_expanded['phq9_total_score'], bins=15, edgecolor="black")
plt.title("PHQ-9 Total Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.show()

# %% [markdown]
# #### Question wise distribution
# 

# %%
phq_cols = [f"phq9_q{i}" for i in range(9)]
df_expanded[phq_cols].mean().plot(kind="bar")
plt.title("Average Response per PHQ-9 Question")
plt.ylabel("Mean Score (0-3)")
plt.show()


# %% [markdown]
# ### DSM 5
# 
# #### Severity
# 

# %%
df_expanded['dsm5_severity'].value_counts().plot(kind="bar", color="red")
plt.title("DSM-5 Severity Levels")
plt.show()


# %% [markdown]
# #### MDD Flag
# 

# %%
df_expanded['dsm5_mdd_assessment'].value_counts().plot(kind="pie", autopct="%1.1f%%", colors=["lightblue", "salmon"])
plt.title("MDD Assessment Result")
plt.show()


# %% [markdown]
# ### Cross Analysis
# 
# #### PHQ-9 vs DSM-5 Severity
# 

# %%
import seaborn as sns

plt.figure(figsize=(12, 5))
order = [
    "No depression",
    "Mild depression",
    "Moderate depression",
    "Moderately severe depression",
    "Severe depression"
]
labels = [
    "no depression",
    "mild",
    "moderate",
    "moderately severe",
    "severe"
]
ax = sns.boxplot(
    x="dsm5_severity",
    y="phq9_total_score",
    data=df_expanded,
    order=order
)
ax.set_xticklabels(labels)
plt.title("PHQ-9 Score Distribution by DSM-5 Severity")
plt.xlabel("DSM-5 Severity")
plt.ylabel("PHQ-9 Total Score")
plt.show()


# %% [markdown]
# #### MDD With age
# 

# %%
sns.histplot(data=df_expanded, x="age", hue="dsm5_mdd_assessment", multiple="stack")
plt.title("Age Distribution by MDD Assessment")
plt.show()


# %% [markdown]
# ### Correlations
# 

# %%
import seaborn as sns

corr = df_expanded[phq_cols + ["phq9_total_score"]].corr()
plt.figure(figsize=(10,7))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between PHQ-9 Questions")
plt.show()


# %% [markdown]
# #### Numberic only columns corr
# 

# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Compute correlation for all numeric columns
corr_all = df_expanded.corr(numeric_only=True)

# ---------------- Save correlation to CSV ----------------
corr_all.to_csv("Correlations\\correlation_matrix_numeric_only.csv")
print("Correlation matrix saved to correlation_matrix_numeric_only.csv")

# ---------------- Plot heatmap ----------------
plt.figure(figsize=(18, 10))

sns.heatmap(
    corr_all, 
    annot=True, 
    fmt=".2f", 
    cmap="coolwarm", 
    center=0,
    cbar_kws={'shrink': 0.8},
    linewidths=0.5
)

plt.title("Correlation Matrix (All Numeric Columns)", fontsize=16)
plt.tight_layout()
plt.savefig("correlation_matrix_numeric_only.png")
plt.close()

# ---------------- Create simple HTML ----------------
html_content = """
<h2>Correlation Matrix (All Numeric Columns)</h2>
<img src="correlation_matrix_numeric_only.png" alt="Correlation Matrix">
"""

with open("Correlations\\correlation_matrix_numeric_only.html", "w") as f:
    f.write(html_content)

print("Color-coded correlation matrix saved as HTML with embedded image.")


# %% [markdown]
# #### Encoded Corr
# 

# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Compute correlation for all numeric columns
corr_all = df_expanded.corr(numeric_only=True)

# ---------------- Save correlation to CSV ----------------
corr_all.to_csv("Correlations\\correlation_matrix_encoded.csv")
print("Correlation matrix saved to correlation_matrix_encoded.csv")

# ---------------- Plot heatmap ----------------
plt.figure(figsize=(18, 10))

sns.heatmap(
    corr_all, 
    annot=True, 
    fmt=".2f", 
    cmap="coolwarm", 
    center=0,
    cbar_kws={'shrink': 0.8},
    linewidths=0.5
)

plt.title("Correlation Matrix (All Numeric Columns)", fontsize=16)
plt.tight_layout()
plt.savefig("correlation_matrix_encoded.png")
plt.close()

# ---------------- Create simple HTML ----------------
html_content = """
<h2>Correlation Matrix (All Numeric Columns)</h2>
<img src="correlation_matrix_encoded.png" alt="Correlation Matrix">
"""

with open("Correlations\\correlation_matrix_encoded.html", "w") as f:
    f.write(html_content)

print("Color-coded correlation matrix saved as HTML with embedded image.")


# %% [markdown]
# ### Temporal Analysis
# 

# %%
import numpy as np
import pandas as pd

# Use 'sim_date' for temporal analysis
daily_counts = df_expanded.groupby('sim_date').size()
daily_counts.plot(figsize=(12,5))
plt.title("Number of Assessments Over Simulated Time")
plt.ylabel("Count")
plt.xlabel("Date")
plt.show()


# %% [markdown]
# ### Textual Notes (Doctors vs Patients)
# 
# #### Word Cloud or Top Keywords from phq9_doctors_notes and phq9_patients_notes.
# 

# %%
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

# Define custom stopwords
patient_stopwords = set([
    "patient", "patients", "consultation", "shows", "assessment", "exhibits", "during", "visit", "review", "progress",
    "continue", "consultations", "consult", "makes", "ve"
])
doctor_stopwords = set([
    "doctor", "doctors", "recommend", "suggest", "advised", "advice", "monitor", "required", "needed", "shows", "assessment", 
    "patient consultation", "patient exhibits", "consultation", "Patient continues","patient s",
])

# ---------------- Patients' Notes ----------------
patients_text = " ".join(df_expanded['phq9_patients_notes'].dropna())
patients_wc_stopwords = STOPWORDS.union(patient_stopwords)

patients_wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="black",
    colormap="Set2",
    max_words=200,
    stopwords=patients_wc_stopwords
).generate(patients_text)

# Display the wordcloud
plt.figure(figsize=(16, 8))
plt.imshow(patients_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Patient's Notes WordCloud", fontsize=20, color="black")
plt.show()

# Save word frequencies to CSV
patients_freq = pd.DataFrame(list(patients_wordcloud.words_.items()), columns=['word', 'frequency'])
patients_freq.to_csv("TopKeywords\\patients_notes_word_frequencies.csv", index=False)
print("Patients' notes word frequencies saved to patients_notes_word_frequencies.csv")

# ---------------- Doctors' Notes ----------------
doctors_text = " ".join(df_expanded['phq9_doctors_notes'].dropna())
doctors_wc_stopwords = STOPWORDS.union(doctor_stopwords)

doctors_wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="black",
    colormap="Set2",
    max_words=200,
    stopwords=doctors_wc_stopwords
).generate(doctors_text)

# Display the wordcloud
plt.figure(figsize=(16, 8))
plt.imshow(doctors_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Doctors' Notes WordCloud", fontsize=20, color="black")
plt.show()

# Save word frequencies to CSV
doctors_freq = pd.DataFrame(list(doctors_wordcloud.words_.items()), columns=['word', 'frequency'])
doctors_freq.to_csv("TopKeywords\\doctors_notes_word_frequencies.csv", index=False)
print("Doctors' notes word frequencies saved to doctors_notes_word_frequencies.csv")


# %% [markdown]
# ### Check how simulated dates are correlating with original dates
# 

# %%
from matplotlib.dates import DateFormatter
from sklearn.preprocessing import MinMaxScaler
import base64
from io import BytesIO
import matplotlib.pyplot as plt

html_blocks = []
scaler = MinMaxScaler(feature_range=(0, 1))

# Use the existing users_to_plot variable
# users_to_plot = np.array([...])  # already defined in your notebook

# Select users who have more than 4 records in df_expanded
user_counts = df_expanded['username'].value_counts()
users_to_plot = user_counts[user_counts > 4].index.values

for user in users_to_plot:
    user_df = df_expanded[df_expanded['username'] == user].copy()
    # Normalize dates to [0,1] for both columns
    for col in ['dsm5_created_at', 'sim_date']:
        if not pd.api.types.is_datetime64_any_dtype(user_df[col]):
            user_df[col] = pd.to_datetime(user_df[col])
        user_df[f'{col}_scaled'] = scaler.fit_transform(user_df[[col]].astype('int64'))

    for date_col, date_label in [('dsm5_created_at', 'DSM5 Created At'), ('sim_date', 'Simulated Date')]:
        fig, axes = plt.subplots(1, 2, figsize=(12, 3))
        # Plot 1: count vs date
        counts = user_df.groupby(date_col).size()
        axes[0].plot(counts.index, counts.values, marker='o')
        axes[0].set_title(f'{user}\nCount vs {date_label}')
        axes[0].set_xlabel(date_label)
        axes[0].set_ylabel('Count')
        axes[0].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        axes[0].tick_params(axis='x', rotation=45)

        # Plot 2: totalcount vs date (cumulative)
        total_counts = counts.cumsum()
        axes[1].plot(total_counts.index, total_counts.values, marker='o', color='orange')
        axes[1].set_title(f'{user}\nCumulative Count vs {date_label}')
        axes[1].set_xlabel(date_label)
        axes[1].set_ylabel('Cumulative Count')
        axes[1].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        axes[1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        html_blocks.append(f'<h3>{user} - {date_label}</h3><img src="data:image/png;base64,{img_base64}"/>')

# Write to HTML file
with open('SimulatedDates\\user_assessment_comparison.html', 'w') as f:
    f.write('<html><body>' + ''.join(html_blocks) + '</body></html>')

print("Saved to user_assessment_comparison.html")


# %% [markdown]
# ## Data with simulated date looks good, can consider the simulated dates for timeseries prediction
# 
# for reference check:
# [user_assessment_comparison.html](SimulatedDates\user_assessment_comparison.html)
# 

# %% [markdown]
# # Feature Engineering
# 

# %%
pprint.pprint(df_expanded.head(1).to_dict(orient='records'))

# %% [markdown]
# #### Gender Label Encoding
# 

# %%
from sklearn.preprocessing import LabelEncoder

# Encode gender
le_gender = LabelEncoder()
df_expanded['gender_enc'] = le_gender.fit_transform(df_expanded['gender'].astype(str))

# Save the mapping for reference
gender_mapping = pd.DataFrame({
    'gender': le_gender.classes_,
    'gender_enc': range(len(le_gender.classes_))
})
gender_mapping.to_csv("Labels\\label_mapping_gender.csv", index=False)

df_expanded[['gender', 'gender_enc']].head()


# %% [markdown]
# #### Age Buckets
# 

# %%
bins = [0, 25, 35, 45, 55, 65, 100]
labels = ['18-25','26-35','36-45','46-55','56-65','65+']
df_expanded['age_bucket'] = pd.cut(df_expanded['age'], bins=bins, labels=labels)
df_expanded['age_bucket_enc'] = LabelEncoder().fit_transform(df_expanded['age_bucket'].astype(str))


# %%
df_expanded_vanilla = df_expanded.copy()

# %% [markdown]
# ## NLP Sentiment Analysis on Notes
# 

# %% [markdown]
# #### Sentiment
# 

# %%
from textblob import TextBlob

df_expanded['patients_sentiment'] = df_expanded['phq9_patients_notes'].dropna().apply(lambda x: TextBlob(x).sentiment.polarity)
df_expanded['doctors_sentiment'] = df_expanded['phq9_doctors_notes'].dropna().apply(lambda x: TextBlob(x).sentiment.polarity)


# %% [markdown]
# #### Keyword Features from notes
# 
# Keywords based of DSM-5 and NICE guidelines symptoms and from generated templates
# 

# %%
# Borrowed from Data Generation Code
symptoms_bank = {
    "None-minimal": [
        "slight fatigue", "occasional low mood", "mild worry", "sometimes feeling distracted",
        "feeling a bit down in the evenings", "minor changes in sleep patterns"
    ],
    "Mild": [
        "feeling tired", "trouble concentrating", "occasional sadness", "low energy during the day",
        "feeling restless", "minor irritability", "difficulty enjoying usual activities"
    ],
    "Moderate": [
        "loss of interest in hobbies", "sleep disturbances", "low motivation", "persistent fatigue",
        "frequent negative thoughts", "difficulty focusing at work", "feeling lonely"
    ],
    "Moderately Severe": [
        "persistent sadness", "difficulty functioning", "frequent irritability", "problems with daily routine",
        "social withdrawal", "significant drop in motivation", "feeling overwhelmed most of the day"
    ],
    "Severe": [
        "hopelessness", "thoughts of self-harm", "inability to get out of bed", "severe anxiety attacks",
        "extreme lack of energy", "loss of interest in eating or personal care",
        "persistent guilt and self-criticism", "intense fear of future"
    ]
}

feelings_bank = {
    "None-minimal": ["okay", "manageable", "slightly low", "a bit tired", "generally fine"],
    "Mild": ["down", "unmotivated", "anxious", "irritable", "uneasy", "restless", "bored"],
    "Moderate": ["sad", "discouraged", "frustrated", "lonely", "overwhelmed", "gloomy", "confused"],
    "Moderately Severe": ["hopeless", "overwhelmed", "exhausted", "disconnected", "distraught", "disheartened"],
    "Severe": ["desperate", "worthless", "completely drained", "trapped", "fearful", "helpless"]
}

daily_impacts = [
    "sleep has been affected", "appetite is irregular", "struggling to concentrate at work",
    "finding it hard to maintain social connections", "energy levels fluctuate during the day",
    "difficulty managing daily chores", "mood swings are noticeable", "motivation is extremely low"
]

doctor_recommendations = {
    "None-minimal": [
        "No active intervention needed. Continue monitoring.",
        "Encourage maintaining healthy routines and self-care."
    ],
    "Mild": [
        "Consider guided self-help or low-intensity CBT.",
        "Recommend mindfulness exercises and monitoring symptoms."
    ],
    "Moderate": [
        "Recommend structured therapy, monitor closely.",
        "Cognitive Behavioral Therapy (CBT) advised, review progress in next visit."
    ],
    "Moderately Severe": [
        "Combination of therapy and possible medication referral.",
        "Suggest referral to mental health specialist, monitor risk factors."
    ],
    "Severe": [
        "Urgent psychiatric evaluation and safety planning required.",
        "Immediate intervention recommended; consider inpatient care if risk escalates."
    ]
}

# %%
patient_keywords = set()

# Add all symptoms
for severity in symptoms_bank:
    patient_keywords.update(symptoms_bank[severity])

# Add all feelings
for severity in feelings_bank:
    patient_keywords.update(feelings_bank[severity])

# Add daily impacts
patient_keywords.update(daily_impacts)


# %%
print(patient_keywords)

# %%
import re

doctor_keywords = set()

# Add severity words
doctor_keywords.update(["None-minimal", "Mild", "Moderate", "Moderately Severe", "Severe"])

# Add recommendation words
for severity in doctor_recommendations:
    for rec in doctor_recommendations[severity]:
        # Lowercase and split
        words = rec.lower().split()
        # Keep only alphanumeric words longer than 2 letters
        filtered_words = [re.sub(r'[^a-z0-9]', '', w) for w in words]  # remove non-alphanumeric
        filtered_words = [w for w in filtered_words if len(w) > 2]       # remove words <= 2 letters
        doctor_keywords.update(filtered_words)

print(doctor_keywords)


# %%
# Generate binary features
for kw in patient_keywords:
    df_expanded[f'patient_{kw}'] = df_expanded['phq9_patients_notes'].str.contains(kw, case=False, na=False).astype(int)

for kw in doctor_keywords:
    df_expanded[f'doctor_{kw}'] = df_expanded['phq9_doctors_notes'].str.contains(kw, case=False, na=False).astype(int)


# %% [markdown]
# #### Suicide risk score
# 

# %%
suicide_keywords = [
    "thoughts of self-harm", "hopelessness", "desperate", "worthless", "trapped", "helpless", "fearful"
]

# %%
# Patient notes suicide score
df_expanded['patient_suicide_score'] = df_expanded[
    [col for col in df_expanded.columns if any(kw in col for kw in suicide_keywords)]
].sum(axis=1)

# Doctor notes suicide score
df_expanded['doctor_suicide_score'] = df_expanded[
    [col for col in df_expanded.columns if any(kw in col for kw in suicide_keywords)]
].sum(axis=1)


# %% [markdown]
# #### Anxiety Score
# 

# %%
anxiety_keywords = ["anxious", "restless", "irritable", "uneasy"]

# %%
df_expanded['patient_anxiety_score'] = df_expanded[
    [col for col in df_expanded.columns if any(kw in col for kw in anxiety_keywords)]
].sum(axis=1)

df_expanded['doctor_anxiety_score'] = df_expanded[
    [col for col in df_expanded.columns if any(kw in col for kw in anxiety_keywords)]
].sum(axis=1)


# %% [markdown]
# #### Total Clinical Severity Score
# 

# %%
clinical_keywords = list(patient_keywords)

df_expanded['patient_symptom_score'] = df_expanded[
    [col for col in df_expanded.columns if any(kw in col for kw in clinical_keywords)]
].sum(axis=1)

df_expanded['doctor_symptom_score'] = df_expanded[
    [col for col in df_expanded.columns if any(kw in col for kw in clinical_keywords)]
].sum(axis=1)

# %% [markdown]
# ## Time Features
# 
# Using simulated time
# 

# %% [markdown]
# #### Consultation sequence per patient
# 

# %%
df_expanded = df_expanded.sort_values(['username', 'sim_date'])
df_expanded['consultation_seq'] = df_expanded.groupby('username').cumcount() + 1

# %% [markdown]
# #### Days since last visit
# 

# %%
df_expanded['days_since_last'] = df_expanded.groupby('username')['sim_date'].diff().dt.days.fillna(0)

# %%
pprint.pprint(df_expanded.head(1).to_dict(orient='records'))

# %%
# Shape and datatypes
print(df_expanded.shape)
print(df_expanded.dtypes)

# Null counts
print(df_expanded.isnull().sum())

# Quick summary
print(df_expanded.describe(include="all"))


# %%
df_expanded.to_csv("ProcessedData\\processed_assessments.csv", index=False)

# %%
feature_cols = [
    'patient_suicide_score', 'doctor_suicide_score',
    'patient_anxiety_score', 'doctor_anxiety_score',
    'patient_symptom_score', 'doctor_symptom_score'
]

df_expanded[feature_cols].to_csv("ProcessedData\\nlp_composite_features.csv", index=False)
print("NLP composite features saved to CSV")


# %% [markdown]
# ## Summarize
# 

# %%
import pandas as pd
import pprint
import json

def summarize_dataframe(df):
    """Comprehensive summary of a DataFrame as a dictionary (updated for latest pandas)."""
    
    summary = {
        'Total Columns': df.shape[1],
        'Column Names': list(df.columns),
        'Columns': {}
    }
    
    for col in df.columns:
        col_data = df[col]
        col_summary = {}
        
        # Basic info
        col_summary['DataType'] = str(col_data.dtype)
        col_summary['Non-Null Count'] = int(col_data.notnull().sum())
        col_summary['Null Count'] = int(col_data.isnull().sum())
        col_summary['Unique Values'] = int(col_data.nunique())
        
        # Numeric stats
        if pd.api.types.is_numeric_dtype(col_data):
            col_summary['Mean'] = float(col_data.mean())
            col_summary['Median'] = float(col_data.median())
            col_summary['Std'] = float(col_data.std())
            col_summary['Min'] = float(col_data.min())
            col_summary['Max'] = float(col_data.max())
        else:
            col_summary['Mean'] = None
            col_summary['Median'] = None
            col_summary['Std'] = None
            col_summary['Min'] = None
            col_summary['Max'] = None
        
        # Categorical stats (updated)
        if pd.api.types.is_object_dtype(col_data) or isinstance(col_data.dtype, pd.CategoricalDtype):
            top_val = col_data.mode()
            col_summary['Top'] = top_val.iloc[0] if not top_val.empty else None
            col_summary['Freq'] = int(col_data.value_counts().max()) if not col_data.value_counts().empty else 0
        else:
            col_summary['Top'] = None
            col_summary['Freq'] = None
        
        summary['Columns'][col] = col_summary
    
    return summary

# Usage
df_summary_dict = summarize_dataframe(df_expanded)

# Pretty print
pprint.pprint(df_summary_dict)

# Save as JSON
with open("ProcessedData\\df_summary.json", "w") as f:
    json.dump(df_summary_dict, f, indent=4)

print("DataFrame summary saved as df_summary.json")


# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Compute correlation for all numeric columns
corr_all = df_expanded.corr(numeric_only=True)

# ---------------- Save correlation to CSV ----------------
corr_all.to_csv("Correlations\\correlation_matrix_170_features.csv")
print("Correlation matrix saved to correlation_matrix_170_features.csv")

# ---------------- Plot heatmap ----------------
n_features = corr_all.shape[0]

# Dynamic figure size (scale with number of features)
fig_size = max(10, n_features)  # scale
plt.figure(figsize=(fig_size, fig_size))

# For large feature sets, skip annotations
annot_flag = n_features <= 30  

sns.heatmap(
    corr_all,
    annot=annot_flag,
    fmt=".2f" if annot_flag else "",
    cmap="coolwarm",
    center=0,
    cbar_kws={'shrink': 0.5},
    linewidths=0.1
)

plt.title(f"Correlation Matrix ({n_features} Numeric Columns)", fontsize=10)
plt.tight_layout()
plt.savefig("Correlations\\correlation_matrix_170_features.png", dpi=300)
plt.close()

# ---------------- Create simple HTML ----------------
html_content = f"""
<h2>Correlation Matrix ({n_features} Numeric Columns)</h2>
<img src="correlation_matrix_170_features.png" alt="Correlation Matrix" style="max-width:100%;">
"""

with open("Correlations\\correlation_matrix_170_features.html", "w") as f:
    f.write(html_content)

print(f"Color-coded correlation matrix ({n_features} features) saved as HTML with embedded image.")


# %% [markdown]
# # Timeseries using XGBoost
# 

# %%
# Load your existing dataframe (assuming it's already in memory as df_expanded)
df = df_expanded.copy()

# Ensure correct sorting
df = df.sort_values(["username", "sim_date"]).reset_index(drop=True)

# Add consultation sequence per patient
df["consult_num"] = df.groupby("username").cumcount() + 1

# Add "days since last consult"
df["days_since_last"] = df.groupby("username")["sim_date"].diff().dt.days.fillna(0)

# %%
feature_cols = [
    "phq9_total_score", "dsm5_severity_enc", "dsm5_q9_flag_enc",
    "consult_num", "days_since_last"
] + [col for col in df.columns if col.startswith("phq9_q")] \
  + [col for col in df.columns if col.startswith("patient_")] \
  + [col for col in df.columns if col.startswith("doctor_")]


# %%
# target: next severity class
df["target_severity"] = df.groupby("username")["dsm5_severity_enc"].shift(-1)

# drop rows with no target (last consults)
df = df.dropna(subset=["target_severity"])

X = df[feature_cols]
y = df["target_severity"]


# %%
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)

for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
    print(f"Fold {fold+1}")
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]


# %%
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

# Train model
xgb_model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
xgb_model.fit(X_train, y_train)

# Predictions
y_pred = xgb_model.predict(X_test)

# Reset indices for alignment
X_test_reset = X_test.reset_index(drop=True)
y_test_reset = y_test.reset_index(drop=True)

# Map severity encoding back to labels
severity_labels = {
    0: "None-minimal",
    1: "Mild",
    2: "Moderate",
    3: "Moderately Severe",
    4: "Severe"
}

# Create results dataframe
results_df = pd.DataFrame({
    "Consult_Num": X_test_reset["consult_num"],
    "Actual_Severity": y_test_reset.map(severity_labels),
    "Predicted_Severity": pd.Series(y_pred).map(severity_labels)
})

# Add correctness column
results_df["Correct"] = results_df["Actual_Severity"] == results_df["Predicted_Severity"]

# Print sample comparison
print("\n===== Prediction Comparison (Actual vs Predicted) =====\n")
for _, row in results_df.head(20).iterrows():  # show first 20 for readability
    status = "✅ Correct" if row["Correct"] else "❌ Wrong"
    print(f"Consult {row['Consult_Num']}: "
          f"Actual = {row['Actual_Severity']}, "
          f"Predicted = {row['Predicted_Severity']} --> {status}")

# Overall accuracy
accuracy = accuracy_score(y_test_reset, y_pred)
print("\n===== Overall Accuracy =====")
print(f"Model Accuracy: {accuracy:.2%}")


# %%
import matplotlib.pyplot as plt
import xgboost as xgb

xgb.plot_importance(xgb_model, max_num_features=20, importance_type="gain")
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Patient only features
# 

# %%
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# ---------- PATIENT-ONLY FEATURE SET ----------
patient_features = [
    "phq9_total_score",
    "consult_num",
    "days_since_last",
] + [col for col in df.columns if col.startswith("phq9_q")] \
  + [col for col in df.columns if col.startswith("patient_")]

X_patient = df[patient_features]
y_patient = df["target_severity"]

# Train/test split
from sklearn.model_selection import train_test_split
X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X_patient, y_patient, test_size=0.2, shuffle=False
)

# Train model
patient_model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
patient_model.fit(X_train_p, y_train_p)

# Predict
y_pred_p = patient_model.predict(X_test_p)

# Results
print("\n===== PATIENT-ONLY MODEL =====")
print("Accuracy:", accuracy_score(y_test_p, y_pred_p))
print(classification_report(y_test_p, y_pred_p))

# Feature importance
import matplotlib.pyplot as plt
import xgboost as xgb
xgb.plot_importance(patient_model, max_num_features=15)
plt.title("Patient-Only Feature Importance")
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Doctor + Patient
# 

# %%
# ---------- FULL FEATURE SET (Doctor + Patient) ----------
doctor_patient_features = patient_features + [col for col in df.columns if col.startswith("doctor_")] + [
    "dsm5_severity_enc", "dsm5_q9_flag_enc"
]

X_full = df[doctor_patient_features]
y_full = df["target_severity"]

# Train/test split
X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(
    X_full, y_full, test_size=0.2, shuffle=False
)

# Train model
full_model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
full_model.fit(X_train_f, y_train_f)

# Predict
y_pred_f = full_model.predict(X_test_f)

# Results
print("\n===== DOCTOR + PATIENT MODEL =====")
print("Accuracy:", accuracy_score(y_test_f, y_pred_f))
print(classification_report(y_test_f, y_pred_f))

# Feature importance
xgb.plot_importance(full_model, max_num_features=15)
plt.title("Doctor + Patient Feature Importance")
plt.tight_layout()
plt.show()


# %% [markdown]
# #### Dtypes of df
# 

# %%
# Dict comprehension: map column name -> dtype
df_col_check = df_expanded_vanilla.copy()
col_dtype_map = {col: str(dtype) for col, dtype in zip(df_col_check.columns, df_col_check.dtypes)}

# Print one by one
for col, dtype in col_dtype_map.items():
    print(f"{col}: {dtype},")


# %% [markdown]
# #### Vanilla df Predection using xgboost
# 

# %%
import pandas as pd
import xgboost as xgb
from sklearn.metrics import root_mean_squared_error

# Sort by time
df = df_expanded.sort_values("sim_date")

# Features and target
features = [
    'age', 'gender_enc', 'industry_enc', 'profession_enc',
    'phq9_q0','phq9_q1','phq9_q2','phq9_q3','phq9_q4',
    'phq9_q5','phq9_q6','phq9_q7','phq9_q8',
    'dsm5_q9_flag_enc','dsm5_mdd_assessment_enc',
    'dsm5_severity_enc', 'age_bucket_enc'
]
target = 'phq9_total_score'

X = df[features]
y = df[target]

# Time series split: first 80% train, last 20% test
split_index = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

# Initialize XGBRegressor with early stopping rounds
model = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    tree_method='auto',  # remove if CPU only
    early_stopping_rounds=50,
    eval_metric='rmse',
    verbose=20
)

# Fit with validation set passed to fit()
model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)]
)

# Predict
y_pred = model.predict(X_test)

# Evaluate
df_expanded_rmse = root_mean_squared_error(y_test, y_pred)
print(f"Test RMSE: {df_expanded_rmse}")


# %%
import pandas as pd

# Create DataFrame with actual vs predicted
results_df = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_pred
}, index=y_test.index)

# Show first 20 rows
print(results_df.head(20))

# Optionally save to CSV for deeper look
results_df.to_csv("phq9_predictions_vs_actual.csv", index=False)


# %%
from sklearn.metrics import r2_score

r2 = r2_score(y_test, y_pred)
print(f"R² Score: {r2:.4f}")


# %%
tolerance = 2  # allow ±2 points difference
within_tol = (abs(results_df["Actual"] - results_df["Predicted"]) <= tolerance).mean()

print(f"Accuracy within ±{tolerance}: {within_tol*100:.2f}%")


# %%
plt.figure(figsize=(7,7))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         color="red", linestyle="--")  # perfect prediction line
plt.xlabel("Actual PHQ-9 Score")
plt.ylabel("Predicted PHQ-9 Score")
plt.title("Actual vs Predicted PHQ-9 Scores")
plt.show()


# %%
residuals = y_test.values - y_pred

plt.figure(figsize=(10,6))
plt.scatter(range(len(residuals)), residuals, alpha=0.6)
plt.axhline(0, color="red", linestyle="--")
plt.xlabel("Test Sample Index")
plt.ylabel("Residual (Actual - Predicted)")
plt.title("Residuals for Test Set")
plt.show()


# %%



