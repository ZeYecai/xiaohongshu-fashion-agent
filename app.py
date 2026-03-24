import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
from collections import Counter
import random

# ---------------------- 页面设置 ----------------------
st.set_page_config(page_title="小红书女装数据分析大屏", layout="wide")
st.title("📊 小红书女装数据分析智能大屏")
st.subheader("爆款分析 · 流行趋势 · 利润款 · 客户痛点")

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------------------- 数据生成（稳定公网版） ----------------------
@st.cache_data(ttl=3600)
def get_data(keyword="女装爆款", pages=2):
    data = []
    styles = ["法式", "韩系", "通勤", "甜妹", "复古", "极简", "辣妹"]
    categories = ["连衣裙", "衬衫", "牛仔裤", "外套", "半身裙", "针织衫", "T恤"]
    fabrics = ["棉", "雪纺", "牛仔", "针织", "西装料"]
    colors = ["黑色", "白色", "杏色", "蓝色", "粉色", "灰色"]

    for page in range(1, pages+1):
        for i in range(20):
            style = random.choice(styles)
            cate = random.choice(categories)
            fabric = random.choice(fabrics)
            color = random.choice(colors)
            data.append({
                "标题": f"{style}{color}{cate}｜显瘦百搭{fabric}面料",
                "风格": style,
                "品类": cate,
                "面料": fabric,
                "色系": color,
                "点赞": random.randint(200, 20000),
                "收藏": random.randint(100, 10000),
                "评论数": random.randint(20, 1000),
                "价格区间": random.choice(["59-99元", "99-199元", "199-399元", "399元以上"]),
                "标签": random.sample(["显瘦", "百搭", "小个子", "梨形身材", "高级感", "通勤", "甜妹"], 3),
                "评论": random.choice([
                    "面料很舒服，就是有点透，需要穿打底",
                    "版型超赞！小个子穿巨显高，显瘦",
                    "质量一般，洗了一次就起球了",
                    "颜色很正，百搭款，推荐购买",
                    "尺码偏大，建议拍小一码",
                    "面料太薄了，夏天穿刚好",
                    "做工精细，性价比很高"
                ])
            })
    df = pd.DataFrame(data)
    return df

# ---------------------- 利润款挖掘 ----------------------
def get_profit(df):
    df["热度"] = df["点赞"] + df["收藏"]*2
    profit = df[(df["价格区间"].isin(["99-199元", "199-399元"])) & (df["热度"] > 5000)]
    profit = profit.sort_values("热度", ascending=False).head(10)
    return profit

# ---------------------- 评论分析 ----------------------
def analyze_comments(df):
    return """
客户痛点：
1. 面料透、薄
2. 起球、质量差
3. 尺码不准
4. 显胖
5. 版型差

客户需求：
1. 显瘦
2. 小个子友好
3. 舒适
4. 百搭
5. 质量好

好评点：
1. 版型好
2. 显瘦
3. 颜色正
4. 面料软
5. 性价比高
"""

# ---------------------- 可视化大屏 ----------------------
def show_dashboard(df):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔥 热门风格")
        style_count = df["风格"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(style_count.index, style_count.values, color="#FF69B4")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader("💰 价格带分布")
        price_count = df["价格区间"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(price_count.values, labels=price_count.index, autopct="%1.1f%%")
        st.pyplot(fig)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("👗 热门品类")
        cate_count = df["品类"].value_counts()
        fig, ax = plt.subplots()
        ax.barh(cate_count.index, cate_count.values, color="#9370DB")
        st.pyplot(fig)

    with col4:
        st.subheader("🎨 流行色系")
        color_count = df["色系"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(color_count.index, color_count.values, color=["#000","#FFF","#F5F5DC","#4169E1","#FFC0CB","#808080"])
        st.pyplot(fig)

    st.subheader("💬 评论词云")
    all_comments = " ".join(df["评论"])
    words = jieba.lcut(all_comments)
    wc = WordCloud(font_path="simhei.ttf", width=800, height=400, background_color="white").generate(" ".join(words))
    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)

    st.subheader("💰 利润款TOP10")
    profit = get_profit(df)
    st.dataframe(profit[["标题","风格","品类","价格区间","点赞","收藏","热度"]], use_container_width=True)

    st.subheader("💡 客户痛点 & 需求")
    st.text(analyze_comments(df))

# ---------------------- 主程序 ----------------------
if __name__ == "__main__":
    keyword = st.text_input("关键词", "女装爆款")
    pages = st.slider("数据页数", 1, 3, 2)

    if st.button("开始分析"):
        with st.spinner("正在生成数据..."):
            df = get_data(keyword, pages)
            st.success(f"✅ 数据生成完成！共 {len(df)} 条")
            show_dashboard(df)

            st.download_button(
                 label="点击下载数据",
    data="你的文件内容",
    file_name="fashion_data.txt",
    mime="text/plain")
df.to_csv(index=False, encoding="utf-8-sig"),
                "女装数据.csv"
