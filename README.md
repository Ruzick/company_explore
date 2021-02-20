# company_explore
__You may interact directly with the heroku app here:__ https://company-explore.herokuapp.com/ 

## What is this app about?
This app will help you explore keywords found on glassdoor for a company of your choice, and also explore how other companies group depending on those keywords.
I used K-means for the dynamic clustering, dynamic since it changes depending on the keyword box checked.
The current Data Base consists of the first Fortune 200 companies, this number will increase the further I scrape. For details on the scrapers used, please visit link at the 
bottom of this page. For each company the aim was to scrape 2000 reviews, but some companies had less than this ammount, and so data was normalized before performing kmeans.

__Methods__


1. Trained Data using Sentiment Analysis in order to label future text
 * Used 3,000 positive reviews and 3,000 negative reviews to train the data
 * For the positive reviews used the Pros section of the review, for the negative reviews used the Cons section of the review
 * Conditioned the data in the following fashion:
   * Made the type of text string
   * Coverted to lowercase
   * Removed punctuation
   * Remove stop words
   * Performed stemming
 * Labeled the data as +1 for positive reviews (Pros section) and -1 for negative reviews (Cons section)
 * Divided data into training and testing sets
 * Trained the data using Logistic Regression
 * Tested the model's accuracy and compared against Vader's. Model gave acurracy of 90%, Vader's of 70% on test set
2. Created the data base
 * Appended all individual company reviews into one Data Base and filtered company review's Pros and Cons
 * Concatenated Pros and Cons
 * Conditioned the data in the same fashion as described above
 * Labeled them using the predict method for our model
 * Builded a new database using the company name as the first column and created a separate column for each keyword desired
   * This includes searching for that keyword in the database created earlier, and adding to it a number that represents the addition of all +1 and -1 labels for that keyword.
   * Normalized this number by dividing by the sample size collected for that company (some company's had less than 2,000 reviews)
   * Multiplied by 100 in order to have a percentage score, easier for the eyes
3. Clustered all keywords
 * With the data base ready, used it to cluster all companies with respect to all keywords
 * Reduced data to 2 dimensions using PCA
 * Lopped to find ideal cluster number using range from 2 clusters to 10
   * Used Silhouette Analysis to select best numbers of clusters
 * Performed K-means on the best number of clusters
 * Plotted the data using Altair
4. Clustered selected keywords
 * Created a new dabase with company name as first column and the rest of the columns the score for the selected keywords (as oppsoed to all keywords)
 * Reduced data to 2 dimensions using PCA
 * Lopped to find ideal cluster number using range from 2 clusters to 10
   * Used Silhouette Analysis to select best numbers of clusters
 * Performed K-means on the best number of clusters
 * Plotted the data using Altair



 


See https://github.com/Ruzick/company_explore_data.git for code on: Sentiment Analysis model, data scrappers used, data collected, and to access code on how dabaframe clusters was built.
