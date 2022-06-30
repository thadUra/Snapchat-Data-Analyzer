import os
import json
from matplotlib.cbook import simple_linear_interpolation
import pandas
import matplotlib.pyplot as plt

# Getting Snapchat JSON Files
jsonFolder = input("Enter directory where Snapchat data is located: ")
os.chdir(jsonFolder + "/json")

'''
Function returns array of Pandas dataframes of each category given in parameters
'''
def extract( file, category, objects ):
    jsonFile = open(file)
    jsonText = json.load(jsonFile)

    dict = jsonText[category]
    dFrame = pandas.DataFrame.from_dict(dict)
    dFrame = dFrame[objects]
    return dFrame

'''
Function prints out total number of friends, five most recently added friends, and five oldest friends 
within the given data timeframe
'''
def friendStats():
    # friend.json extraction
    cols = ["Username", "Display Name", "Creation Timestamp"]
    categories = ["Friends"]
    dFrame = extract("friends.json", categories[0], cols)
    
    # Parsing dataframe for print
    dFrame.rename(columns = {"Creation Timestamp":"Date Added"}, inplace = True )
    dFrame["Date Added"] = pandas.to_datetime(dFrame["Date Added"], format="%Y-%m-%d %H:%M:%S %Z")
    dFrame.sort_values(by=["Date Added"], inplace=True, ascending=False)
    dFrame["Date Added"] = dFrame["Date Added"].dt.strftime("%m/%d/%Y")
    startDate = dFrame.iloc[-1]['Date Added']
    endDate = dFrame.iloc[0]['Date Added']

    # Printing Results
    print('\033[1m', "Total Number of Friends: ", '\033[0m', dFrame.shape[0], "\n")
    print('\033[1m', "Five Most Recent Friends:\n",'\033[0m', dFrame.head())
    print('\033[1m', "\nFive Oldest Friends:\n",'\033[0m', dFrame.tail(), "\n")
    print('\033[1m', "Date Range for Data Values: ", '\033[0m', startDate, " to ", endDate, "\n")


'''
Function prints out message counts, media type counts, most messages sent to/from a user, 
monthly total of messages, and favorite words sent in chat
'''
def chatStats():
    # chat_history.json extraction
    cols = [["From", "Media Type", "Created", "Text"], ["To", "Media Type", "Created", "Text"]]
    categories = ["Received Saved Chat History", "Sent Saved Chat History", 
                  "Received Unsaved Chat History", "Sent Unsaved Chat History"]
    dFrames = [ extract("chat_history.json", categories[0], cols[0]), 
                extract("chat_history.json", categories[1], cols[1]), 
                extract("chat_history.json", categories[2], cols[0]), 
                extract("chat_history.json", categories[3], cols[1])]
    
    # Parsing dataframes for print
    totalMessages = dFrames[0].shape[0] +  dFrames[1].shape[0] +  dFrames[2].shape[0] +  dFrames[3].shape[0]
    totalReceived = dFrames[0].shape[0] +  dFrames[2].shape[0]
    totalSent = dFrames[1].shape[0] +  dFrames[3].shape[0]

    mediaTypeCount = {}
    sentCountsByUser = {}
    receivedCountsByUser = {}
    wordCounts = {}
    uniqueWordCounts = {}
    commonWords = ["the","of","and","a","to","in","is","you","that","it","he","was","for","on","are","as","with","his",
                   "they","I","i","at","be","this","have","from","or","one","had","by","word","but","not","what","all",
                   "were","we","when","your","can","said","there","use","an","each","which","she","do","how","their",
                   "if","will","up","other","about","out","many","then","them","these","so","some","her","would","make",
                   "like","him","into","time","has","look","two","more","write","go","see","number","no","way","could",
                   "people","my","than","first","water","been","call","who","oil","its","now","find","long","down",
                   "day","did","get","come","made","may","part"]
    iter = 0
    for f in dFrames:
        f["Created"] = pandas.to_datetime(f["Created"], format="%Y-%m-%d %H:%M:%S %Z")
        f["Year"] = pandas.DatetimeIndex(f["Created"]).year
        f["Month"] = pandas.DatetimeIndex(f["Created"]).month
        for index, row in f.iterrows():
            if iter % 2 == 0:
                user = row["From"]
                receivedCountsByUser[user] = receivedCountsByUser.get(user, 0) + 1
            else:
                user = row["To"]
                sentCountsByUser[user] = sentCountsByUser.get(user, 0) + 1
                msg = str(row["Text"])
                msg = msg.split()
                for word in msg:
                    wordCounts[word] = wordCounts.get(word, 0) + 1
                    if word not in commonWords:
                        uniqueWordCounts[word] = uniqueWordCounts.get(word, 0) + 1
            media = row["Media Type"]
            mediaTypeCount[media] = mediaTypeCount.get(media, 0) + 1
        iter += 1
    
    # Sorting for print
    receivedCountsByUserDF = pandas.DataFrame(list(receivedCountsByUser.items()), columns=['Username', 'Messages Received'])
    receivedCountsByUserDF.sort_values(by=["Messages Received"], inplace=True, ascending=False)
    sentCountsByUserDF = pandas.DataFrame(list(sentCountsByUser.items()), columns=['Username', 'Messages Sent'])
    sentCountsByUserDF.sort_values(by=["Messages Sent"], inplace=True, ascending=False)
    favoriteWords = pandas.DataFrame(list(wordCounts.items()), columns=['Word', 'Count'])
    favoriteWords.sort_values(by=["Count"], inplace=True, ascending=False)
    uniqueFavoriteWords = pandas.DataFrame(list(uniqueWordCounts.items()), columns=['Word', 'Count'])
    uniqueFavoriteWords.sort_values(by=["Count"], inplace=True, ascending=False)
    
    monthlyReceivedDF = pandas.concat([dFrames[0], dFrames[2]])
    monthlyReceivedDF = monthlyReceivedDF["Month"].value_counts().rename_axis("Month").reset_index(name="Count")
    monthlyReceivedDF.sort_values(by=["Month"], inplace=True, ascending=True)
    monthlySentDF = pandas.concat([dFrames[1], dFrames[3]])
    monthlySentDF = monthlySentDF["Month"].value_counts().rename_axis("Month").reset_index(name="Count")
    monthlySentDF.sort_values(by=["Month"], inplace=True, ascending=True)

    # Printing Results
    print('\033[1m', "Total Number of Messages Sent: ", '\033[0m', totalSent, "\n")
    print('\033[1m', "Total Number of Messages Received: ", '\033[0m', totalReceived, "\n")
    print('\033[1m', "Total: ", '\033[0m', totalMessages, "\n")
    print('\033[1m', "Top Five Users Messages Sent To: \n",'\033[0m', sentCountsByUserDF.head())
    print('\033[1m', "\nTop Five Users Messages Received From: \n",'\033[0m', receivedCountsByUserDF.head())
    print('\033[1m', "\nFive Favorite Words to Send: \n",'\033[0m', favoriteWords.head())
    print('\033[1m', "\nFive Unique Favorite Words to Send (Excludes 100 Most Common English Words): \n",'\033[0m', uniqueFavoriteWords.head(), "\n")

    # Plotting messages
    index = ["January","February","March","April","May","June","July",
            "August","September","October","November","December"]
    graph = pandas.DataFrame({"Sent": monthlySentDF["Count"].values.tolist(), "Received": monthlyReceivedDF["Count"].values.tolist()}, index=index)
    plot = graph.plot.bar(rot=0)
    plt.show()
    

