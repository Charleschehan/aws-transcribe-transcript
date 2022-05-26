#!/usr/bin/env python3
def main():
 import json
    import datetime
    import codecs
    #import nltk
    #import spacy
    import csv
    #nlp = spacy.load("en_core_web_trf")

    """
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('vader_lexicon')
    """
    #from nltk.sentiment.vader import SentimentIntensityAnalyzer
    #from nltk.corpus import stopwords
    #from nltk.tokenize import word_tokenize
    #sid = SentimentIntensityAnalyzer()

    filenames = ('L:\Test.json', 'L:\\fullfile.json')
    #print("Filename: ", filename)
	
    #with codecs.open(filename+'.txt', 'w', 'utf-8') as w:
    with open('L:\\fulltest.csv', 'w', newline='', encoding='utf-8') as w:
        writer = csv.writer(w)
        header = ['time','speaker','content']
        writer.writerow(header)
	
        for filename in filenames:
            with codecs.open(filename, 'r', 'utf-8') as f:
                data = json.loads(f.read())
                labels = data['results']['speaker_labels']['segments']
                speaker_start_times = {}
                for label in labels:
                    for item in label['items']:
                        speaker_start_times[item['start_time']] = item['speaker_label']
                        items = data['results']['items']
                        lines = []
                        line = ''
                        time = 0
                        speaker = 'New recording'
                        i = 0
                for item in items:
                    i = i+1
                    content = item['alternatives'][0]['content']
                    if item.get('start_time'):
                        current_speaker = speaker_start_times[item['start_time']]
                    elif item['type'] == 'punctuation':
                        line = line+content

                    if current_speaker != speaker :
                        if speaker:
                            lines.append(
                                {'speaker': speaker, 'line': line, 'time': time})
                        line = content
                        speaker = current_speaker
                        time = item['start_time']
                    elif item['type'] != 'punctuation':
                        line = line + ' ' + content

                    print (line)
                    print (i)
                        
                lines.append({'speaker': speaker, 'line': line, 'time': time})
                sorted_lines = sorted(lines, key=lambda k: float(k['time']))
                for line_data in sorted_lines:
                
                    #text_tokens = word_tokenize(line_data.get('line'))
                    #tokens_without_sw = [word for word in text_tokens if word.isalpha() and not word in stopwords.words()]
                    
                    #doc=nlp(line_data.get('line'))
                    #exclude_sub = ['I','that']
                    #sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj")]           
                    
                    line = [
                        str(datetime.timedelta(seconds=int(round(float(line_data['time']))))),  
                        str(line_data.get('speaker')), 
                        #len(text_tokens), 
                        #len(tokens_without_sw), 
                        #str(sub_toks), 
                        str(datetime.timedelta(seconds=int(round(float(line_data['time']))))) + ' ' +str(line_data.get('line'))
                        ]
                    writer.writerow(line)
                    """
                    score = sid.polarity_scores(line_data.get('line'))
                    w.write(str(score) + '\n')
                    
                    text_tokens = word_tokenize(line_data.get('line'))
                    tokens_without_sw = [word for word in text_tokens if word.isalpha() and not word in stopwords.words()]
                    w.write(str(tokens_without_sw) + '\n')
                           
                    doc=nlp(line_data.get('line'))
    
                    sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
    
                    w.write(str(sub_toks) + '\n') 
                    """    

if __name__ == '__main__':
	main()
