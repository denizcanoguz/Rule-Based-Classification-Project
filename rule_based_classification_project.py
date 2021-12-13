import pandas as pd
def check_df(dataframe, head=5, tail=5, quan=False):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(tail))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())

    if quan:
        print("##################### Quantiles #####################")
        print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


#TASK:1
        
# persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz. !Genel bilgilere önceden tanımladığımız check_df func ile ulaştık.
df = pd.read_csv("datasets/persona.csv")
check_df(df, head=3, tail=3)

# Kaç unique SOURCE vardır ve Frekansları nedir?
df["SOURCE"].value_counts()

# Kaç unique PRICE vardır?
df["PRICE"].nunique()
df["PRICE"].unique()

# Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()
df.PRICE.value_counts().sort_index()

#Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()

# Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY")["PRICE"].agg("sum")

# SOURCE türlerine göre göre satış sayıları nedir?
df["SOURCE"].value_counts()

# Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY")["PRICE"].agg("mean")

# SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE")["PRICE"].agg("mean")

# COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY", "SOURCE"])["PRICE"].agg("mean")


#TASK:2

# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY", "SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).round(2)

#TASK:3

# Çıktıyı PRICE’a göre sıralayınız.Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE’a göre uygulayınız. Çıktıyı agg_df olarak kaydediniz.
agg_df = df.groupby(["COUNTRY", "SOURCE","SEX","AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE",ascending=False)

#TASK:4

# Index’te yer alan isimleri değişken ismine çeviriniz. Üçüncü sorunun çıktısında yer alan price dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.
agg_df = agg_df.reset_index()

#TASK:5

# age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.

#1.YOL
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0,18,23,30,40,66], labels =["0_18","19_23","24_30","31_40","41_66"])
#2.YOL
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0,19,24,31,41,70],right=False)
agg_df["AGE_CAT"] = agg_df["AGE_CAT"].apply(lambda x: str(x.left)+"_"+str(x.right-1) if x.right != 70 else str(x.left)+"_"+str(agg_df["AGE"].max()))

#TASK:6

# Yeni seviye tabanlı müşterileri (persona) tanımlayınız ve veri setine değişken olarak ekleyiniz. Yeni eklenecek değişkenin adı: customers_level_based
# Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek customers_level_based değişkenini oluşturmanız gerekmektedir.
agg_df["customers_level_based"] = [(aggdfcol[0]+"_"+aggdfcol[1]+"_"+ aggdfcol[2]+"_"+aggdfcol[5]).upper() for aggdfcol in agg_df.values]
agg_dff = agg_df[["customers_level_based","PRICE"]].groupby("customers_level_based")["PRICE"].agg("mean").sort_values(ascending=False).reset_index()

#TASK:7

# Yeni müşterileri (personaları) segmentlere ayırınız. Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
# Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz. Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).
# C segmentini analiz ediniz (Veri setinden sadece C segmentini çekip analiz ediniz).
agg_dff["SEGMENT"] = pd.qcut(agg_dff["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_dff.groupby("SEGMENT")["PRICE"].agg(["mean", "max", "sum"])
agg_dff.SEGMENT.value_counts()
agg_dff[agg_dff["SEGMENT"]=="C"].describe()   #32.254 ile 34.072 arasında price değerlerine sahip
agg_dff[agg_dff["SEGMENT"]=="C"].sort_values("customers_level_based")
# C segmenti çoğunlukla 19-23 ve 24-30 yaş aralıklarındaki bayanlardan oluşmaktadır.


#TASK:8

# Yeni gelen müşterileri segmentlerine göre sınıflandırınız ve ne kadar gelir getirebileceğini tahmin ediniz.

# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_dff[agg_dff["customers_level_based"]==new_user] #A segmentindedir. Ortalama 41.83 gelir kazandırır

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "FRA_IOS_FEMALE_31_40"
agg_dff[agg_dff["customers_level_based"]==new_user]  #C segmentindedir. Ortalama 32.81 gelir kazandırır.



