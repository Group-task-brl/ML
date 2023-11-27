from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df.user == selected_user]
    # 1. fetch no. of messages
    num_messages = df.shape[0]
    words = []
    links = []
    for message in df.message:
        # 2. no. of words
        words.extend(message.split())
        # 4. fetch no. of links shared
        links.extend(extract.find_urls(message))
    # 3. fetch no. of media messages
    num_media_messages = df[df.message == '<Media omitted>\n'].shape[0]
    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    return df.user.value_counts().head(), round((df.user.value_counts() / df.shape[0])*100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})


def create_wordcloud(selected_user, df):
    f = open('../Stop Words/stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    f.close()
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('../Stop Words/stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in temp.message:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    f.close()
    return pd.DataFrame(Counter(words).most_common(20))


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df.user == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline_df = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline_df


def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
