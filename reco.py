import streamlit as st
import pandas as pd

# Load Mentee and Mentor CSV files
mentee_df = pd.read_csv("Mentee.csv")
mentor_df = pd.read_csv("Mentor.csv")

# Function to recommend mentors based on the gap and rating
def recommend_mentors(mentee_df, mentor_df, employee_id):
    # Filter mentee data for the given employee_id
    mentee_data = mentee_df[mentee_df['Employee ID'] == employee_id]
    recommended_mentors = {}

    for index, row in mentee_data.iterrows():
        skill = row['Skill']
        rating = row['Rating']

        # Check if the skill rating allows mentor recommendation
        if rating.lower() in ['below', 'way below']:
            # Find mentors for the skill with proficiency level >= gap
            mentors_for_skill = mentor_df[(mentor_df['Skill'] == skill)]
            if not mentors_for_skill.empty:
                mentors_for_skill = mentors_for_skill.sort_values(by='Proficiency Level', ascending=False)
                recommended_mentors[skill] = mentors_for_skill

    return recommended_mentors

def main():
    st.title('Mentor Recommendation System')

    # Dropdown for selecting employee ID
    selected_employee_id = st.selectbox('Select Employee ID', mentee_df['Employee ID'].unique())

    if selected_employee_id:
        # Retrieve user skills
        user_data = mentee_df[mentee_df['Employee ID'] == selected_employee_id]
        user_skills = user_data[['Skill', 'Rating', 'Proficiency Level', 'Target', 'Gap']].reset_index(drop=True)  # Reset index to remove index number

        # Center-align the table
        st.markdown("<h3 style='text-align: center;'>Your Skills and Ratings</h3>", unsafe_allow_html=True)
        
        # Convert Gap to whole number and display "-" for blank values
        user_skills['Gap'] = user_skills['Gap'].apply(lambda x: "-" if pd.isnull(x) else int(x))

        # Add custom index starting at 1
        user_skills.index = user_skills.index + 1

        # Display the table with centered content
        st.table(user_skills.style.set_properties(**{'text-align': 'center'}))

        # Recommend mentors
        recommended_mentors = recommend_mentors(mentee_df, mentor_df, selected_employee_id)

        st.subheader('Recommended Mentors')
        for skill, mentors in recommended_mentors.items():
            st.write(f"For {skill}:")
            if not mentors.empty:
                # Sort mentors based on proficiency level from highest to lowest
                mentors_sorted = mentors.sort_values(by='Proficiency Level', ascending=False)
                # Reset index to start at 1
                mentors_sorted.reset_index(drop=True, inplace=True)
                # Add custom index starting at 1
                mentors_sorted.index = mentors_sorted.index + 1
                # Display recommended mentors with selected columns
                st.table(mentors_sorted[['Employee ID', 'Skill', 'Proficiency Level']].style.set_properties(**{'text-align': 'center'}))
            else:
                st.write("No mentors found for this skill.")

if __name__ == '__main__':
    main()
