import argparse
from google.cloud import storage
from google.cloud import videointelligence
import time

def do_upload(storage_client, bucket_name, source, destination):
  print('\nUploading video to GCS...')

  start_time = time.time()

  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(destination)
  blob.upload_from_filename(args.source)

  gcs_path = 'gs://%s/%s' % (bucket_name, destination)

  end_time = time.time()

  print('Successfully uploaded video to %s [%ds]' % (gcs_path, end_time - start_time))

  return gcs_path


def do_speech_transcription(video_client, input_uri):
  features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]

  config = videointelligence.types.SpeechTranscriptionConfig(
      language_code="en-US", enable_automatic_punctuation=True
  )
  video_context = videointelligence.types.VideoContext(
      speech_transcription_config=config
  )

  start_time = time.time()

  operation = video_client.annotate_video(input_uri=input_uri, features=features, video_context=video_context)

  print('\nProcessing video from %s (timeout in 600s)' % input_uri)

  result = operation.result(timeout=600)

  end_time = time.time()

  print('Finished transcribing video [%ds]' % (end_time - start_time))

  # There is only one annotation_result since only
  # one video is processed.
  annotation_results = result.annotation_results[0]
  for speech_transcription in annotation_results.speech_transcriptions:

      # The number of alternatives for each transcription is limited by
      # SpeechTranscriptionConfig.max_alternatives.
      # Each alternative is a different possible transcription
      # and has its own confidence score.
      for alternative in speech_transcription.alternatives:
          print("\nAlternative level information:")

          print("\tTranscript: {}".format(alternative.transcript))
          print("\tConfidence: {}\n".format(alternative.confidence))

          print("\tWord level information:")
          for word_info in alternative.words:
              word = word_info.word
              start_time = word_info.start_time
              end_time = word_info.end_time
              print(
                  "\t\t{}s - {}s: {}".format(
                      start_time.seconds + start_time.nanos * 1e-9,
                      end_time.seconds + end_time.nanos * 1e-9,
                      word,
                  )
              )

def main(args):

  print('Running upload_and_analyze with inputs:')
  print('\t[gcs_uri] = %s' % args.gcs_uri)
  print('\t[bucket] = %s' % args.bucket)
  print('\t[source] = %s' % args.source)
  print('\t[destination] = %s' % args.destination)
  print('\t[credentials] = %s' % args.credentials)
  print('\t[prefix] = %s' % args.prefix)
  
  # Intialize clients
  storage_client = storage.Client.from_service_account_json(args.credentials)
  video_client = videointelligence.VideoIntelligenceServiceClient.from_service_account_json(args.credentials)

  # Determine or get video GCS uri
  input_uri = ''
  if args.gcs_uri is not None:
    input_uri = args.gcs_uri
  else:
    input_uri = do_upload(storage_client, args.bucket, args.source, '%s/%s' % (args.prefix, args.destination))
  
  do_speech_transcription(video_client, input_uri)

  
if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='Uploads a file from local file system to Google Cloud Storage, or fetches video from GCS, then analyses it'
  )

  # Provide this, OR
  parser.add_argument('--gcs_uri', help='gs://path/to/video; skips gs upload if provided')

  # Provide these
  parser.add_argument('--source', help='local/path/to/file')
  parser.add_argument('--destination', help='storage-object-name')
  parser.add_argument('--bucket', help='your-bucket-name (default: another-linda-bucket)', default='another-linda-bucket')
  parser.add_argument('--prefix', help='GCS blob prefix (default: video-analysis)', default='video-analysis')
  
  parser.add_argument('--credentials', help='GCS service account credentials json file (default: credentials/service_account.json)', default='credentials/service_account.json')
  
  args = parser.parse_args()

  main(args)