from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

class StyleAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        os.environ["OPENAI_API_KEY"] = api_key

    def analyze_writing(self, sample_1, sample_2, sample_3):


        template = """Task: Analyze the following writing samples and create detailed instructions for mimicking this writer's unique writing style.
        Writing Samples:
        [Sample 1]
        {sample_1}
        [Sample 2]
        {sample_2}
        [Sample 3]
{sample_3}
Please analyze these writing samples and provide:
1. Core Writing Patterns
- Identify the writer's signature sentence structures
- Note any patterns in paragraph organization
- Describe their unique approach to introducing and developing ideas
- Point out distinctive punctuation usage

2. Language Choices
- List their frequently used words or phrases
- Identify any unusual word combinations or unique expressions
- Describe their level of formality and tone
- Note any recurring metaphors or analogies

3. Unique Stylistic Elements
- Highlight specific techniques that make their writing distinctive
- Identify their approach to emphasis and persuasion
- Note how they handle transitions between ideas
- Describe any special formatting or structural preferences

4. Direct Examples
Quote 3-5 passages that perfectly exemplify their unique style, explaining what makes each passage characteristic of their writing.

5. Style Replication Instructions
Provide clear, step-by-step instructions for replicating this writing style, including:
- Essential elements that must be included
- Patterns to avoid
- How to maintain authenticity while mimicking their style
- Specific techniques for different types of content (descriptions, arguments, etc.)

6. Additional Context
- Note any situational variations in their writing style
- Describe how their style adapts to different topics or audiences
- Highlight what makes their writing instantly recognizable

Important: Focus on unique and distinctive elements rather than common writing practices. Use specific examples from the provided samples to illustrate each point.
Format your analysis in clear, detailed sections. For each observation, provide at least one concrete example from the writing samples."""

        # Create the prompt template
        prompt = PromptTemplate(
            input_variables=["sample_1", "sample_2", "sample_3"],
            template=template
        )

        # Initialize the language model
        llm = ChatOpenAI(temperature=0.7, api_key=self.api_key)

        # Create the chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Generate the analysis
        result = chain.run({
            "sample_1": sample_1,
            "sample_2": sample_2,
            "sample_3": sample_3
        })

        return result

    def generate_article(self, style_analysis, interview_transcript, preliminary_notes):
    # Set your OpenAI API key (using the same key as before)

    # Create the prompt template for article generation
        article_template = """You are an expert writer tasked with creating a marketing research article based on an interview transcript. 
    You must write this article following the specific writing style described in the style analysis below.
    
    Style Analysis:
    {style_analysis}
    
    Interview Materials:
    [Interview Transcript]
    {interview_transcript}
    
    [Preliminary Notes]
    {preliminary_notes}
    
    Task: Write a marketing research article that:
    1. Follows the writing style patterns described in the style analysis, including:
       - Using the identified sentence structures
       - Following the paragraph organization patterns
       - Employing the characteristic word choices and phrases
       - Maintaining the same tone and level of formality
       - Using similar transition techniques
       
    2. Effectively presents the insights from the interview by:
       - Incorporating relevant quotes from the interview transcript
       - Organizing information in a logical flow
       - Highlighting key industry insights
       - Maintaining the balance between technical detail and accessibility
       - Including context from the preliminary notes where relevant
       
    3. Maintains the format of a marketing research article by:
       - Having a compelling headline
       - Including an engaging introduction
       - Presenting clear main points
       - Ending with a strong conclusion
       
    Important: The article should read as if it was written by the same person who wrote the sample articles analyzed earlier.
    
    Please write the complete article now:"""

    # Create the prompt template
        article_prompt = PromptTemplate(
        input_variables=["style_analysis", "interview_transcript", "preliminary_notes"],
        template=article_template
    )

    # Initialize the language model with slightly lower temperature for more focused output
        llm = ChatOpenAI(temperature=0.5, api_key=self.api_key)

    # Create the chain
        article_chain = LLMChain(llm=llm, prompt=article_prompt)

    # Generate the article
        result = article_chain.run({
        "style_analysis": style_analysis,
        "interview_transcript": interview_transcript,
        "preliminary_notes": preliminary_notes
    })

        return result

