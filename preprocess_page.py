import streamlit as st
from hydralit import HydraHeadApp

class AppPreprocessPage(HydraHeadApp):
    def __init__(self) -> None:
        self.text_loadSubData = "We load the dataset, and select the corresponding columns which maybe used in our image."
        self.code_loadSubData = """
def load_dataset():
    df = pd.read_csv("data.csv")
    df = df[pd.notnull(df['longitude']) & pd.notnull(df['latitude'])]
    return df

def load_geo_subset(df):
    geo_df = df[["longitude", "latitude"]]
    geo_df.dropna(inplace=True)
    return geo_df

def load_city_subset(df, city):
    subdf = df[df['city_or_county'] == city].copy()
    subdf = subdf[["longitude", "latitude", "address", "n_killed", "n_injured"]]
    subdf.dropna(inplace=True)
    return subdf
        """
        self.text_exploreColumn = "Before we use the data, we need to find which column need to preprocess, for exmaple fill the missing data. And we also need to see the different data type of all column."
        self.code_exploreColumn = """
def findColumnNeedProcess:
    columns = df.columns
    columns_to_process = df[columns].isnull().any()
    print(df.dtypes.to_dict())
    return columns_to_process
        """
        self.text_parseMapping = "After the first exploration, we find some column type are concated string, whcih means it can be parsed and we need to convert into need data type. Below code show how we parse these map into a new column information."
        self.code_parseMapping = """
def get_user_mapping(txt):
    if txt == "NA":
        return {}
    mapping = {}
    for d in txt.split("||"):
        try:
            key = d.split("::")[0]
            val = d.split("::")[1]
            if key not in mapping:
                mapping[key] = val
        except:
            pass
    return mapping

df['participant_type'] = df['participant_type'].fillna("NA")
df['participant_type_map'] = df['participant_type'].apply(lambda x : get_user_mapping(x))
df['participant_age'] = df['participant_age'].fillna("NA")
df['participant_age_map'] = df['participant_age'].apply(lambda x : get_user_mapping(x))
df['participant_age_group'] = df['participant_age_group'].fillna("NA")
df['participant_age_group_map'] = df['participant_age_group'].apply(lambda x : get_user_mapping(x))
df['participant_gender'] = df['participant_gender'].fillna("NA")
df['participant_gender_map'] = df['participant_gender'].apply(lambda x : get_user_mapping(x))

        """
        self.text_findUniqueType = "Beside the information we get above, we also need to find the enumerate kinds of each column. Only in this, can we find a good way to plot the image."
        self.code_findUniqueType = """
def get_unique_name(df,column_name):
    s = set()
    for item in df[column_name]:
        for k,v in item.items():
            s.add(v)
    print(column_name,s)
def city_list(df):
    return sorted(list(df['city_or_county'].unique()))

get_unique_name(df,'participant_type_map') 
get_unique_name(df,'participant_age_group_map') 
get_unique_name(df,'participant_gender_map') 

        """

    def run(self):
        st.title("The basic preprocess of DataSet")
        st.header("Load data", anchor=None)
        st.write(self.text_loadSubData)
        st.code(self.code_loadSubData, language="python")
        st.header("Explore column", anchor=None)
        st.write(self.text_exploreColumn)
        st.code(self.code_exploreColumn, language="python")
        st.header("Parse map", anchor=None)
        st.write(self.text_parseMapping)
        st.code(self.code_parseMapping, language="python")
        st.header("Find enumerate type", anchor=None)
        st.write(self.text_findUniqueType)
        st.code(self.code_findUniqueType, language="python")


class AppContactPage(HydraHeadApp):
    def __init__(self) -> None:
        pass

    def run(self):
        st.title("Contact")
        st.write("**Tianyi Sun**, tsun2@andrew.cmu.edu")
        st.write("**Yufan Song**, yufans@andrew.cmu.edu")
        st.write("**YunXuan Xiao**, yunxuan2@andrew.cmu.edu")
        st.write("**Zhouyang Li**, zhouyanl@andrew.cmu.edu")


class AppVideoPage(HydraHeadApp):
    def __init__(self) -> None:
        self.url = "https://www.youtube.com/embed/_5XkJC3xuc0?controls=0&showinfo=0&modestbranding=1&wmode=transparent&disablekb=1&rel=0&enablejsapi=1&origin=https%3A%2F%2Fwww.cmu.edu&widgetid=1"

    def run(self):
        st.title("Presentation")
        st.video(self.url)


if __name__ == "__main__":
    contact_app = AppContactPage()
    contact_app.run()
    video_app = AppVideoPage()
    video_app.run()
    prosess_app = AppPreprocessPage()
    prosess_app.run()
