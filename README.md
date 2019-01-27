An extension to Visitpedia: Wiki Article Log Visualization

Summary:

In this project I implemented and extended a data visualization research paper called Visitpedia. Visitpedia is an interactive visual analytics tool which enables users to analyze events and understand evolution patterns of real-world events. This process of exploratory data analysis is under the user’s control and as the data is based on the visit counts of users, this process of event detection is unbiased and reliable.

The workflow of the tool consists of data pre-processing, entry-event detection, critical event extraction and finally event analysis. The system was extended by scaling the data. A time-series chart and a word cloud were also added to give an overview of the changes in the number of events over the years. 

For the dataset, I scraped the Topviews Analysis webpage to retrieve the daily page views. Web scraping tools like Selenium and BeautifulSoup in Python were used.

After the extraction of page counts, I applied the CUSUM algorithm to detect entry events. To detect events as soon as they start, a fast-initial response time wass added. An Upper Control Limit was added to only consider important events.

All the graphs were implemented from scratch using D3.js.