'''
Function prints out most / least stories viewed and total number of stories viewed within the given data timeframe
'''
def storyStats():
    # story_history.json extraction
    cols = ["View", "Media Type", "View Date"]
    categories = ["Friend and Public Story Views"]
    dFrame = extract("story_history.json", categories[0], cols)

    # Parsing dataframes for print
    dFrame["View Date"] = pandas.to_datetime(dFrame["View Date"], format="%Y-%m-%d %H:%M:%S %Z")
    dFrame.sort_values(by=["View Date"], inplace=True, ascending=False)
    dFrame["View Date"] = dFrame["View Date"].dt.strftime("%m/%d/%Y")
    startDate = dFrame.iloc[-1]['View Date']
    endDate = dFrame.iloc[0]['View Date']

    storyViews = {}
    totalStories = 0
    for index, row in dFrame.iterrows():
        if row["Media Type"] == "STORY" or row["Media Type"] == "VIDEO":
            key = row["View"]
            storyViews[key] = storyViews.get(key, 0) + 1
            totalStories += 1
    dFrame = pandas.DataFrame(list(storyViews.items()), columns=['Username', 'Views'])
    dFrame.sort_values(by=["Views"], inplace=True, ascending=False)

    # Printing Results
    print('\033[1m', "Total Number of User Stories Viewed: ", '\033[0m', totalStories, "\n")
    print('\033[1m', "Five Most Viewed User Stories:\n",'\033[0m', dFrame.head())
    print('\033[1m', "\nFive Least Viewed User Stories:\n",'\033[0m', dFrame.tail(), "\n")
    print('\033[1m', "Date Range for Data Values: ", '\033[0m', startDate, " to ", endDate, "\n")


'''
Function prints out breakdown of time spent on app and creates pie chart of values
TODO: Rework pie chart to donut chart using plotly
'''
def timeStats():
    # user_profile.json extraction 
    # cannot use extract function with different file structure
    jsonFile = open("user_profile.json")
    jsonText = json.load(jsonFile)
    jsonString = jsonText["Breakdown of Time Spent on App"]
    categories = []
    percentSpent = []

    # Printing time breakdown values while storing into dataframe
    print('\033[1m', "Breakdown of Time Spent on App:", '\033[0m')
    for i in jsonString:
        print("  ", i)
        temp = i.split(": ", 1)
        categories.append(temp[0])
        percentSpent.append(float(temp[1].strip('%')))
    
    # Displaying pie chart of time breakdown
    dFrame = pandas.DataFrame({'percentages': percentSpent}, index=categories)
    plot = dFrame.plot.pie(y='percentages', figsize=(5,5))
    plt.show()

# Main loop for analyzer
userInput = ''
while userInput != '0':
    print("=======================================================================\n") # Divider

    # Choices for which data to print and provide information for
    print("[1] View Snapchat friend statistics")                     # friends.json
    print("[2] View chat message statistics")                          # chat_history.json
    print("[3] View story history statistics")                         # story_history.json
    print("[4] View time breakdown of time spent on Snapchat")         # user_profile.json
    print("[0] Exit the Snapchat Analyzer Program")                    # Exit program
    userInput = input("\n\nWhat statistic would you like to see: ")    # Input

    print("\n=======================================================================\n") # Divider

    if userInput == '1':
        friendStats()
    elif userInput == '2':
        chatStats()
    elif userInput == '3':
        storyStats()
    elif userInput == '4':
        timeStats()
    elif userInput == '0':
        print("Exiting program now...\n")
    else:
        print("Sorry, you could you provide a valid choice.\n")