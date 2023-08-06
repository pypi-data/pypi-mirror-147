import os
from gensim.models import CoherenceModel
from gensim import corpora, models
import gensim
import pickle
import warnings
import pandas as pd
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings("ignore")

def build_lda_models(dict_data,n_topics=10,max_ds_size=-1,alpha='auto',eta='auto',pass_words=20,print_words=10,
                     save=False,save_path="",save_corpus_path="",save_dictionary_path="",save_data_path=""
                     ):

    doc_set = []
    doc_ids = []
    for key in dict_data.keys():
        doc_set.append(dict_data[key].split(","))
        doc_ids.append(str(key))

    # set max data set size
    import random
    if max_ds_size!=-1:
        doc_ids = random.sample(doc_ids, max_ds_size)
        doc_set = [dict_data[id].split(",") for id in doc_ids]


    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(doc_set)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in doc_set]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=n_topics, id2word=dictionary, passes=pass_words,
                                               alpha=alpha, eta=eta)

    # print keywords
    topics = ldamodel.print_topics(num_words=print_words)
    print()
    for topic in topics:
        print(topic)
    print()
    if save:
        ldamodel.save(save_path)
        pickle.dump(corpus,open(save_corpus_path,"wb"))
        pickle.dump(dictionary,open(save_dictionary_path,"wb"))
        pickle.dump(doc_set,open(save_data_path,'wb'))
    return ldamodel

def evaluate_perplexity(lda_model,corpus):
    perplexity=lda_model.log_perplexity(corpus)
    return perplexity

'''
Coherence measure to be used. Fastest method - 'u_mass', 'c_uci' also known as `c_pmi`. 
For 'u_mass' corpus should be provided, if texts is provided, it will be converted to corpus using the dictionary. 
For 'c_v', 'c_uci' and 'c_npmi' `texts` should be provided (`corpus` isn't needed)
'''
def evaluate_coherence_score(ldamodel,texts,dictionary,coherence='c_v'):
    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=ldamodel, texts=texts, dictionary=dictionary, coherence=coherence)
    coherence_lda = coherence_model_lda.get_coherence()
    return coherence_lda

def evaluate_all_metrics_from_lda_model(input_file,output_folder,model_name,num_topics=10,use_metrics="perplexity,c_v,u_mass,c_uci,c_npmi"):

    dict_symptoms = pickle.load(open(input_file, "rb"))
    # build a model and save to disk
    lda_model = build_lda_models(dict_symptoms,
                                 n_topics=num_topics,
                                 save=True,
                                 save_path=f"{output_folder}/{model_name}.gensim",
                                 save_corpus_path=f"{output_folder}/{model_name}.corpus.pickle",
                                 save_dictionary_path=f"{output_folder}/{model_name}.dictionary.pickle",
                                 save_data_path=f"{output_folder}/{model_name}.dataset.pickle",

                                 )
    mlist=use_metrics.split(",")
    # load lda model and other objects
    lda_model_new = gensim.models.ldamodel.LdaModel.load(f"{output_folder}/{model_name}.gensim")
    corpus = pickle.load(open(f"{output_folder}/{model_name}.corpus.pickle", "rb"))
    dictionary = pickle.load(open(f"{output_folder}/{model_name}.dictionary.pickle", "rb"))
    doc_set = pickle.load(open(f"{output_folder}/{model_name}.dataset.pickle", "rb"))
    # measures
    results = {}
    print("no. topics = ",num_topics)
    if 'perplexity' in mlist:
        perplexity = evaluate_perplexity(lda_model, corpus)
        print("perplexity = ", perplexity)
        results['perplexity']=perplexity
    if 'c_v' in mlist:
        c_v = evaluate_coherence_score(lda_model, doc_set, dictionary, coherence='c_v')
        print("c_v = ", c_v)
        results['c_v'] = c_v
    if 'u_mass' in mlist:
        u_mass = evaluate_coherence_score(lda_model, doc_set, dictionary, coherence='u_mass')
        print("u_mass = ", u_mass)
        results['u_mass'] = u_mass
    if 'c_uci' in mlist:
        c_uci = evaluate_coherence_score(lda_model, doc_set, dictionary, coherence='c_uci')
        print("c_uci = ", c_uci)
        results['c_uci'] = c_uci
    if 'c_npmi' in mlist:
        c_npmi = evaluate_coherence_score(lda_model, doc_set, dictionary, coherence='c_npmi')
        print("c_npmi = ", c_npmi)
        results['c_npmi'] = c_npmi
    return results

def explore_topic_model_metrics(input_file,output_folder,model_name,start=2,end=10,use_metrics="perplexity,c_v,u_mass,c_uci,c_npmi"):
    list_results=[]
    result_folder=f"{output_folder}/metrics"
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    for num_topics in range(start,end+1):
        results = evaluate_all_metrics_from_lda_model(input_file=input_file, output_folder=output_folder,
                                                  model_name=model_name, num_topics=num_topics,use_metrics=use_metrics)
        results["num_topics"]=num_topics
        results["model_name"]=model_name
        pickle.dump(results,open(f"{result_folder}/{num_topics}.pickle","wb"))
        list_results.append(results)
    return list_results

def show_topic_model_metric_change(list_result,save=True,save_path=""):
    print()
    fields=["num_topics",'model_name']+"perplexity,c_v,u_mass,c_uci,c_npmi".split(",")
    print("\t".join(fields))
    data=("\t".join(fields)).replace("\t",",")+"\n"
    for result in list_result:
        line=f"{result['num_topics']}\t{result['model_name']}"
        for k in "perplexity,c_v,u_mass,c_uci,c_npmi".split(","):
            line+=f"\t{result[k]}"
        data+=line.replace("\t",",")+"\n"
        print(line)
    if save:
        f_out=open(save_path,"w",encoding='utf-8')
        f_out.write(data)
        f_out.close()
    print()

def test_single():
    # configure
    # load a dictionary with document key and its term list split by ','.
    input_file = "datasets/covid19_symptoms.pickle"
    output_folder = "outputs"
    model_name = "symptom"
    num_topics = 10
    # run
    results = evaluate_all_metrics_from_lda_model(input_file=input_file, output_folder=output_folder,
                                                  model_name=model_name, num_topics=num_topics)
    print(results)

if __name__=="__main__":
    # start configure
    # load a dictionary with document id as key and its term list split by ',' as value.
    input_file = "datasets/covid19_symptoms.pickle"
    output_folder = "outputs"
    model_name = "symptom"
    start=2
    end=20
    # end configure
    # run and explore
    list_results = explore_topic_model_metrics(input_file=input_file, output_folder=output_folder,
                                                  model_name=model_name,start=start,end=end)
    # summarize results
    show_topic_model_metric_change(list_results,save=True,save_path=f"{output_folder}/metrics.csv")
    # plot metric changes





