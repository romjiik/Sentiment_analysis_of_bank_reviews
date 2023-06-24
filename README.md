# Sentiment_analysis_of_bank_reviews
Course work at the Higher School of Economics on the topic "Sentiment Analysis of Bank Reviews"

# How to run
All the code is in the folder "notebooks_with_code". To run logistic regression, BERT with MLP, BERT plus CNN with MLP or GPT3 with MLP you need to run "Tf-idf plus logreg regression baseline.ipynb", "BERT.ipynb", "BERT_AND_GPT_CNN.ipynb" respectively. Also you need to specify the correct path to the data.

# Where to find data
The data is located in the data folder and is called "final_review_dataset_extended.csv". The code with which the data was obtained is located in the same folder. Also the data is published on [Hugging Face](https://huggingface.co/datasets/Romjiik/Russian_bank_reviews) and on [Kaggle](https://www.kaggle.com/datasets/romanberdyshev/bank-reviews-dataset)

## Dataset Description
### Dataset Summary
The dataset is collected from the banki.ru website. It contains customer reviews of various banks. In total, the dataset contains 12399 reviews. The dataset is suitable for sentiment classification. The dataset contains this fields - bank name, username, review title, review text, review time, number of views, number of comments, review rating set by the user, as well as ratings for special categories

### Languages
Russian

# Perfomance and training
All the metrcis and graphics with training you can find on [wandb](https://wandb.ai/romjiik/course_work?workspace=user-berdyshevrv). Also graphics with training LaBSE-en-ru is located in the images folder.

# Main results of the work
In this term paper, various methods for solving this task were considered, including the use of deep learning models such as BERT and GPT. The experiments included the use of different text preprocessing algorithms and model architectures. The main contribution of the work lies in the collection of a dataset containing reviews about banks, including data from the banki.ru website, and making it publicly available for further use. Additionally, we conducted a comparative analysis of 15 machine learning models, and the results of this amalysis as follows: we identified the most effective models for sentiment analysis of bank reviews, which can be useful for decision-making and improving customer service.
