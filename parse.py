import csv

whichend = "backend"
# Input and Output file paths
input_file = whichend + "_commits.txt"
commit_output_file = "./export/" + whichend + "_commits.csv"
filechange_output_file = "./export/" + whichend + "_filechange.csv"

# Data storage for commits and file changes
commit_data = []
filechange_data = []

# Variables to track the current commit details
current_commit = None
total_added = 0
total_deleted = 0

# Function to clean null characters from strings
def clean_null_chars(s):
    return s.replace('\x00', '').strip()

# Read the git log file
with open(input_file, "r", encoding="utf-16") as file:
    for line in file:
        line = line.strip()

        # If line contains commit info (commit id | description | date)
        if "|" in line:
            # Save previous commit data if it exists
            if current_commit:
                commit_data.append(current_commit + [total_added, total_deleted])

            # Reset for the new commit
            commit_id, description, username, date = line.split("|")
            current_commit = [commit_id, description, username, date]
            total_added = 0
            total_deleted = 0

        # If the line is not empty and contains file change info
        elif line:
            # Try to split by tab, but check the length of the result first
            parts = line.split("\t")
            if len(parts) == 3:
                added, deleted, file_name = parts
                
                # Clean null characters from each part
                added = clean_null_chars(added)
                deleted = clean_null_chars(deleted)
                file_name = clean_null_chars(file_name)

                try:
                    added = int(added)
                    deleted = int(deleted)
                except ValueError:
                    # Handle cases where the added/deleted are not integers
                    added = deleted = 0

                # Update total lines added/deleted for the current commit
                total_added += added
                total_deleted += deleted

                # Record the file change
                filechange_data.append([current_commit[0], file_name, added, deleted])

# Save the last commit data
if current_commit:
    commit_data.append(current_commit + [total_added, total_deleted])

# Write commit data to commit.csv
with open(commit_output_file, mode="w", newline="", encoding="utf-8") as commit_csv:
    writer = csv.writer(commit_csv)
    writer.writerow(["commit_id", "description", "username", "date", "code_added", "code_deleted"])
    writer.writerows(commit_data)

# Write file change data to filechange.csv
with open(filechange_output_file, mode="w", newline="", encoding="utf-8") as filechange_csv:
    writer = csv.writer(filechange_csv)
    writer.writerow(["commit_id", "file_name", "code_added", "code_deleted"])
    writer.writerows(filechange_data)

print(f"Data has been written to {commit_output_file} and {filechange_output_file}.")

