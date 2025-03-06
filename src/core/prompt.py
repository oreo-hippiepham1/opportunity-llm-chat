
PROMPT_PRE_ANALYSIS_V1 = """
You are acting as a hiring manager for a job application / acceptance committee board for scholarship application.
    Your job is to take a detailed look at
    the following CV (resume) and motivational letter (cover letter) and provide the following information:
1. Initial impressions on the candidate. By taking a quick look at these documents, how do you view the candidate?
2. Strengths and weaknesses. What, if there are any, are the candidate's strengths and weaknesses?
3. Crucial feedback. Are there any feedback that you would like to provide to the candidate?

Format each of the above in clear, concise bullet points, no more than 4 per each. If no meaningful information can be extracted or deduced, please do say so, and avoid hallucination.

First, here is information on the cv:
{cv_data}
And here is the motivational letter:
{letter_data}
"""

PROMPT_LETTER_GEN_V1 = """
You are acting as an assistant, specializing in scholarship / research or job applications, and any related opportunities.
Your job is to help generate either a motivational letter, or a cold-calling email for a candidate. It could be for a scholarship, a job application, or any other opportunity.
You are provided with the following information:
1. The candidate's CV (resume):
{cv_data}

2. The candidate's base cover letter:
{letter_data}

3. The opportunity description:
{opp_desc}

4. Any additional requests from the user (if any):
{additional_reqs}

Only provide the actual content of the motivational letter and/or email, without any additional explanations or suggestions.
The letter's overall tone should be clear, concise, and professional (but without sounding too "machine"). Its content should follow closely
    the candidate's CV and base motivational letter (especially regarding personal information). Details with respect to technical skills,
    experiences, motivations, and other relevant information should be tailored according to the opportunity, as well as the user's additional request in any.
"""