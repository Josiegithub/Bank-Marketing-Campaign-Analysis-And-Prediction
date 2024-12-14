
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Bank Client Subscription Prediction App",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Title and introduction
st.title("Bank Client Subscription Prediction")
st.markdown(
    """
    This app uses machine learning to predict the likelihood of a client subscribing to a bank's term deposit product.  
    By inputting relevant customer details, the app generates accurate predictions to support your decision-making.
    """
)

# Features
st.subheader("Key Features")
st.markdown(
    """
    - **Prediction**: Input customer details to predict subscription likelihood.
    - **User-Friendly**: Intuitive interface for seamless user experience.
    - **Quick Results**: Instant insights at your fingertips.
    """
)

# Steps for prediction
st.subheader("How It Works")
st.markdown(
    """
    1. **Input Data**: Provide the required customer details (features).  
    2. **Get Prediction**: The app processes your input and predicts the likelihood of subscription.  
    3. **Make Informed Decisions**: Use the results to guide your actions.  
    """
)

# Benefits of the app
st.subheader("Why Use This App?")
st.markdown(
    """
    - **Precise Predictions**: Focus your efforts on customers most likely to subscribe.  
    - **Data-Driven Decision Making**: Enhance strategies with reliable insights.  
    - **Improved Efficiency**: Prioritize high-potential leads effectively.  
    """
)

# About the model
st.subheader("Model Information")
st.markdown(
    """
    The app utilizes a powerful machine learning model trained on historical customer data, considering factors such as age, job type, marital status, education level, housing loan status, personal loan status, previous campaign outcomes, and consumer confidence index. These diverse inputs help deliver precise predictions.  
While the predictions are reliable, they should be incorporated into a broader decision-making strategy rather than serving as the sole basis for actions..
    """
)


# Contact information
st.subheader("Contact Us")
customer_support_email = "josephine.asante@azubiafrica.org"
st.markdown(f"""
For inquiries or assistance, please reach out to our support team [here]({customer_support_email}).
""")
