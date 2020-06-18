import os
import argparse 

import numpy as np
from scipy.io import wavfile 
from hmmlearn import hmm
from python_speech_features import mfcc

def build_arg_parser():
    parser = argparse.ArgumentParser(description='Trains the HMM classifier')
    parser.add_argument("--input-folder", dest="input_folder", required=True, help="Input folder containing the audio files in subfolders")
    parser.add_argument("--transcribe", dest="transcribe", required=True, help="Test file") # TODO: better explanation for arguments
    return parser

# TODO: --help to to explain how it works

class HMMTrainer(object):
    def __init__(self, model_name='GaussianHMM', n_components=4, cov_type='diag', n_iter=10000):
        self.model_name = model_name
        self.n_components = n_components
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = []

        if self.model_name == 'GaussianHMM':
            self.model = hmm.GaussianHMM(n_components=self.n_components, 
                    covariance_type=self.cov_type, n_iter=self.n_iter)
        else:
            raise TypeError('Invalid model type')

    def train(self, X):
        np.seterr(all='ignore')
        self.models.append(self.model.fit(X))

    def get_score(self, input_data):
        return self.model.score(input_data)

if __name__=='__main__':
    args = build_arg_parser().parse_args()
    input_folder = args.input_folder
    test_file = args.transcribe

    hmm_models = []

    for dirname in os.listdir(input_folder):
        subfolder = os.path.join(input_folder, dirname)

        if not os.path.isdir(subfolder): 
            continue

        label = subfolder[subfolder.rfind('/') + 1:]

        X = np.array([])
        y_words = []

        for filename in [x for x in os.listdir(subfolder) if x.endswith('.wav')]:
            filepath = os.path.join(subfolder, filename)
            sampling_freq, audio = wavfile.read(filepath)
            
            mfcc_features = mfcc(audio, sampling_freq, winlen=0.025, winstep=0.01, numcep=13, nfilt=26, nfft=1500)

            if len(X) == 0:
                X = mfcc_features
            else:
                X = np.append(X, mfcc_features, axis=0)
            
            y_words.append(label)

        print 'X.shape =', X.shape
        
        hmm_trainer = HMMTrainer()
        hmm_trainer.train(X)
        hmm_models.append((hmm_trainer, label))
        hmm_trainer = None

    test_files = [ test_file ]
    
    for input_file in test_files:
        sampling_freq, audio = wavfile.read(input_file)
        
        mfcc_features = mfcc(audio, sampling_freq, winlen=0.025, winstep=0.01, numcep=13, nfilt=26, nfft=1500)

        max_score = None
        output_label = None

        for item in hmm_models:
            hmm_model, label = item
            score = hmm_model.get_score(mfcc_features)
            if score > max_score:
                max_score = score
                output_label = label
        
        print "\nExpected:", input_file[input_file.find('/')+1:input_file.rfind('/')]
        print "Predicted:", output_label 