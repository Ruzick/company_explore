# company_explore
__You can interact directly with the heroku app here:__ https://company-explore.herokuapp.com/ 

## What is this app about?
This app will help you explore keywords found on glassdoor for a company of your choice, and also find out how other companies group depending on those keywords.

<p align="center">
  <img width="600" height="500" src="https://user-images.githubusercontent.com/57594261/108615310-c1fe6a80-73d0-11eb-9e44-7881ad78d7a0.png">
</p>

About the program
I used K-means for the dynamic clustering, dynamic since it changes depending on the keyword box checked.
The current Data Base consists of the first Fortune 200 companies, this number will increase the further I scrape. For details on the scrapers used, please visit link at the 
bottom of this page. For each company the aim was to scrape 2000 reviews, but some companies had less than this ammount, and so data was normalized before performing kmeans.

The app lets you compare cluster averages and this is helpful to see what keyword scores best per cluster.
<p align="center">
  <img width="600" height="500" src="https://user-images.githubusercontent.com/57594261/108615309-c1fe6a80-73d0-11eb-8418-13911c294171.png">
</p>

You can also compare the three most important important keywords if this helps you choose a company.
<p align="center">
  <img width="690" height="390" src="https://user-images.githubusercontent.com/57594261/108615308-c165d400-73d0-11eb-96ba-d66cbba1d5cb.png">
</p>

I wanted this app to be easily transferable to different sets of data so I performed a sentiment analysis for the labeling of positive and negative reviews. 



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
 * Shuffled the data and divided it into training and testing sets
 * Trained the data using Logistic Regression
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
<p align="center">
  <img width="690" height="390" src="https://user-images.githubusercontent.com/57594261/108616230-9af86680-73d9-11eb-973b-838df0c7f3d2.png">
</p>

4. Clustered selected keywords
 * Created a new dabase with company name as first column and the rest of the columns the score for the selected keywords (as oppsoed to all keywords)
 * Reduced data to 2 dimensions using PCA
 * Lopped to find ideal cluster number using range from 2 clusters to 10
   * Used Silhouette Analysis to select best numbers of clusters
 * Performed K-means on the best number of clusters
 * Plotted the data using Altair
<p align="center">
  <img width="690" height="390" src="https://user-images.githubusercontent.com/57594261/108616234-9f248400-73d9-11eb-9a01-127305f90943.png">
</p>

__Exploring Sentiment Analysis__

At first I was tempted to use Vader's pretrained model for the labeling, but because I wanted to se something tailored to review text I decided to train my own.
The training was performed on a very even data set of 1:1 positive to negatove reviews for a total of 6,000 reviews.

<p align="center">
  <img width="910" height="360" src="https://user-images.githubusercontent.com/57594261/108630337-361d2a80-7432-11eb-897a-828b956de744.png">
</p>
Tested the model's accuracy and compared against Vader's. Model gave acurracy of 90%, Vader's of 70% on test set.
For Vader, I set the treshold to -1 for anything lower than or equal to  0, +1 otherwise.
<p align="center">
  <img width="650" height="600" src="https://user-images.githubusercontent.com/57594261/108630341-39b0b180-7432-11eb-9a8c-510814e9f540.png">
</p>


__Exploring the score__

The score is the summation of all the sentiment labels given for that keyword per company text database. The search will look in each of the 2,000 reviews per company and when the keyword is matched it will return the label of +1 or -1. As an example if looking for keyword 'free coffee' and free coffee appears in 7 positive reviews and 5 negative reviews, the summation would give 2. Ideally 2,000 reviews from company are scraped, but some companies may not have that many reviews in glassdoor and so data is normalized per size of sample collected.To make this fraction friendlier to the eye, I multiplied it by 100. A score of 0.04 would translate into 0.04% positive, this is as if we were saying that word appears in 0.04% of the reviews as a positive; we can also have scores of -0.04, meaning this word has the same effect as if it appeared negative on 0.04% of the document. What is 0.04% really, it feels like a low score, how does it compare to other keywords? After doing some simple stats on the average of each keyword per company we find that 0.04% is close to the mean and so it is not too low of a score. 
<p align="center">
  <img src="https://user-images.githubusercontent.com/57594261/108630334-31f10d00-7432-11eb-937f-b6e810c7a7a9.png">
</p>


__Exploring Clustering__

The first step is to determine if we should reduce the dimensionality of the feature space. Because the app is dynamic, I will have no control over how many features the user will choose. I am going to assume the maximum allowed features are selected and optimize based on this selection.

Looking at the Scree plot
<p align="center">
  <img src="https://user-images.githubusercontent.com/57594261/108615892-849cdb80-73d6-11eb-8026-2654a306eca0.png">
</p>


We see three components as a good option, yet two is not a bad option option and easier to visiualize, I chose two components.

For determining the number of clusters, the elbow plot, silhouette and Davies Bouldin were inspected
<p align="center">
  <img src="https://user-images.githubusercontent.com/57594261/108615894-85357200-73d6-11eb-99db-405072bccbc1.png">
</p>


The elbow plot was not enough to determine the number of clusters, it hinted at 3-4, possibly 7. So I explored the silhouette score. The highest silhouette scores
were at 2, 5 and 7 clusters.Finally looking at the Davis Bouldin scores, lowest being at 7 clusters.

![silhouette](https://user-images.githubusercontent.com/57594261/108615895-85357200-73d6-11eb-8252-5bb8d7acc0e2.png)![davies_bouldin](https://user-images.githubusercontent.com/57594261/108615787-887c2e00-73d5-11eb-954f-d30613c497e1.png)





And if we compare the two together:

Score for number of cluster(s) 2: -1255950.727
Silhouette score for number of cluster(s) 2: 0.334
Davies Bouldin score for number of cluster(s) 2: 1.115

Score for number of cluster(s) 3: -988375.702
Silhouette score for number of cluster(s) 3: 0.282
Davies Bouldin score for number of cluster(s) 3: 1.188

Score for number of cluster(s) 4: -828609.385
Silhouette score for number of cluster(s) 4: 0.272
Davies Bouldin score for number of cluster(s) 4: 1.157

Score for number of cluster(s) 5: -746083.488
Silhouette score for number of cluster(s) 5: 0.287
Davies Bouldin score for number of cluster(s) 5: 1.062

Score for number of cluster(s) 6: -669064.051
Silhouette score for number of cluster(s) 6: 0.259
Davies Bouldin score for number of cluster(s) 6: 1.101

Score for number of cluster(s) 7: -597546.287
Silhouette score for number of cluster(s) 7: 0.276
Davies Bouldin score for number of cluster(s) 7: 0.926

Score for number of cluster(s) 8: -579422.799
Silhouette score for number of cluster(s) 8: 0.235
Davies Bouldin score for number of cluster(s) 8: 1.181

We can see that two clusters would probably be optimal. When it came to implementing the program, for simplicity I chose to go for only one analysis, the silhouette score.
The best silhoutte scores where at two clusters.
 

![Silhouete5](https://user-images.githubusercontent.com/57594261/108615306-c165d400-73d0-11eb-94a2-2ff3055dff58.png)
![2clusters](https://user-images.githubusercontent.com/57594261/108615302-c0cd3d80-73d0-11eb-99fd-b092d90ececc.png)




 


See https://github.com/Ruzick/company_explore_data.git for code on: Sentiment Analysis model, data scrappers used, data collected, and to access code on how dabaframe clusters was built.
