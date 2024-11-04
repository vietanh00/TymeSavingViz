import pandas as pd
from io import StringIO

# Read the features data
features_data = pd.read_csv(StringIO("""
Feature;Description;Keywords
User;"Include sign up, log in, view and manage user information";"user,signin,signup"
Transaction;"Include CRUD, reports, lists, approve and decline";"transaction"
SharedBudget;"Include CRUD, reports, lists, members, amount update";"sharedBudget,budget"
GroupSaving;"Include CRUD, reports, lists, members, amount update";"groupsaving,saving"
Invitation;"Include CRUD, accept, cancel";"invitation,invite"
FinancialChallenge;"Include CRUD, amount update, progress tracking, reward allocation";"challenge,checkpoint,progress,reward,point"
Assets;"Different assets used when rendering the application";"asset,res,png,svg"
"""))

# Read the frontend_file_feature data
frontend_data = pd.read_csv(StringIO("""
filename
app/api/user/[username]/route.ts
"""))

# Create a function to check if a filename matches any keyword
def filename_matches_keywords(filename, keywords):
    return any(keyword.lower() in filename.lower() for keyword in keywords.split(','))

# Apply the function to create a new column
frontend_data['Feature'] = frontend_data['filename'].apply(lambda x: features_data.loc[features_data['Keywords'].str.contains('|'.join(features_data['Keywords'].split(',')[0::2])), 'Feature'].iloc[0] if filename_matches_keywords(x, features_data['Keywords'].iloc[0]) else '')

# Display the result
print(frontend_data)
