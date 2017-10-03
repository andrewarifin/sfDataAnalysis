# San Francisco Municipal Building Energy Usage Analysis

### https://sf-eui-analysis.herokuapp.com/

## Synopsis
The data set I am analyzing is the 2013 energy performance of over 470 San Francisco public buildings. In particular, I am examining EUI, or Energy Use Intensity. EUI is calculated by dividing the total energy the building consumed by the building in the span of one year and divided by the total gross floor area of the building. I analyzed the EUI of buildings categorically, and within each category, I grouped bulidings by their facility type and the decade they were built/renovated.

## Challenges
Having very little, if any, data analytics/visualization experience, this project was very overwhelming at first. Luckily, my older brother Kevin was a huge help in getting me started. Be sure to check out his Github: https://github.com/kevarifin14! He helped me understand what exactly Jupyter Notebook was as well some initial brainstorming. 

### Jupyter Notebook
The initial overhead of learning how to use Jupyter Notebook was tough, from the concepts of dataframes and series to visualizing data into tables and graphs. It took me hours just to generate simple tables and graphs. With extensive Googling and trial and error, I was finally able to create my first Jupyter Notebook 😊

As seen at the end of my notebook, I attempted to do a linear regressional analysis of my data, first with by category and second by build year/renovated. Unfortunately, it did not turn out very well with a stunning r-squared value of 0.012. However, it was cool to see how easy it is to do regressional analysis. I believe that this data set itself just didn't have very much correlation between any of its columns

### Dash
Dash was a whole other beast to tackle. Since I have had lots of experience using React in the past, I highly considered using it to implement my frontend. However, after looking into Dash, I realized how quick and simple it was to implement. Huge shoutout to Plotly for creating such an amazing library! Despite having 0 experience in Dash, I chose it over React because of how easy it was to pick up. After crash coursing several tutorials it was time to get started on my front end.

One of the biggest issues I had with Dash was formatting. Due to my inexperience, I had many callbacks linked to the same input. Also, I was modifying the formatting through callbacks which I now realize is not the best practice. This was an extremely hacky and I refactored my implementation to make it much more modular and solved the formating issues.

## Next Steps
* Mobile support - The UI does not look good on mobile
* Deeper analysis - With a stronger knowledge of data analytics/machine learning, I would want to be able to predict a building's EUI based of its building category, facility type, and build year.

## Conclusion
Overall, I thoroughly enjoyed this side project. It was a great introduction to data analysis as well as Jupyter Notebooks and Dash. I loved transforming a simple .csv into a beautiful web app and will definitely continue to explore more aspects of data analytics.
