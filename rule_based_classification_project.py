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
###############################################
# ÖDEV 3: ÇÖZÜM.
###############################################


###############################################
# ÖDEV 3: Görev 1: ÇÖZÜM.
###############################################
##Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
##Çözüm: !Genel bilgilere önceden tanımladığımız check_df func ile ulaştık.
df = pd.read_csv("datasets/persona.csv")
check_df(df, head=3, tail=3)
##Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
##Çözüm:2 adet vardır. Toplam frekans sayısı 5000 dir.
# SOURCE değişkeninin sınıfları ve frekansları
df["SOURCE"].value_counts()
# SOURCE değişkeninin sınıfları
##Soru 3: Kaç unique PRICE vardır?
##Çözüm:
df["PRICE"].nunique()
df["PRICE"].unique()
##Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
##Çözüm:
df["PRICE"].value_counts()
df.PRICE.value_counts().sort_index()
##Soru 5: Hangi ülkeden kaçar tane satış olmuş?
##Çözüm:
df["COUNTRY"].value_counts()
##Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
##Çözüm:
df.groupby("COUNTRY")["PRICE"].agg("sum")
##Soru 7: SOURCE türlerine göre göre satış sayıları nedir?
##Çözüm:
df["SOURCE"].value_counts()
##Soru 8: Ülkelere göre PRICE ortalamaları nedir?
##Çözüm:
df.groupby("COUNTRY")["PRICE"].agg("mean")
##Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
##Çözüm:
df.groupby("SOURCE")["PRICE"].agg("mean")
##Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
##Çözüm:
df.groupby(["COUNTRY", "SOURCE"])["PRICE"].agg("mean")

###############################################
# ÖDEV 3: Görev 2: ÇÖZÜM.
###############################################
##COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY", "SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).round(2)

###############################################
# ÖDEV 3: Görev 3: ÇÖZÜM.
###############################################
##Çıktıyı PRICE’a göre sıralayınız.
##Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE’a göre uygulayınız.
##Çıktıyı agg_df olarak kaydediniz.
agg_df = df.groupby(["COUNTRY", "SOURCE","SEX","AGE"])["PRICE"].agg("mean").sort_values(ascending=False)

###############################################
# ÖDEV 3: Görev 4: ÇÖZÜM.
###############################################
##Index’te yer alan isimleri değişken ismine çeviriniz.
##Üçüncü sorunun çıktısında yer alan price dışındaki tüm değişkenler index isimleridir.
##Bu isimleri değişken isimlerine çeviriniz.
agg_df = agg_df.reset_index()

###############################################
# ÖDEV 3: Görev 5: ÇÖZÜM.
###############################################
##age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
##Age sayısal değişkenini kategorik değişkene çeviriniz.
##Aralıkları ikna edici şekilde oluşturunuz.
##Örneğin: ‘0_18', ‘19_23', '24_30', '31_40', '41_70' :)
#1.YOL
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0,18,23,30,40,66], labels =["0_18","19_23","24_30","31_40","41_66"])
#2.YOL
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0,19,24,31,41,70],right=False)
agg_df["AGE_CAT"] = agg_df["AGE_CAT"].apply(lambda x: str(x.left)+"_"+str(x.right-1) if x.right != 70 else str(x.left)+"_"+str(agg_df["AGE"].max()))
###############################################
# ÖDEV 3: Görev 6: ÇÖZÜM.
###############################################
##Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
##ve veri setine değişken olarak ekleyiniz.
##Yeni eklenecek değişkenin adı: customers_level_based
##Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek customers_level_based
##değişkenini oluşturmanız gerekmektedir.
agg_df["customers_level_based"] = [(aggdfcol[0]+"_"+aggdfcol[1]+"_"+ aggdfcol[2]+"_"+aggdfcol[5]).upper() for aggdfcol in agg_df.values]
agg_dff = agg_df[["customers_level_based","PRICE"]].groupby("customers_level_based")["PRICE"].agg("mean").sort_values(ascending=False).reset_index()

###############################################
# ÖDEV 3: Görev 7: ÇÖZÜM.
###############################################
##Yeni müşterileri (personaları) segmentlere ayırınız.
##Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
##Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
##Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).
##C segmentini analiz ediniz (Veri setinden sadece C segmentini çekip analiz ediniz).
agg_dff["SEGMENT"] = pd.qcut(agg_dff["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_dff.groupby("SEGMENT")["PRICE"].agg(["mean", "max", "sum"])

agg_dff.SEGMENT.value_counts()

agg_dff[agg_dff["SEGMENT"]=="C"].describe()   #32.254 ile 34.072 arasında price değerlerine sahip

agg_dff[agg_dff["SEGMENT"]=="C"].sort_values("customers_level_based")

# C segmenti çoğunlukla 19-23 ve 24-30 yaş aralıklarındaki bayanlardan oluşmaktadır.


###############################################
# ÖDEV 3: Görev 8: ÇÖZÜM.
###############################################
## Yeni gelen müşterileri segmentlerine göre sınıflandırınız ve
## ne kadar gelir getirebileceğini tahmin ediniz.
## 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve
## ortalama ne kadar gelir kazandırması beklenir?
## 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne
## kadar gelir kazandırması beklenir?

new_user = "TUR_ANDROID_FEMALE_31_40"
agg_dff[agg_dff["customers_level_based"]==new_user] #A segmentindedir. Ortalama 41.83 gelir kazandırır


new_user = "FRA_IOS_FEMALE_31_40"
agg_dff[agg_dff["customers_level_based"]==new_user]  #C segmentindedir. Ortalama 32.81 gelir kazandırır.



