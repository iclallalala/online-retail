import pandas as pd
import matplotlib.pyplot as plt
import time

start = time.process_time()
df = pd.read_excel("online_retail2.xlsx")
df["WeekDay"]=df["InvoiceDate"].dt.weekday
df.dropna(inplace=True)
df.loc[df["WeekDay"] == 0, "WeekDay"]="Monday"
df.loc[df["WeekDay"] == 1, "WeekDay"]="Tuesday"
df.loc[df["WeekDay"] == 2, "WeekDay"]="Wednesday"
df.loc[df["WeekDay"] == 3, "WeekDay"]="Thursday"
df.loc[df["WeekDay"] == 4, "WeekDay"]="Friday"
df.loc[df["WeekDay"] == 5, "WeekDay"]="Saturday"
df.loc[df["WeekDay"] == 6, "WeekDay"]="Sunday"
df["Money"]=df["Quantity"]*df["Price"]

df["Date"] = df["InvoiceDate"].dt.date

def Top10Products():
    df2=df[["Description","Quantity"]]
    df2=df2.groupby(["Description"]).sum().reset_index()
    df2=df2.sort_values("Quantity",ascending=False).head(10)
    print("1)Top 10 products ordered by individuals:")
    print(df2)

def Top10CustomersWhoSpentMostMoney():

    CustomersSpendings = pd.DataFrame(df["Price"]*df["Quantity"],columns = ["TotalSpending"])
    CustomersSpendings["Customer ID"] =df["Customer ID"]
    Listof = pd.DataFrame(CustomersSpendings.groupby("Customer ID").sum())
    Sorted = Listof.sort_values("TotalSpending",ascending = False)
    RESULT = Sorted.head(n=10)
    print("Here is the list of Top 10 customers who spent the most money : ")
    print(RESULT)

def Top5Dates():
    DateGroup = df.groupby(["Date"])
    List =pd.DataFrame(DateGroup.nunique())
    sortedlist = List["Invoice"].sort_values(ascending = False)
    top5 = sortedlist.head(5)
    print("3) Top 5 dates in which the greatest number of orders were placed: ")
    print(top5)

def AverageNumbersOfOrdersEachDay():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"]
    print("4) Average Numbers Of Orders Each Day: ")
    for i in days:
        df5 = df[["WeekDay", "Invoice", "Date"]]
        df5 = df5.drop_duplicates("Invoice")
        df5 = df5.loc[df5["WeekDay"] == i]
        df5 = df5.groupby("Date").count()
        df5 = df5.reset_index()
        df5["WeekDay"] = pd.to_datetime(df5["Date"]).dt.weekday
        df5 = df5.groupby("WeekDay").mean().reset_index()
        df5 = df5["Invoice"]
        print("Average number of orders placed on", i, ":", int(df5))
def MostOrderedProductForSpecificDay():
    while True:
        year = int(input("Please enter year: "))
        if year < 2010 or year > 2011:
            print("Please enter 2010 or 2011")
            continue
        break

    while True:
        month = int(input("Please enter month: "))
        if month < 1 or month > 12:
            print("Enter a number between [1,12]")
            continue
        break
    while True:
        day = int(input("Please enter day: "))
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            if day < 0 or day > 31:
                print("Enter a number between [1,31]")
                continue
            break
        elif month == 2:
            if day < 0 or day > 28:
                print("Enter a number between [1,28]")
                continue
            break
        else:
            if day < 0 or day > 30:
                print("Enter a number between [1,30]")
                continue
            break

    date1 = pd.to_datetime(str(year) + "-" + str(month) + "-" + str(day))

    df1 = df[["Date", "Description", "Quantity"]]
    df1 = df1.loc[df1["Date"] ==date1]
    df1 = df1.groupby("Description").sum()
    df1 = df1.sort_values("Quantity", ascending=False).head(1)
    print("5)Most ordered product for", date1, "is:", df1)




Top10Products()
Top10CustomersWhoSpentMostMoney()
Top5Dates()
AverageNumbersOfOrdersEachDay()

MostOrderedProductForSpecificDay()
def visualizeProduct():

    vis3 = df[["Description","Quantity"]]
    vis3.groupby("Description").sum().sort_values("Quantity",ascending=False).head(n=10).plot(kind="bar",figsize=(10,3),color="r")
    plt.title("Product-Quantity Diagram")
    plt.xlabel("Products")
    plt.ylabel("Quantity")
def visualizeInvoiceDate():

    df["Money"]=df["Price"]*df["Quantity"]
    vis4 = df[["InvoiceDate", "Money"]]
    vis4.groupby("InvoiceDate").sum().sort_values("Money", ascending=False).head(10).plot(kind="bar",figsize=(18, 10))
    plt.title("Spent Money - InvoiceDate Diagram")
    plt.xlabel("InvoiceDate")
    plt.ylabel("Spent Money")
    plt.show()
def visualizeCountry():

    vis1 = df[["Country", "Invoice"]]
    vis1.drop_duplicates("Invoice")
    vis1.groupby("Country").count().sort_values("Invoice", ascending=False).head(10).plot(figsize=(15, 5))
    plt.title("Order-Country Diagram")
    plt.xlabel("Countries")
    plt.ylabel("Number of Orders")
    plt.show()
def visualizeCustomer():

    vis2 = df[["Customer ID", "Country"]]
    vis2dup = vis2.drop_duplicates("Customer ID")
    vis2dup["Country"].value_counts().head(10).plot(kind="bar",figsize=(14, 6), color="k")
    plt.title("Customer - Country Diagram")
    plt.xlabel("Country")
    plt.ylabel("Customer")
    plt.show()



visualizeCountry()
visualizeCustomer()
visualizeProduct()
visualizeInvoiceDate()
