# Video Analysis with Google Cloud

A simple python script to upload a local video to Google Cloud Storage, or retreive a video from GCS, then output the transcription of the video.

## Requirments
### Google Cloud
1. Google Cloud account with Storage API and Video Intelligence API enabled
2. A Project created within the account
3. A Bucket created for the project
4. A Service Account credentials for the project (typically a JSON file)

(Refer to Google Cloud docs for getting this set up)

### Local Development
```
>>> python --version
Python 3.7.3

>>> cd path/to/gc-video-analysis
>>> pip install requirements.txt
```

Once you've created a Service Account and generated the credentials, place your `.json` file in `./credentials` directory. The progam looks for a file called `service_account.json` by default, but you can provide an alterate path. This file is ignored by `git`.

## Usage
```
>>> python upload_and_analyze.py --help
usage: upload_and_analyze.py [-h] [--gcs_uri GCS_URI] [--source SOURCE]
                             [--destination DESTINATION] [--bucket BUCKET]
                             [--prefix PREFIX] [--credentials CREDENTIALS]

Uploads a file from local file system to Google Cloud Storage, or fetches
video from GCS, then analyses it

optional arguments:
  -h, --help            show this help message and exit
  --gcs_uri GCS_URI     gs://path/to/video; skips gs upload if provided
  --source SOURCE       local/path/to/file
  --destination DESTINATION
                        storage-object-name
  --bucket BUCKET       your-bucket-name (default: another-linda-bucket)
  --prefix PREFIX       GCS blob prefix (default: video-analysis)
  --credentials CREDENTIALS
                        GCS service account credentials json file (default:
                        credentials/service_account.json)
```

Either `--gcs_uri`, or `--source` and `--destination`, MUST be provided.

`source` videos can be locally stored in the `/videos` directory. The contents are ignored by `git`.



