import re
from collections import defaultdict


# ==========================================================
# CONFIGURATION
# ==========================================================

MIN_CONFIDENCE = 45


# ==========================================================
# NORMALIZATION
# ==========================================================

def normalize(text):
    """
    Convert a column name into a comparable format.
    """

    if text is None:
        return ""

    text = str(text).lower()

    text = text.replace("_", " ")
    text = text.replace("-", " ")

    text = re.sub(r"[^a-z0-9 ]", "", text)

    text = " ".join(text.split())

    return text


# ==========================================================
# SCORE HELPERS
# ==========================================================

def exact_match(column, keyword):

    return normalize(column) == normalize(keyword)


def contains_match(column, keyword):

    return normalize(keyword) in normalize(column)


def word_overlap(column, keyword):

    c = set(normalize(column).split())

    k = set(normalize(keyword).split())

    return len(c & k)


# ==========================================================
# COLUMN SCORER
# ==========================================================

def score_column(column, keywords):

    score = 0

    for keyword in keywords:

        if exact_match(column, keyword):

            score += 100

        elif contains_match(column, keyword):

            score += 60

        else:

            score += word_overlap(column, keyword) * 20

    return score


# ==========================================================
# FIND BEST COLUMN
# ==========================================================

def find_best_column(columns, keywords):

    best_column = None

    best_score = -1

    scores = {}

    for column in columns:

        current = score_column(column, keywords)

        scores[column] = current

        if current > best_score:

            best_score = current

            best_column = column

    if best_score < MIN_CONFIDENCE:

        return None, scores

    return best_column, scores

# ==========================================================
# BUSINESS CONCEPT LIBRARY
# ==========================================================

