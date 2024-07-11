import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the data
data = pd.read_csv('raw_data/battle_logs_07-10-2024_10:05_am_5M.csv')

# Preprocess the data
categorical_features = ['battle_mode', 'map_name', 'winner_1', 'winner_2', 'winner_3', 'loser_1', 'loser_2', 'loser_3']

# Define the target (assuming 'winner_1' for the purpose of this example)
target = 'winner_1'  # Adjust this to your actual target column

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# Separate features and target
X = data[categorical_features]
y = data[target]

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with preprocessing and a classifier model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42, n_estimators=50, max_depth=10))
])

# Measure training time
start_time = time.time()
pipeline.fit(X_train, y_train)
end_time = time.time()

training_time = end_time - start_time
print(f'Training time for {len(data)} rows: {training_time:.2f} seconds')

# Predict on the test set
y_pred = pipeline.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print(f'Classification Report:\n{report}')

# Save the pipeline (including the preprocessor and the classifier)
joblib.dump(pipeline, 'models/random_forest.pkl')
print("Model saved successfully!")
