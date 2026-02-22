# Import the necessary libraries to work with file operations and globbing.
import glob
import os
import datetime
from pathlib import Path

# https://www.geeksforgeeks.org/append-text-or-lines-to-a-file-in-python/
def append_text_to_file(file_path, text_to_append):
  try:
    with open(file_path, 'a') as file:
      file.write(text_to_append + '\n')
    # print('Text appended to {file_path} successfully')
  except Exception as e:
    print('Error: {e}')

# https://www.w3resource.com/python-exercises/python-basic-exercise-70.php
# https://sentry.io/answers/get-the-last-element-of-a-list-in-python/
# Use the glob module to find all files in the current directory.
jobsPath = "/var/www/10/oranta/sites/oranta.kapsi.fi/jobs/missing_squadrats"
logPath = '/home/users/oranta/missingSquadrats.log'
jobsDirContent = glob.glob(os.path.join(jobsPath, "*.sh"))
if len(jobsDirContent) > 0 and not(os.path.exists(os.path.join(jobsPath, "inProcess"))):
  # Sort the list of file names based on the modification time (getmtime) of each file.
  jobsDirContent.sort(key=os.path.getmtime)
  # Print the sorted list of file names, one per line.
  print("\n".join(jobsDirContent))
  # Append a timestamp to the log file
  # https://www.geeksforgeeks.org/get-current-date-and-time-using-python/
  text_to_append = datetime.datetime.now()
  append_text_to_file(logPath, text_to_append.strftime("%Y.%m.%d %H:%M:%S"))
  # Create inProgres file
  # https://www.geeksforgeeks.org/create-an-empty-file-using-python/
#  with open(os.path.join(jobsPath, "inProcess"), 'w') as fp:
#    pass
  # Run the latest runMissingSquadrats
  os.system('sh ' + jobsDirContent[0] + ' >> /home/users/oranta/missingSquadrats.log 2>&1')
  # Check if the run was succesfull and remove the inProgress file
  text_to_append = datetime.datetime.now()
  append_text_to_file(logPath, text_to_append.strftime("%Y.%m.%d %H:%M:%S"))

baseDir = Path(__file__).parent.parent.parent

