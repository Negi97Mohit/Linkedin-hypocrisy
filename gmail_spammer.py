
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual values
CLIENT_ID = '595141379598-c24m9vpfii9q7pgqpn71oj35g1eqmrqq.apps.googleusercontent.com'
CLIENT_SECRET = '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'

# Path to the file containing the user's OAuth 2.0 credentials
CREDENTIALS_FILE = "C:/Linkedin-hypocrisy/creds.json"


# Scope for accessing Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    # Load OAuth 2.0 credentials from file
    creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, scopes=SCOPES)

    # Build Gmail service object
    service = build('gmail', 'v1', credentials=creds)

    # Retrieve labels
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

if __name__ == '__main__':
    main()
