#%% [markdown]
# # Jieba斷句
# 將爬蟲結果用Jieba進行拆字、斷句，並接結果分別存成txt檔
# [Jieba斷句結果](./dictionary/data)

#%%
import pandas as pd
import pickle
import jieba
import jieba.analyse

#%%
# Define a function to load scraped data
def load_data(filename):
    with open("./crawler/data/tech_orange_" + filename + ".pkl", "rb") as handle:
        data = pickle.load(handle)

    # Reverse data
    data = data[::-1]
    data = pd.DataFrame(data)
    return(data)

#%%
# Define a function to cut word and save results as txt files
def cut_word(filename):
    f = open("./dictionary/data/" + filename + "_seg.txt", "w+", encoding="utf-8")
    data = load_data(filename)
    all_news_content = data["content"].values.tolist()
    one_news_result = []
    for one_news_content in all_news_content:
        one_news_result[:] = []
        seg_list = jieba.cut(one_news_content, cut_all=False)
        for seg in seg_list:
            seg = ''.join(seg.split())
            if (seg != '' and seg != "\n" and seg != "\n\n"):
                one_news_result.append(seg)
        f.write(' '.join(one_news_result))
        f.write("\n")
    f.close()

#%%
# Execute Jieba cut word
for industry in ["ecommerce", "blockchain", "finance", "marketing", "travel"]:
    cut_word(industry)