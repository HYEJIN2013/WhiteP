import librosa
import jams
import os
import mutagen
import argparse
import requests

n_fft = 4096
hop_length = n_fft/2


def get_annotation_metadata():
    c = jams.Curator(name="Hugh Rawlinson", email="mu202hr@gold.ac.uk")
    return jams.AnnotationMetadata(curator=c,
                                   annotation_rules="frame length 4096,hop size 2048",
                                   annotation_tools="librosa")


def get_jams(filepath):
    filename = filepath.split('/')[-1]
    try:
        y, sr = librosa.load(filepath)
    except(Exception):
        return
    track_duration = librosa.get_duration(y=y, sr=sr)
    jam = jams.JAMS()
    jam.file_metadata.duration = track_duration
    jam.file_metadata.identifiers.update(filename=filename)
    md = get_annotation_metadata()
    md.annotator = {'feature': "Spectral Centroid"}
    c_annotation = jams.Annotation(namespace='vector', annotation_metadata=md)
    centroids = get_centroid(y, sr)
    md.annotator = {'feature': "RMS"}
    r_annotation = jams.Annotation(namespace='vector', annotation_metadata=md)
    rmss = get_rmse(y, sr)
    md.annotator = {'feature': "Spectral Rolloff"}
    ro_annotation = jams.Annotation(namespace='vector', annotation_metadata=md)
    rolloffs = get_rolloff(y, sr)
    md.annotator = {'feature': "MFCCs"}
    mfcc_annotation = jams.Annotation(namespace='vector', annotation_metadata=md)
    mfccs = get_mfccs(y, sr)
    for index, value in enumerate(centroids):
        time = (hop_length*index)/float(sr)
        c_annotation.append(value=value, duration=0.0, time=time)
        r_annotation.append(value=rmss[index], duration=0.0, time=time)
        ro_annotation.append(value=rolloffs[index], duration=0.0, time=time)
        mfcc_annotation.append(value=rolloffs[index], duration=0.0, time=time)
    jam.annotations.append(c_annotation)
    jam.annotations.append(r_annotation)
    jam.annotations.append(ro_annotation)
    jam.annotations.append(mfcc_annotation)
    try:
        md = get_song_metadata(filepath)
        jam.file_metadata.title = md.tags['title']
        jam.file_metadata.artist = md.tags['artist']
        jam.file_metadata.release = md.tags['album']
    except(Exception):
        print "metadata not found for file "+filename
    print "returning file "+filename
    return jam


def get_song_metadata(filepath):
    f = mutagen.File(filepath)
    return f


def get_centroid(y, sr):
    c = librosa.feature.spectral_centroid(y, sr, None, n_fft, hop_length)
    return c.reshape(-1)


def get_rmse(y, sr):
    rmse = librosa.feature.rmse(y, None, n_fft, hop_length)
    return rmse.reshape(-1)


def get_rolloff(y, sr):
    rolloff = librosa.feature.spectral_rolloff(y, sr, None, n_fft, hop_length)
    return rolloff.reshape(-1)

def get_mfccs(y, sr):
    rolloff = librosa.feature.mfcc(y, sr, None, n_mfcc=12, n_fft=n_fft, hop_length=hop_length)
    return rolloff.reshape(-1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Recursively search for audio files in a directory, perform analysis, upload for Hugh')
    parser.add_argument('--path', dest='path', action='store',
                        default=os.getcwd(),
                        help='path containing audio files')

    args = parser.parse_args()
    args.path = os.path.abspath(os.path.expanduser(args.path))
    for file in librosa.util.find_files(args.path):
        requests.put("http://jams.hughrawlinson.me/jams", data=get_jams(file).dumps())
