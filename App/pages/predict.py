import streamlit as st
import joblib
import pandas as pd
import os
import datetime

# ===========================================================================================================
# Page Setup
st.set_page_config(
    page_title='Predict',
    layout='wide'
)

# ===========================================================================================================
# Load Pipelines
@st.cache_resource(show_spinner='Model loading')
def load_lgbm_pipeline():
    # Update path to be relative or use environment-specific configuration
    model_path = os.path.join('App','Model', 'lgbm_model_1')
    # model_path = r'C:\Users\Josephine\Desktop\Career Accelerator\Bank-Marketing-Campaign-Analysis-And-Prediction\App\Model\lgbm_model_1.pk1'
    return joblib.load(model_path)
   
    


# ===========================================================================================================
# Model Selection Function
def select_model():
    
    st.session_state['selected_model'] = 'Light GBM'
 
    pipeline = load_lgbm_pipeline()
    
    # Update path for encoder
    encoder_path = os.path.join('App', 'Model', 'LabelEncoder_1')
    #encoder_path = r'C:\Users\Josephine\Desktop\Career Accelerator\Bank-Marketing-Campaign-Analysis-And-Prediction\App\Model\LabelEncoder_1'
    encoder = joblib.load(encoder_path)
    return pipeline, encoder
  


# ===========================================================================================================
# Initialize Session State
if 'predictions' not in st.session_state:
    st.session_state.predictions = None
if 'probability' not in st.session_state:
    st.session_state.probability = None


# ===========================================================================================================
# Prediction Function
def make_prediction(pipeline, encoder):
    # Collect user inputs from session state
    features = ["age", "job","marital","education","default","housing","loan","contact","month",
                "day_of_week","duration","campaign","pdays","previous","poutcome","emp.var.rate","cons.price.idx",
                "cons.conf.idx","euribor3m","nr.employed"]
    data = [[st.session_state[feature] for feature in features]]
    df = pd.DataFrame(data, columns=features)

    # Add metadata for history
    df['Prediction time'] = datetime.date.today()
    df['selected_model'] = st.session_state['selected_model']
    history_path = 'History/history.csv'
    
    # Append history, ensuring file exists
    df.to_csv(history_path, mode='a', header=not os.path.exists(history_path), index=False)

    # Make prediction
    probability = pipeline.predict_proba(df)[0]
    predicted_class = int(probability[1])
    prediction = encoder.inverse_transform([predicted_class])
    
    # Store results in session state
    st.session_state['predictions'] = prediction[0]
    st.session_state['probability'] = probability
    
    return prediction[0], probability


# ===========================================================================================================
# Display Form Function
def display_form():
    pipeline, encoder = select_model()

    with st.form('input-feature'):
        col1, col2 = st.columns(2)

        with col1:
            st.number_input('Age', min_value=0, max_value=120, key='age')
            st.selectbox('Job', ['housemaid', 'services', 'admin.', 'blue-collar', 'technician', 'retired',
                                 'management', 'unemployed', 'self-employed', 'unknown', 'entrepreneur',
                                 'student'], key='job')
            st.selectbox('Marital Status', ['married', 'single', 'divorced', 'unknown'], key='marital')
            st.selectbox('Education Level', ['basic school', 'high school', 'professional course', 'unknown',
                                             'university degree', 'illiterate'], key='education')
            st.selectbox('Default Credit', ['yes', 'unknown', 'no'], key='default')
            st.selectbox('Housing Loan', ['no', 'yes', 'unknown'], key='housing')
            st.selectbox('Personal Loan', ['no', 'yes', 'unknown'], key='loan')
            st.selectbox('Contact Type', ['telephone', 'cellular'], key='contact')
            st.selectbox('Month', ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], key='month')
            st.number_input('Campaign Contacts', min_value=0, key='campaign')

        with col2:
            st.number_input('Days since Previous Campaign Contact', min_value=-1, key='pdays')
            st.number_input('Number of Previous Contacts', min_value=0, key='previous')
            st.selectbox('Previous Outcome', ['nonexistent', 'failure', 'success'], key='poutcome')
            st.number_input('Employment Variation Rate', value=0.0, key='emp.var.rate')
            st.number_input('Consumer Price Index', value=0.0, key='cons.price.idx')
            st.number_input('Euribor 3-month Rate', value=0.0, key='euribor3m')
            st.number_input('Number of Employees', min_value=0, key='nr.employed')
            st.selectbox('Day of Week', ['mon', 'tue', 'wed', 'thu', 'fri'], key='day_of_week')
            st.number_input('Durations', value=0 , key='duration')
            st.number_input('Consumer Confidence Index', value=0.0, key='cons.conf.idx')
            

        st.form_submit_button('Make Prediction', on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder=encoder))
        
# ===========================================================================================================
# Main Page
if __name__ == "__main__":
    st.title('Make Prediction')
    display_form()

    prediction = st.session_state['predictions']
    probability = st.session_state['probability']

    if prediction is None:
        st.markdown('### Predictions will show here')
    elif prediction == 'yes':
        probability_of_yes = probability[1] * 100
        st.markdown(f'### The customer has an estimated {round(probability_of_yes, 1)}% likelihood of subscribing.')
    else:
        probability_of_no = probability[0] * 100
        st.markdown(f'### The customer has an estimated {round(probability_of_no, 1)}% unlikelihood of subscribing.')