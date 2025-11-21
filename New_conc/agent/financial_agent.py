"""
Financial AI Agent using LangChain with ReAct pattern
"""

from langchain_classic.agents import AgentExecutor, create_react_agent
from langchainhub import Client as HubClient
from langchain_classic.memory import ConversationBufferMemory
from agent.config import Config
from agent.prompts import SYSTEM_PROMPT, USER_CONTEXT_TEMPLATE
from agent.tools import (
    analyze_portfolio,
    analyze_transactions,
    fetch_market_data,
    generate_insights,
    check_goal_alignment
)
from data.mock_user import USER_PROFILE


class FinancialAgent:
    """
    LangChain-based agent for financial relationship management
    """
    
    def __init__(self):
        """Initialize the financial agent with tools and memory"""
        
        # Get LLM from config
        self.llm = Config.get_llm()
        
        # Initialize tools
        self.tools = [
            analyze_portfolio,
            analyze_transactions,
            fetch_market_data,
            generate_insights,
            check_goal_alignment
        ]
        
        # Create conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        
        # Create user context string
        user_context = USER_CONTEXT_TEMPLATE.format(
            name=USER_PROFILE['name'],
            age=USER_PROFILE['age'],
            risk_tolerance=USER_PROFILE['risk_tolerance'],
            investment_horizon=USER_PROFILE['investment_horizon'],
            financial_goals='\n'.join([f"- {goal}" for goal in USER_PROFILE['financial_goals']])
        )
        
        # Use the standard ReAct prompt from LangChain hub with custom system message
        try:
            # Get the standard ReAct prompt template
            hub_client = HubClient()
            base_prompt = hub_client.pull("hwchase17/react")
            
            # Prepend our custom system message and user context
            prompt_template = f"""{SYSTEM_PROMPT}

{user_context}

You are a helpful financial advisor. Use the available tools to answer questions.

{base_prompt.template}"""
            
            from langchain_core.prompts import PromptTemplate
            react_prompt = PromptTemplate(
                template=prompt_template,
                input_variables=base_prompt.input_variables
            )
        except:
            # Fallback: use standard ReAct format if hub is unavailable
            from langchain_core.prompts import PromptTemplate
            react_prompt = PromptTemplate.from_template(
                f"""{SYSTEM_PROMPT}

{user_context}

Answer the following questions as best you can. You have access to the following tools:

{{tools}}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{input}}
Thought:{{agent_scratchpad}}"""
            )
        
        # Create the agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=react_prompt
        )
        
        # Create agent executor with increased limits
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=15,  # Increased from 5 to allow more tool usage
            max_execution_time=60,  # 60 second timeout
            return_intermediate_steps=False,
            early_stopping_method="generate"  # Generate output even if max iterations reached
        )
    
    def chat(self, message: str) -> str:
        """
        Process a user message and return the agent's response
        
        Args:
            message: User's input message
            
        Returns:
            Agent's response string
        """
        try:
            response = self.agent_executor.invoke({"input": message})
            return response.get("output", "I apologize, but I encountered an error processing your request.")
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def reset_conversation(self):
        """Clear the conversation memory"""
        self.memory.clear()


# Singleton instance
_agent_instance = None

def get_agent() -> FinancialAgent:
    """Get or create the singleton agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = FinancialAgent()
    return _agent_instance