BUSINESS_CONCEPTS = {

    "pickup_location": [

    "pickup location",
    "pickup_location",
    "pickup"
],


"drop_location": [

    "drop location",
    "drop_location",
    "drop"
],


"customer_rating": [

    "customer rating",
    "customer_rating",
    "customer ratings"
],


"driver_rating": [

    "driver rating",
    "driver_rating",
    "driver ratings"
],

    # ------------------------------------------------------
    # DATE
    # ------------------------------------------------------

    "date": [

        "date",
        "order date",
        "booking date",
        "transaction date",
        "invoice date",
        "purchase date",
        "training date",
        "survey date",
        "start date",
        "joining date",
        "hire date",
        "created date",
        "created",
        "timestamp",
        "time",
        "datetime",
        "month",
        "year",
        "day",
        "step"

    ],

    # ------------------------------------------------------
    # CUSTOMER
    # ------------------------------------------------------

    "customer": [

        "customer",
        "customer id",
        "customerid",
        "customer name",
        "client",
        "client id",
        "user",
        "user id",
        "userid",
        "buyer"

    ],

    # ------------------------------------------------------
    # PRODUCT
    # ------------------------------------------------------

    "product": [

        "product",
        "product id",
        "product name",
        "productname",
        "item",
        "item name",
        "sku",
        "model",
        "model name"

    ],

    # ------------------------------------------------------
    # CATEGORY
    # ------------------------------------------------------

    "category": [

        "category",
        "subcategory",
        "segment",
        "department category",
        "product category"

    ],

    # ------------------------------------------------------
    # REGION
    # ------------------------------------------------------

    "region": [

        "region",
        "country",
        "state",
        "city",
        "location",
        "shipping address",

    ],

    # ------------------------------------------------------
    # QUANTITY
    # ------------------------------------------------------

    "quantity": [

        "quantity",
        "qty",
        "units",
        "unit sold",
        "items",
        "itemsincart",
        "order quantity"

    ],

    # ------------------------------------------------------
    # PRICE
    # ------------------------------------------------------

    "price": [

        "price",
        "unit price",
        "unitprice",
        "product price",
        "productprice",
        "training cost",
        "cost",
        "expense",
        "fuel price"

    ],

    # ------------------------------------------------------
    # REVENUE
    # ------------------------------------------------------

    "revenue": [

        "revenue",
        "sales",
        "sales amount",
        "salesamount",
        "weekly sales",
        "weekly_sales",
        "booking value",
        "total price",
        "totalprice",
        "invoice amount",
        "total amount",
        "turnover",
        "income"

    ],

    # ------------------------------------------------------
    # AMOUNT
    # ------------------------------------------------------

    "amount": [

        "amount",
        "transaction amount",
        "transaction value",
        "value",
        "balance amount"

    ],

    # ------------------------------------------------------
    # EMPLOYEE
    # ------------------------------------------------------

    "employee": [

        "employee",
        "employee id",
        "employeeid",
        "emp id",
        "empid",
        "associate"

    ],

    # ------------------------------------------------------
    # DEPARTMENT
    # ------------------------------------------------------

    "department": [

        "department",
        "department type",
        "departmenttype",
        "division"

    ],

    # ------------------------------------------------------
    # SALARY
    # ------------------------------------------------------

    "salary": [

        "salary",
        "pay",
        "payzone",
        "monthly income"

    ],

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    "status": [

        "status",
        "booking status",
        "employee status",
        "order status",
        "condition"

    ],

    # ------------------------------------------------------
    # FRAUD
    # ------------------------------------------------------

    "fraud": [

        "fraud",
        "isfraud",
        "fraudulent",
        "fraud flag"

    ],

    # ------------------------------------------------------
    # TRANSACTION
    # ------------------------------------------------------

    "transaction": [

        "transaction",
        "transaction type",
        "type",
        "payment",
        "payment method"

    ],

    # ------------------------------------------------------
    # SATISFACTION
    # ------------------------------------------------------

    "satisfaction": [

        "satisfaction",
        "satisfaction score",
        "employeesatisfaction"

    ],

    # ------------------------------------------------------
    # ENGAGEMENT
    # ------------------------------------------------------

    "engagement": [

        "engagement",
        "engagement score",
        "employee engagement"

    ],

    # ------------------------------------------------------
    # WORK LIFE BALANCE
    # ------------------------------------------------------

    "worklife": [

        "work life balance",
        "worklifebalance",
        "work-life balance"

    ],

    # ------------------------------------------------------
    # DISTANCE
    # ------------------------------------------------------

    "distance": [

        "ride distance",
        "distance",
        "travel distance"


],

"external_factors": [

    "temperature",
    "fuel price",
    "fuel_price",
    "cpi",
    "unemployment"

],

"payment_method": [

    "payment method",
    "payment_method",
    "paymentmethod"

],


"shipping_address": [

    "shipping address",
    "shipping_address"

],


"order_status": [

    "order status",
    "order_status",
    "orderstatus"

],

"forecast_target": [

    # Sales datasets
    "sales",
    "sales amount",
    "salesamount",
    "revenue",
    "weekly sales",
    "weekly_sales",

    # Online store
    "total price",
    "totalprice",
    "invoice amount",
    "invoice value",

    # Uber / Ride datasets
    "booking value",
    "bookingvalue",
    "ride fare",
    "fare amount",
    "trip amount",

    # Transactions / Finance
    "amount",
    "transaction amount",
    "transaction value",
    "income",
    "turnover"

]

}

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def normalize(text):
    return (
        text.lower()
        .replace("_", " ")
        .replace("-", " ")
        .strip()
    )


def find_best_column(columns, keywords):

    normalized = {
        col: normalize(col)
        for col in columns
    }

    # Exact match
    for keyword in keywords:
        keyword = normalize(keyword)

        for col, value in normalized.items():

            if value == keyword:
                return col

    # Partial match
    for keyword in keywords:
        keyword = normalize(keyword)

        for col, value in normalized.items():

            if keyword in value:
                return col

    return None

def build_semantic_model(df):

    semantic = {}

    columns = df.columns.tolist()

    for concept, keywords in BUSINESS_CONCEPTS.items():

        column = find_best_column(
            columns,
            keywords
        )

        if column is not None:
            semantic[concept] = column

    print("SEMANTIC MODEL")
    print(semantic)

    return semantic