import streamlit as st
from tech import *  # Ensure tech.py contains all necessary functions
from assistant import *
# import pycountry




# PAGES
# home
def home():
    st.title('AuditHelper')
    st.header("AI environmental report evaluation")
    st.write('Choose one option:')

    # buttons
    if st.button("check full report"):
        st.session_state.page = "full report check 1"
        st.rerun()

    if st.button("check report block"):
        st.session_state.page = "block report check 1"
        st.rerun()

# full report check 1
def full_report_form():
    st.title("Full report check")
    st.subheader("Step 1. Fill in the form:")

    st.session_state.industry = st.selectbox('Industry', ['Banking', 'Mining', 'Manufacturing'], index=None)
    st.session_state.company_size = st.selectbox('Company size:', ['10+', '100+', '1000+', '10000+'], index=None)
    st.session_state.standards = st.selectbox('Standards:', ['TCFD', 'GRI', 'SASB', 'ISO14001'])

    st.subheader('Step 2. Upload the report')
    uploaded_report = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'])

    if uploaded_report:
        st.session_state.uploaded_report = uploaded_report
        st.session_state.uploaded_report_type = uploaded_report.type.split('/')[-1]

        # button to continue
        if st.button("get results"):
            st.session_state.page = "full report check 2"
            st.experimental_rerun()


# full report check 2
def full_report_results():
    st.title("Full report check")
    # placeholder = st.empty()

    if 'uploaded_report' in st.session_state:
        get_full_report_check(st.session_state.uploaded_report)    


    if st.button('home'):
        st.session_state.page = "home"
        st.experimental_rerun()


# block report check 1
def block_report_form():
    st.title("Block report check")
    st.subheader("Step 1. Fill in the form:")

    st.session_state.standards = st.selectbox('Standards:', ['TCFD', 'GRI', 'SASB', 'ISO14001'])
    st.session_state.block = st.selectbox('Report block:', ['block 1', 'block 2'])

    # input report block
    st.subheader('Step 2. Type or upload the report block text')
    user_text = st.text_area("Enter your text here:")
    uploaded_file = st.file_uploader("Or choose a file:", type=['pdf', 'docx', 'txt'])

    st.session_state.report_block_text = None
    st.session_state.uploaded_file = None
    if user_text:
        st.session_state.report_block_text = user_text
    elif uploaded_file:
        # file_type = uploaded_file.type.split('/')[-1]
        st.session_state.uploaded_file = uploaded_file
        # st.session_state.uploaded_report_type = file_type
        # st.session_state.report_block_text = get_file_text(uploaded_file, file_type)

    # button to continue
    if st.session_state.report_block_text:
        if st.button("continue"):
            st.session_state.page = "block report check 2"
            st.rerun()

    elif st.session_state.uploaded_file:
        if st.button("continue"):
            st.session_state.page = "block report check 2"
            st.rerun()

# # block report check 2
def block_report_results():
    st.title("Block report check")
    placeholder = st.empty()

    if st.session_state.page == 'home':
        return

    if 'report_block_text' in st.session_state and st.session_state.report_block_text is not None:    
        get_assistant_response(st.session_state.report_block_text)
#         # running the analysis process
#         placeholder.text('Analysis running...')
#         block_analysis_results = run_block_report_analysis(st.session_state.report_block_text)
#         st.session_state.block_analysis_results = block_analysis_results
#         placeholder.text('Analysis completed!')

#         # general feedback and recommendations in short format
#         st.subheader("General feedback")
#         st.write(st.session_state.block_analysis_results['short_feedback'])

#         st.subheader("General recommendations")
#         st.write(st.session_state.block_analysis_results['short_recommendations'])

        # buttons
        if st.button('generate report block using recommendations and new information'):
            st.session_state.page = 'block report generation'
            st.experimental_rerun()
        if st.button('home'):
            st.session_state.page = 'home'
            st.experimental_rerun()
    
    if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
        get_part_report_check(st.session_state.uploaded_file)    

        # buttons
        if st.button('generate report block using recommendations and new information'):
            st.session_state.page = 'block report generation'
            st.experimental_rerun()
        if st.button('home'):
            st.session_state.page = 'home'
            st.experimental_rerun()



# block report generation
def block_report_generation():
    st.title('Block report generation')
    st.subheader('Type new information:')
    new_info_text = st.text_area("Enter your text here:")
    placeholder = st.empty()

    if new_info_text:
        if st.button('generate'):
            # running the generation process
            placeholder.text('Generation running...')
            generation_results = generate_block(st.session_state.report_block_text, new_info_text)
            st.session_state.generation_results = generation_results
            placeholder.text('Generation completed!')

            # print generated block
            st.session_state.generated_block_text = st.session_state.generation_results['generated_block_text']

            st.subheader('Generated report block:')
            st.write(st.session_state.generated_block_text)
            
            # download results
            if 'generation_results' in st.session_state:
                with open(st.session_state.generation_results['generated_block_file'], 'rb') as file:
                    st.download_button(
                        label="download new report block",
                        data=file,
                        file_name="generated_report_block.txt",
                        mime="text/plain"
                    )
        
        if st.button('home'):
            st.session_state.page = "home"
            st.rerun()

# MAIN
# initialization of the page state
if 'page' not in st.session_state:
    st.session_state.page = "home"

# display the selected page
if st.session_state.page == "home":
    home()
elif st.session_state.page == "full report check 1":
    full_report_form()
elif st.session_state.page == "full report check 2":
    full_report_results()
elif st.session_state.page == "block report check 1":
    block_report_form()
elif st.session_state.page == "block report check 2":
    block_report_results()
elif st.session_state.page == "block report generation":
    block_report_generation()